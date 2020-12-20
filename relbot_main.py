import discord
import relbot.json.json_reader as json_reader
from relbot.commands.commands_tracker import CommandsTracker
from relbot.app_config import GlobalAppConfig, GlobalCommandConfig
from relbot.database.database_manager import DatabaseManager

client = discord.Client()
guild = discord.Guild
database = DatabaseManager()
app_cfg = GlobalAppConfig("config.json").config
cmd_cfg = GlobalCommandConfig("commands.json").config
commands_tracker = CommandsTracker(client)


@client.event
async def on_message(message):
    if message.author.bot:
        return
    await commands_tracker.identify_command(message)


@client.event
async def on_reaction_add(reaction, user):
    for command in commands_tracker.commands:
        await command.on_reaction_add(reaction, user)


@client.event
async def on_reaction_remove(reaction, user):
    for command in commands_tracker.commands:
        await command.on_reaction_remove(reaction, user)


@client.event
async def on_ready():
    print('Loaded Discord.py version {}'.format(discord.__version__))
    print('We have logged in as {0.user}'.format(client))

client.run(json_reader.read(app_cfg['token_filename']))
