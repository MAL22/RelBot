import os
import re
import importlib
import shlex

from jujube.utils.debug.logging import log
from jujube.utils.singleton import Singleton
from jujube.json import json_reader
from jujube.commands.command import CommandOptions
from jujube.app_config import GlobalLanguageConfig, GlobalAppConfig
from jujube.utils.exceptions import NotOwnerException, NotAllowedGuildException


class Commands(Singleton):
    def init(self, client, prefix: str, *args, **kwargs):
        self.client = client
        self.prefix = prefix
        self._commands, self._quiet_commands, self._unique_commands, self.react_add_commands, self.react_rem_commands = self._instantiate_commands()

    @property
    def commands(self):
        return self._commands

    def _instantiate_commands(self, reload=False):
        commands = {}
        quiet_commands = []
        unique_commands = []
        react_add_commands = []
        react_rem_commands = []
        log('Parsing command json files...')
        for dirpath, dirnames, filenames in os.walk('./commands'):
            for filename in filenames:
                if re.match('([\w]+.[\w]+[.]+dis[\w]*)', filename):
                    log(f'skipped {filename}')
                    continue
                command_config = json_reader.read(os.path.join(dirpath, filename))
                if not command_config['module'] or not command_config['class']:
                    log(f'No module or class definition found in {filename}')
                    continue

                module = importlib.import_module(command_config['module'])
                if reload:
                    importlib.reload(module)
                class_ = getattr(module, command_config['class'])
                command = class_(self.client, CommandOptions(command_config), **command_config['parameters'])
                unique_commands.append(command)

                if command.params.commands:
                    for alias in command.params.commands:
                        if alias in commands:
                            log(f'Alias collision between {command} and {commands[alias]}')
                        else:
                            commands[alias] = command
                            log(f'Added \'{alias}\' {command} from {filename}')
                else:
                    quiet_commands.append(command)
                    log(f'Added {command} from {filename}')

                if hasattr(command, 'on_reaction_add'):
                    react_add_commands.append(command)
                if hasattr(command, 'on_reaction_remove'):
                    react_rem_commands.append(command)

        return commands, quiet_commands, unique_commands, react_add_commands, react_rem_commands

    def reload_commands(self):
        log('Reloading commands...')
        self._commands, self._quiet_commands, self._unique_commands, self.react_add_commands, self.react_rem_commands = self._instantiate_commands(reload=True)

    async def on_message(self, message):
        try:
            if message.author.bot:
                return

            has_prefix, command, args = self.get_args(message.content)
            log(f'Command: {command} |', f'prefix: {has_prefix} |', f'args: {args}')

            if command in self.commands:
                if self._commands[command].params.prefix_required and not has_prefix:
                    return
                if not self._commands[command].params.prefix_required and has_prefix:
                    return
                if not self._commands[command].params.enabled:
                    return

                    self._commands[command].verify_entitlements(message.author.id, message.channel.id, message.guild.id)
                    await self._commands[command].on_message(message, *args)
            else:
                """ Checking commands that do not have aliases. """
                for command in self._quiet_commands:
                    await command.on_message(message, *args)
        except KeyError as e:
            log(__class__, e)
        except NameError as e:
            log(__class__, e)
        except NotOwnerException as e:
            await message.channel.send(GlobalLanguageConfig().localization.errors.error_not_owner_exception)
            await message.delete()
        except NotAllowedGuildException as e:
            await message.channel.send(GlobalLanguageConfig().localization.errors.error_guild_not_allowed_exception)

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
            log("Ignoring message,", e)
            return False, None, []
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
