import discord
import relbot.json.json_reader as json_reader
from relbot.utils.logging import log
from relbot.commands.commands import Commands
from relbot.app_config import GlobalAppConfig, GlobalCommandConfig, JSONConfig, GlobalLanguageConfig
from relbot.database.database_manager import DatabaseManager

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

client = discord.Client(intents=intents)
guild = discord.Guild
database = DatabaseManager()
app_cfg = GlobalAppConfig("config.json")
cmd_cfg = GlobalCommandConfig("commands.json").config
lng_cfg = GlobalLanguageConfig(app_cfg.language)
app_info = JSONConfig("version").config
commands: Commands = None


@client.event
async def on_message(message):
    if message.author.bot:
        return
    await commands.on_message(message)


@client.event
async def on_reaction_add(reaction, user):
    await commands.on_reaction_add(reaction, user)


@client.event
async def on_reaction_remove(reaction, user):
    await commands.on_reaction_remove(reaction, user)


@client.event
async def on_ready():
    global commands
    log('Loaded Discord.py version {}'.format(discord.__version__))
    log('Connected as {0.user}'.format(client))
    log('RelBot version {0} {1}'.format(app_info['ver'], app_info['env']))

    commands = Commands(client)


client.run(json_reader.read('token'))
