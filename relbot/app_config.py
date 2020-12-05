import relbot.json.json_reader as json_reader
from relbot.singleton import Singleton


class GlobalAppConfig(Singleton):
    def init(self, cfg_name, *args, **kwargs):
        self.config = json_reader.read(cfg_name)


class CommandConfig:
    def __init__(self, cfg_name, *args, **kwargs):
        self.config = json_reader.read(cfg_name)
