import os
import discord
import importlib
from jujube.commands.base_command import BaseCommand
from jujube.commands import split_arguments
from jujube.app_config import GlobalLanguageConfig, GlobalCommandConfig


class CommandOptions:
    def __init__(self, module_to_import, commands, expected_args, min_args=0, max_args=None, enabled=True, prefix_required: bool=True, hidden: bool=False, on_message=None, on_reaction_add=None, on_reaction_remove=None):
        self.module = importlib.import_module(module_to_import)
        self.commands = commands
        self.min_args = min_args
        self.max_args = max_args
        self.expected_args = expected_args
        self.enabled = enabled
        self.prefix_required = prefix_required
        self.hidden = hidden
        self.on_message = on_message
        self.on_reaction_add = on_reaction_add
        self.on_reaction_remove = on_reaction_remove

    def __init__(self, config: dict):
        self.module = importlib.import_module(config['module'])
        self.commands = config['commands']
        self.min_args = config['min_args']
        self.max_args = config['max_args']
        self.expected_args = config['expected_args']
        self.enabled = config['enabled']
        self.prefix_required = config['prefix_required']
        self.hidden = config['hidden']
        self.on_message = config['callbacks']['on_message']
        self.on_reaction_add = config['callbacks']['on_reaction_add']
        self.on_reaction_remove = config['callbacks']['on_reaction_remove']


class Command(BaseCommand):
    def __init__(self, command_options: CommandOptions):
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
