import importlib
from relbot.app_config import GlobalAppConfig
from relbot.json import json_reader
from relbot.singleton import Singleton
from relbot.commands import Command
from relbot.commands.reputation_commands import ReputationCommand


class CommandsTracker(Singleton):
    def init(self, client, *args, **kwargs):
        self.client = client
        self._commands = self._instantiate_commands()

    def _instantiate_commands(self):
        commands = {}
        for command in [cls(self.client) for cls in Command.__subclasses__()]:
            for alias in command.aliases:
                if alias in commands:
                    continue
                commands[alias] = command
        return commands

    async def identify_command(self, message):
        if message.content.startswith(GlobalAppConfig().config['prefix']):
            command, *args = message.content.strip(GlobalAppConfig().config['prefix']).split(' ')
            _has_prefix = True
        else:
            command, *args = message.content.split(' ')
            _has_prefix = False

        if (self._commands[command].requires_prefix and not _has_prefix) or (not self._commands[command].requires_prefix and _has_prefix):
            return
        await self._commands[command].execute(message)

    async def get_command(self, name):
        if self._commands[name] is None:
            return None
        return self._commands[name]


class DynCommandsTracker:
    def __init__(self, client):
        self.commands = {}
        test = json_reader.read('commands.json')
        for cmd in test:
            print(cmd)
            module = importlib.import_module(cmd['module'])
            class_ = getattr(module, cmd['class'])
            self.commands[cmd['name']] = class_(client)
        print(self.commands)
