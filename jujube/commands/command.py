import discord
from abc import ABC, abstractmethod
from jujube.app_config import GlobalLanguageConfig
from jujube.commands.base_command import BaseCommand


class CommandOptions:
    def __init__(self, config: dict):
        self.commands = config['commands']
        self.min_args = config.pop('min_args', 0)
        self.max_args = config.pop('max_args', 0)
        self.expected_args = config.pop('expected_args', "")
        self.enabled = config['enabled']
        self.prefix_required = config['prefix_required']
        self.hidden = config['hidden']
        self.parameters = config['parameters']


class CommandParameter:
    def __init__(self, name, description):
        self._name = name
        self._description = description

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description


class Command(BaseCommand):
    def __init__(self, client: discord.Client, command_options: CommandOptions, localized_params=None):
        BaseCommand.__init__(self)
        self.client = client
        self.params = command_options
        self.localized_params = localized_params
        self._loc = GlobalLanguageConfig().localization

    @property
    @abstractmethod
    def localized_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def localized_long_desc(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def localized_short_desc(self):
        raise NotImplementedError


class OnMessageInterface(ABC):
    @abstractmethod
    async def on_message(self, message, *args, **kwargs):
        raise NotImplementedError

    @property
    @abstractmethod
    def command_template(self):
        raise NotImplementedError


class OnReactionAddInterface(ABC):
    @abstractmethod
    async def on_reaction_add(self, reaction, user, *args, **kwargs):
        raise NotImplementedError


class OnReactionRemoveInterface(ABC):
    @abstractmethod
    async def on_reaction_remove(self, reaction, user, *args, **kwargs):
        raise NotImplementedError


class OnReady(ABC):
    @abstractmethod
    async def on_ready(self, *args, **kwargs):
        raise NotImplementedError
