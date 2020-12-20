import enum
from abc import ABC, abstractmethod
from relbot.database.database_manager import DatabaseManager
from relbot.app_config import GlobalCommandConfig, GlobalAppConfig


class ErrorType(enum.Enum):
    NoError = 0
    InvalidCommandName = 1
    MissingArguments = 2
    TooManyArguments = 3
    InvalidArguments = 4


class Command(ABC):
    def __init__(self, client, command_name, requires_prefix=True, required_params=None, optional_params=None):
        config = GlobalCommandConfig().config[command_name]

        self._database_manager: DatabaseManager = DatabaseManager()
        self._app_config = GlobalAppConfig().config

        self.client = client
        self.name = command_name
        self.requires_prefix = requires_prefix
        self.aliases = config['commands']
        self.automatic_removal = config['automatic_removal']
        self.params = config['parameters']
        self.required_params = required_params
        self.optional_params = optional_params
        self.template = self._build_cmd_template()

    @abstractmethod
    async def verify(self, message):
        pass

    @abstractmethod
    async def execute(self, message):
        pass

    @abstractmethod
    async def on_reaction_add(self, reaction, user):
        pass

    @abstractmethod
    async def on_reaction_remove(self, reaction, user):
        pass

    @abstractmethod
    def reload_config(self):
        pass

    @abstractmethod
    async def on_error(self, message, error):
        pass

    def _build_cmd_template(self):
        template = '{}'.format('|'.join(self.aliases))
        for argument in self.required_params:
            template += ' {}'.format(argument['name'])
        for argument in self.optional_params:
            template += ' [{}]'.format(argument['name'])
        return template

    @abstractmethod
    async def _parse_args(self, message):
        args = message.content.strip(self._app_config['prefix']).split(' ')
        if len(args) < 2:
            return []
        if len(args[1:]) < len(self.required_params):
            raise SyntaxError(ErrorType.MissingArguments)
        if len(args[1:]) > len(self.required_params) + len(self.optional_params):
            raise SyntaxError(ErrorType.TooManyArguments)
        return args[1:]
