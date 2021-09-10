import os
import re
import importlib
import shlex

from jujube.utils.debug.logging import log
from jujube.singleton import Singleton
from jujube.json import json_reader
from jujube.commands.command import CommandOptions


class Commands(Singleton):
    def init(self, client, prefix, *args, **kwargs):
        self.client = client
        self.prefix = prefix
        self._commands, self._unique_commands, self.react_add_commands, self.react_rem_commands = self._instantiate_commands()

    def _instantiate_commands(self):
        commands = {}
        unique_commands = []
        react_add_commands = []
        react_rem_commands = []
        log('Parsing command json files...')
        for dirpath, dirnames, filenames in os.walk('./commands'):
            for filename in filenames:
                if re.match('([\w]+.[\w]+[.]+dis[\w]*)', filename):
                    log(f'skipped {filename}')
                    continue
                filepath = os.path.join(dirpath, filename)
                command_config = json_reader.read(filepath)
                if not command_config['module'] or not command_config['class']:
                    log(f'no module or class definition found in {filename}')
                    continue
                module = importlib.import_module(command_config['module'])
                class_ = getattr(module, command_config['class'])
                command = class_(self.client, CommandOptions(command_config), **command_config['parameters'])
                unique_commands.append(command)

                for alias in command.params.commands:
                    if alias in commands:
                        log(f'Alias collision between {command} and {commands[alias]}')
                    else:
                        commands[alias] = command
                        log(f'Added \'{alias}\' {command} from {filename}')

                if hasattr(command, 'on_reaction_add'):
                    react_add_commands.append(command)
                if hasattr(command, 'on_reaction_remove'):
                    react_rem_commands.append(command)

        return commands, unique_commands, react_add_commands, react_rem_commands

    async def on_message(self, message):
        try:
            if message.author.bot:
                return

            has_prefix, command, args = self.get_args(message.content)
            log(f'Command: {command} |', f'prefix: {has_prefix} |', f'args: {args}')

            if command not in self._commands:
                return
            if self._commands[command].params.prefix_required and not has_prefix:
                return
            if not self._commands[command].params.prefix_required and has_prefix:
                return
            if not self._commands[command].params.enabled:
                return

            await self._commands[command].on_message(message, *args)

        except KeyError as e:
            log(__class__, e)
        except NameError as e:
            log(__class__, e)

    async def on_reaction_add(self, reaction, user):
        for command in self.react_add_commands:
            await command.on_reaction_add(reaction, user)

    async def on_reaction_remove(self, reaction, user):
        for command in self.react_rem_commands:
            await command.on_reaction_remove(reaction, user)

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
            return self._commands
        else:
            return self._unique_commands

    def get_args(self, message) -> (bool, str, [str]):
        try:
            command, *args = shlex.split(message)
            contains_prefix = command.startswith(self.prefix)
            if contains_prefix:
                command = command.strip(self.prefix)
        except ValueError as e:
            print(type(e))
            log("Ignoring message,", e)
            return False, None, None
        return contains_prefix, command, args

    """def get_args(self, message) -> (bool, str, [str]):
        matches = re.findall('["]([^"]*)["]|([^"][^" ]*[^" ])', message, re.I)
        args = []
        for grp1, grp2 in matches:
            if grp2 == '':
                args.append(grp1)
            else:
                args.append(grp2.strip(' '))
        command = args.pop(0)
        del matches

        has_prefix = False
        if command.startswith(self.prefix):
            has_prefix = True
            command = command[1:]

        return has_prefix, command, args"""
