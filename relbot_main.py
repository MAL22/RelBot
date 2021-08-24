import discord
import relbot.json.json_reader as json_reader
from relbot.commands.commands import Commands
from relbot.app_config import GlobalAppConfig, GlobalCommandConfig, JSONConfig, GlobalLanguageConfig
from relbot.database.database_manager import DatabaseManager

client = discord.Client()
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
    await commands.identify_command(message)


@client.event
async def on_reaction_add(reaction, user):
    await commands.on_reaction_add(reaction, user)


@client.event
async def on_reaction_remove(reaction, user):
    await commands.on_reaction_remove(reaction, user)


@client.event
async def on_ready():
    global commands
    commands = Commands(client)

    print('Loaded Discord.py version {}'.format(discord.__version__))
    print('Connected as {0.user}'.format(client))
    print('RelBot version {0}{1}'.format(app_info['ver'], '-' + app_info['env']))

client.run(json_reader.read('token'))
