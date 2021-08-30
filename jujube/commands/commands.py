import os
import re
import importlib
import argparse
from jujube.utils.debug.timer import measure_exec_time
from jujube.utils.debug.logging import log
from jujube.singleton import Singleton
from jujube.json import json_reader
from jujube.commands.command import Command, CommandOptions


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
        for dirpath, dirnames, filenames in os.walk('./jujube/json/commands'):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                command_config = json_reader.read(filepath)
                command: Command = Command(CommandOptions(command_config))
                unique_commands.append(command)

                for alias in command.params.commands:
                    if alias in commands:
                        log(f'Alias collision between {command} and {commands[alias]}')
                    else:
                        commands[alias] = command
                        log(f'Added \'{alias}\' {command} to {self} from {filename}')

                if hasattr(command, 'on_reaction_add'):
                    react_add_commands.append(command)
                if hasattr(command, 'on_reaction_remove'):
                    react_rem_commands.append(command)

        return commands, unique_commands, react_add_commands, react_rem_commands

    def instantiate_test(self):
        commands = {}
        for dirpath, dirnames, filenames in os.walk('./jujube/json/commands'):
            for filename in filenames:
                pass


    async def on_message(self, message):
        try:
            has_prefix, command, *args = self.get_args(message)

            if command not in self._commands:
                return
            if self._commands[command].params.prefix_required and not has_prefix:
                return
            if not self._commands[command].params.prefix_required and has_prefix:
                return
            if not self._commands[command].params.on_message:
                return
            if not self._commands[command].params.enabled:
                return

            await self._commands[command].on_message(self.client, message)

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
            return self._commands.items()
        else:
            return self._unique_commands

    @measure_exec_time
    def get_args(self, message) -> (bool, str, [str]):
        parser = argparse.ArgumentParser()
        parser.add_argument()
        log(re.split('[ \"]{0}([^\"]+)[ \"]{0}', message.content))
        command, *args = re.split('[\"]*([^\"]+)[\"]*', message.content)
        has_prefix = False
        if command.startswith(self.prefix):
            has_prefix = True
            command = command[1:]

        # log(has_prefix, command, *args)
        for idx, arg in enumerate(args):
            print(idx, ':', arg)

        return has_prefix, command, args
