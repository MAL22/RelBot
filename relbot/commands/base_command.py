from enum import Enum
from abc import ABC, abstractmethod
from relbot.database.database_manager import DatabaseManager
from relbot.app_config import GlobalCommandConfig, GlobalAppConfig, GlobalLanguageConfig


class ArgumentsMetadata:
    def __init__(self, required_arguments=None, optional_arguments=None):
        if required_arguments is None:
            self._required_arguments = {}
        else:
            self._required_arguments = required_arguments

        if optional_arguments is None:
            self._optional_arguments = {}
        else:
            self._optional_arguments = optional_arguments

    @property
    def required_arguments(self):
        return self._required_arguments

    @property
    def optional_arguments(self):
        return self._optional_arguments


class BaseCommand(ABC):
    def __init__(self, client, internal_name, display_name, long_desc, short_desc, prefix_required=True, hidden=False, remove_output=False, arguments_metadata=ArgumentsMetadata()):
        self._app_config: GlobalAppConfig = GlobalAppConfig()
        self._command_config = GlobalCommandConfig().config[internal_name]
        self._language_config = GlobalLanguageConfig().config
        self._database_manager: DatabaseManager = DatabaseManager()
        self._client = client

        self.prefix_required = prefix_required
        self._internal_name = internal_name
        self._display_name = display_name
        self.long_desc = long_desc
        self.short_desc = short_desc
        self.arguments_metadata = arguments_metadata
        self._enabled = self._command_config['enabled']
        self._hidden = hidden
        self._aliases = self._command_config['aliases']
        self._remove_output = remove_output
        self._extra_parameters = self._command_config['parameters']
        self.command_template = self._assemble_command_template()

    @property
    def internal_name(self):
        return self._internal_name

    @property
    def name(self):
        return self._display_name

    @property
    def aliases(self):
        return self._aliases

    @property
    def extra_parameters(self):
        return self._extra_parameters

    @property
    def hidden(self):
        return self._hidden

    @abstractmethod
    async def on_message(self, message):
        raise NotImplementedError

    @abstractmethod
    async def on_reaction_add(self, reaction, user):
        raise NotImplementedError

    @abstractmethod
    async def on_reaction_remove(self, reaction, user):
        raise NotImplementedError

    @abstractmethod
    async def on_error(self, message, error):
        raise NotImplementedError

    def _assemble_command_template(self):
        template = '({})'.format(', '.join(self._aliases))
        for _, argument in self.arguments_metadata.required_arguments.items():
            template += ' {}'.format(argument['display_name'])
        for _, argument in self.arguments_metadata.optional_arguments.items():
            template += ' [{}]'.format(argument['display_name'])
        return template

    @abstractmethod
    async def _validate_args(self, message, *args):
        max_expected_args = len(self.arguments_metadata.required_arguments) + len(self.arguments_metadata.optional_arguments)

        if len(args) < len(self.arguments_metadata.required_arguments):

            if len(self.arguments_metadata.required_arguments) > 1:
                raise SyntaxError(GlobalLanguageConfig().config['Errors']['MissingArgumentsPlural'].format(
                    cmd_name=self.name, num_expected_arguments=len(self.arguments_metadata.required_arguments), num_received_args=len(args)))
            else:
                raise SyntaxError(GlobalLanguageConfig().config['Errors']['MissingArgumentsSingular'].format(
                    cmd_name=self.name, num_expected_arguments=len(self.arguments_metadata.required_arguments), num_received_args=len(args)))

        if len(args) > max_expected_args:

            if max_expected_args > 1:
                raise SyntaxError(GlobalLanguageConfig().config['Errors']['TooManyArgumentsPlural'].format(
                    cmd_name=self.name, num_expected_arguments=len(self.arguments_metadata.required_arguments) + len(self.arguments_metadata.optional_arguments),
                    num_received_args=len(args)))
            else:
                raise SyntaxError(GlobalLanguageConfig().config['Errors']['TooManyArgumentsSingular'].format(
                    cmd_name=self.name, num_expected_arguments=len(self.arguments_metadata.required_arguments) + len(self.arguments_metadata.optional_arguments),
                    num_received_args=len(args)))
