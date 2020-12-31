import relbot.json.json_reader as json_reader
import configparser
import json
from json import JSONDecodeError
from relbot.singleton import Singleton


class GlobalAppConfig(Singleton):
    def init(self, cfg_name, *args, **kwargs):
        self.__config = json_reader.read(cfg_name)
        self.__cfg_name = cfg_name

    @property
    def prefix(self):
        return self.__config['prefix']

    @prefix.setter
    def prefix(self, new_prefix):
        self.__config['prefix'] = new_prefix
        json_reader.write(self.__cfg_name, self.__config)

    @property
    def deletion_delay(self):
        return self.__config['deletion_delay']

    @deletion_delay.setter
    def deletion_delay(self, new_delay):
        self.__config['deletion_delay'] = new_delay
        json_reader.write(self.__cfg_name, self.__config)

    @property
    def language(self):
        return self.__config['language']

    @language.setter
    def language(self, new_language):
        self.__config['language'] = new_language
        json_reader.write(self.__cfg_name, self.__config)


class GlobalCommandConfig(Singleton):
    def init(self, cfg_name, *args, **kwargs):
        try:
            self.config = json_reader.read(cfg_name)
        except JSONDecodeError as e:
            raise e


class GlobalLanguageConfig(Singleton):
    def init(self, cfg_name, *args, **kwargs):
        self.__config = configparser.ConfigParser()
        self.__config.read(f'langs\\{cfg_name}')

    @property
    def config(self):
        return self.__config


class JSONConfig:
    def __init__(self, cfg_name, *args, **kwargs):
        self.config = json_reader.read(cfg_name)
