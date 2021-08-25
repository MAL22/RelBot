import os
import discord
import importlib
from relbot.commands.base_command import BaseCommand
from relbot.commands import split_arguments
from relbot.app_config import GlobalLanguageConfig, GlobalCommandConfig


class Command(BaseCommand):
    def __init__(self, config):
        module = importlib.import_module(f"{config['module']}")
        self.enabled = config['enabled']
        self.prefix_required = config['prefix_required']
        self.hidden = config['hidden']
        self.name = config['name']
        self.aliases = config['aliases']

        try:
            if config['callbacks']['on_reaction_add']:
                self.on_message = getattr(module, config['callbacks']['on_message'])
        except AttributeError as e:
            print(e)
            self.on_message = None

        try:
            if config['callbacks']['on_reaction_add']:
                self.on_reaction_add = getattr(module, config['callbacks']['on_reaction_add'])
        except AttributeError as e:
            print(e)
            self.on_reaction_add = None

        try:
            if config['callbacks']['on_reaction_add']:
                self.on_reaction_remove = getattr(module, config['callbacks']['on_reaction_remove'])
        except AttributeError as e:
            print(e)
            self.on_reaction_remove = None

    async def on_error(self, message, error):
        raise NotImplementedError
