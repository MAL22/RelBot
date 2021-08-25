import os
import discord
import importlib
from relbot.commands.base_command import BaseCommand
from relbot.commands import split_arguments
from relbot.app_config import GlobalLanguageConfig, GlobalCommandConfig


class Command(BaseCommand):
    def __init__(self, client: discord.Client, config):
        module = importlib.import_module(f"{config['module']}")

        self._client = client
        self.enabled = config['enabled']
        self.prefix_required = config['prefix_required']
        self.hidden = config['hidden']

        self.name = config['name']
        self.aliases = config['aliases']

        self.on_message = None if not config['on_message_callback'] else getattr(module, config['on_message_callback'])
        self.on_reaction_add = None if not config['on_reaction_add_callback'] else getattr(module, config['on_reaction_add_callback'])
        self.on_reaction_remove = None if not config['on_reaction_remove_callback'] else getattr(module, config['on_reaction_remove_callback'])

    async def on_error(self, message, error):
        raise NotImplementedError
