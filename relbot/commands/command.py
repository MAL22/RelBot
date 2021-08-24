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

        self._on_message_callback = getattr(module, config['on_message_callback'])
        self._on_reaction_add_callback = getattr(module, config['on_reaction_add_callback'])
        self._on_reaction_remove_callback = getattr(module, config['on_reaction_remove_callback'])

    async def on_message(self, message):
        if self._on_message_callback is None:
            return
        await self._on_message_callback(discord.Client(), message)

    async def on_reaction_add(self, reaction, user):
        if self._on_reaction_add_callback is None:
            return
        self._on_reaction_add_callback(discord.Client(), reaction, user)

    async def on_reaction_remove(self, reaction, user):
        if self._on_reaction_remove_callback is None:
            return
        self._on_reaction_remove_callback(reaction, user)

    async def on_error(self, message, error):
        raise NotImplementedError
