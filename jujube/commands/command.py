import inspect
from typing import List

import discord
from abc import ABC, abstractmethod
from jujube.app_config import GlobalLanguageConfig
from jujube.app_config import GlobalAppConfig
from jujube.commands.base_command import BaseCommand
from jujube.utils.exceptions import NotOwnerException, NotAllowedGuildException


class CommandOptions:
    def __init__(self, config: dict):
        self.enabled = config.pop('enabled', False)
        self.commands = config.pop('commands', None)
        self.prefix_required = config.pop('prefix_required', True)
        self.hidden = config.pop('hidden', False)
        self.owner_only = config.pop('owner_only', False)
        self.allowed_guilds = config.pop('allowed_guilds', [])
        self.blocked_guilds = config.pop('blocked_guilds', [])
        self.requires_role = config.pop('requires_role', [])
        self.min_args = config.pop('min_args', 0)
        self.max_args = config.pop('max_args', 0)
        self.expected_args = config.pop('expected_args', None)
        self.optional_args = config.pop('optional_args', None)
        self.parameters = config.get('parameters', {})


class Command(BaseCommand):
    def __init__(self, client: discord.Client, command_options: CommandOptions):
        BaseCommand.__init__(self)
        self.client = client
        self.params = command_options
        self._loc = GlobalLanguageConfig().localization

    @property
    def localized_name(self):
        return ""

    @property
    def localized_long_desc(self):
        return ""

    @property
    def localized_short_desc(self):
        return ""

    def verify_entitlements(self, user_id, channel_id, guild_id):
        if self.params.owner_only and user_id != GlobalAppConfig().owner_id:
            raise NotOwnerException
        if self.params.blocked_guilds and guild_id in self.params.blocked_guilds:
            raise NotAllowedGuildException


class OnMessageInterface(ABC):
    def __init__(self, aliases: str, string_keys: List[str] = None):
        self._localized_params = init_localized_params(self.on_message, string_keys)
        self._command_template = generate_command_template(aliases, self.on_message)

    @abstractmethod
    async def on_message(self, message, *args, **kwargs):
        raise NotImplementedError

    @property
    def command_template(self) -> str:
        return self._command_template

    @property
    def localized_params(self) -> dict[str, str]:
        return self._localized_params


class OnReactionAddInterface(ABC):
    @abstractmethod
    async def on_reaction_add(self, reaction, user, *args, **kwargs):
        raise NotImplementedError

    """@abstractmethod
    async def on_raw_reaction_add(self, reaction, user, *args, **kwargs):
        raise NotImplementedError"""


class OnReactionRemoveInterface(ABC):
    @abstractmethod
    async def on_reaction_remove(self, reaction, user, *args, **kwargs):
        raise NotImplementedError

    """@abstractmethod
    async def on_raw_reaction_remove(self, reaction, user, *args, **kwargs):
        raise NotImplementedError"""


class OnReadyInterface(ABC):
    @abstractmethod
    async def on_ready(self, *args, **kwargs):
        raise NotImplementedError


def generate_command_template(commands, func) -> str:
    if len(commands) > 1:
        aliases = f'({", ".join(commands)})'
    else:
        aliases = f'{commands[0]}'

    params = ""
    sig = inspect.signature(func)
    for param in list(sig.parameters.values())[1:len(sig.parameters) - 2]:
        if param.default == inspect._empty:
            params += f'[{param.name}]'
        else:
            params += f'<{param.name}>'
    return f'{aliases} {params}'


def init_localized_params(func, string_keys: List[str]) -> dict[str, str]:
    localized_params = {}
    sig = inspect.signature(func)
    for idx, param in enumerate(list(sig.parameters.values())[1:len(sig.parameters) - 2]):
        localized_params[param.name] = string_keys[idx]
    return localized_params
