import enum
import sys
from abc import ABC, abstractmethod
from relbot.database.database_manager import DatabaseManager
from relbot.app_config import CommandConfig, GlobalAppConfig


class ErrorType(enum.Enum):
    NoError = 0
    InvalidCommandName = 1
    MissingArguments = 2
    TooManyArguments = 3
    InvalidArguments = 4


class Command(ABC):
    def __init__(self, client, config: dict):
        self._database_manager: DatabaseManager = DatabaseManager()
        self._app_config = GlobalAppConfig().config
        self.config = CommandConfig(config).config
        self.client = client
        self.name = self.config['name']
        self.commands = self.config['commands']
        self.automatic_removal = self.config['automatic_removal']
        self.required_args = self.config['required_arguments']
        self.optional_args = self.config['optional_arguments']

    async def _parse_args(self, message):
        args = message.content.strip(self._app_config['prefix']).split(' ')
        if args[0] not in self.commands:
            raise ValueError(ErrorType.InvalidCommandName)
        if len(args[1:]) < self.required_args:
            raise ValueError(ErrorType.MissingArguments)
        if len(args[1:]) > self.required_args + self.optional_args:
            raise ValueError(ErrorType.TooManyArguments)
        return args[1:]

    @abstractmethod
    async def verify(self, message):
        pass

    @abstractmethod
    async def execute(self, message, *args):
        pass

    @abstractmethod
    def on_reaction_add(self, reaction, user):
        pass

    @abstractmethod
    def on_reaction_remove(self, reaction, user):
        pass

    @abstractmethod
    def reload_config(self):
        pass
