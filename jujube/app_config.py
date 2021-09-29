import jujube.json.json_reader as json_reader
import configparser
import json
from json import JSONDecodeError
from jujube.utils.map import Map
from jujube.utils.debug.timer import measure_exec_time
from jujube.utils.singleton import Singleton


class GlobalAppConfig(Singleton):
    def init(self, cfg_name, *args, **kwargs):
        self.__config = json_reader.read(cfg_name)
        self.__cfg_name = cfg_name

    @property
    def prefix(self):
        return self.__config['prefix']

    @property
    def owner_id(self):
        return self.__config['owner_id']

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
        self._config = configparser.ConfigParser()
        self._config.read(f'langs\\{cfg_name}')
        self._localization = Map({s: dict(self._config.items(s)) for s in self._config.sections()})

    @property
    def localization(self):
        return self._localization


class JSONConfig:
    def __init__(self, cfg_name, *args, **kwargs):
        self.config = json_reader.read(cfg_name)
