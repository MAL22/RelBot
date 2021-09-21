import discord
import jujube.json.json_reader as json_reader
from jujube.utils.timer import Timers
from jujube.client import JujubeClient
from jujube.app_config import GlobalAppConfig, GlobalLanguageConfig
from jujube.database.database_manager import DatabaseManager

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

app_cfg = GlobalAppConfig("config.json")
lng_cfg = GlobalLanguageConfig(app_cfg.language)

DatabaseManager()
Timers()

client = JujubeClient(intents=intents)

client.run(json_reader.read('token'))
