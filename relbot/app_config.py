from json import JSONDecodeError
from relbot.singleton import Singleton
import relbot.json.json_reader as json_reader


class GlobalAppConfig(Singleton):
    def init(self, cfg_name, *args, **kwargs):
        self.config = json_reader.read(cfg_name)


class GlobalCommandConfig(Singleton):
    def init(self, cfg_name, *args, **kwargs):
        try:
            self.config = json_reader.read(cfg_name)
        except JSONDecodeError as e:
            raise e


class CommandConfig:
    def __init__(self, cfg_name, *args, **kwargs):
        self.config = json_reader.read(cfg_name)
