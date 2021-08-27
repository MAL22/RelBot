import discord
import jujube.json.json_reader as json_reader
from jujube.client import JujubeClient
from jujube.utils.logging import log
from jujube.app_config import GlobalAppConfig, GlobalCommandConfig, JSONConfig, GlobalLanguageConfig
from jujube.database.database_manager import DatabaseManager

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

client = JujubeClient(intents=intents)
guild = discord.Guild
database = DatabaseManager()
app_cfg = GlobalAppConfig("config.json")
cmd_cfg = GlobalCommandConfig("commands.json").config
lng_cfg = GlobalLanguageConfig(app_cfg.language)
app_info = JSONConfig("version").config

client.run(json_reader.read('token'))
