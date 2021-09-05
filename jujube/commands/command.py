import os
from abc import ABC, abstractmethod
import discord
import importlib
from jujube.commands.base_command import BaseCommand
from jujube.commands import split_arguments
from jujube.app_config import GlobalLanguageConfig, GlobalCommandConfig


class CommandOptions:
    def __init__(self, config: dict):
        self.module = importlib.import_module(config['module'])
        self.commands = config['commands']
        self.min_args = config.pop('min_args', 0)
        self.max_args = config.pop('max_args', 0)
        self.expected_args = config.pop('expected_args', "")
        self.enabled = config['enabled']
        self.prefix_required = config['prefix_required']
        self.hidden = config['hidden']
        self.parameters = config['parameters']


class _Command(BaseCommand):
    def __init__(self, client: discord.Client, command_options: CommandOptions):
        self.client = client
        self.params = command_options

        try:
            if self.params.on_message:
                self.on_message = getattr(self.params.module, self.params.on_message)
        except AttributeError as e:
            print(e)
            self.on_message = None

        try:
            if self.params.on_reaction_add:
                self.on_reaction_add = getattr(self.params.module, self.params.on_reaction_add)
        except AttributeError as e:
            print(e)
            self.on_reaction_add = None

        try:
            if self.params.on_reaction_remove:
                self.on_reaction_remove = getattr(self.params.module, self.params.on_reaction_remove)
        except AttributeError as e:
            print(e)
            self.on_reaction_remove = None

    async def on_error(self, message, error):
        raise NotImplementedError


class Command(BaseCommand):
    def __init__(self, client: discord.Client, command_options: CommandOptions):
        self.client = client
        self.params = command_options


class OnMessageInterface(ABC):
    @abstractmethod
    async def on_message(self, message, has_prefix: bool, command: str, *args, **kwargs):
        raise NotImplementedError


class OnReactionAddInterface(ABC):
    @abstractmethod
    async def on_reaction_add(self, reaction, user, *args, **kwargs):
        raise NotImplementedError


class OnReactionRemoveInterface(ABC):
    @abstractmethod
    async def on_reaction_remove(self, reaction, user, *args, **kwargs):
        raise NotImplementedError