import os
import discord
from relbot.app_config import GlobalAppConfig
from relbot.singleton import Singleton
from relbot.json import json_reader
from relbot.commands.base_command import BaseCommand
from relbot.commands.command import Command


class Commands(Singleton):
    def init(self, client, *args, **kwargs):
        self.client = client
        self._commands, self._unique_commands, self.react_add_commands, self.react_rem_commands = self._instantiate_commands()

    def _instantiate_commands(self):
        commands = {}
        react_add_commands = []
        react_rem_commands = []
        print("instantiating...")
        for dirpath, dirnames, filenames in os.walk(os.path.realpath('./commands')):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                command_config = json_reader.read(filepath)
                command: Command = Command(discord.Client(), command_config)
                commands[command.name] = command
                if command.on_reaction_add:
                    react_add_commands.append(command)
                if command.on_reaction_remove:
                    react_rem_commands.append(command)
                print(f'Added {command} to {self}')

        return commands, list(commands.values()), react_add_commands, react_rem_commands

    async def on_message(self, message):
        try:
            if message.content.startswith(GlobalAppConfig().prefix):
                command = message.content.strip(GlobalAppConfig().prefix).split(' ')[0]
                has_prefix = True
            else:
                command = message.content.split(' ')[0]
                has_prefix = False

            if self._commands[command].prefix_required and not has_prefix:
                return
            if not self._commands[command].prefix_required and has_prefix:
                return
            if not self._commands[command].on_message:
                return
            if not self._commands[command].enabled:
                return

            await self._commands[command].on_message(message)
        except KeyError as e:
            print(e)

    async def on_reaction_add(self, reaction, user):
        for command in self.react_add_commands:
            await command.on_reaction_add(reaction, user)

    async def on_reaction_remove(self, reaction, user):
        for command in self.react_rem_commands:
            await command.on_reaction_remove(reaction, user)
        pass

    def get_command(self, name, refer_by_alias=True):
        try:
            if refer_by_alias:
                return self._commands[name]
            else:
                return self._unique_commands[name]
        except KeyError as e:
            return None

    def get_commands(self, refer_by_alias=True):
        if refer_by_alias:
            return self._commands.items()
        else:
            return self._unique_commands.items()
