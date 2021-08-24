from relbot.app_config import GlobalAppConfig
from relbot.singleton import Singleton
from relbot.commands.base_command import BaseCommand
from relbot.commands.help_commands import HelpCommand
from relbot.commands.reputation_commands import ReputationCommand
from relbot.commands.secret_responses import SecretResponses


class CommandTracker(Singleton):
    def init(self, client, *args, **kwargs):
        self.client = client
        self._commands, self._unique_commands, self._hidden_commands = self._instantiate_commands()

    def _instantiate_commands(self):
        commands = {}
        unique_commands = {}
        hidden_commands = {}
        for cmd in BaseCommand.__subclasses__():
            cmd: BaseCommand
            print(cmd)
            print(f'\t{cmd.internal_name}')

        for command in [cls(self.client) for cls in BaseCommand.__subclasses__()]:
            if command.hidden:
                hidden_commands[command.internal_name] = command
            else:
                unique_commands[command.internal_name] = command
            for alias in command.aliases:
                if alias in commands:
                    continue
                commands[alias] = command
        return commands, unique_commands, hidden_commands

    async def identify_command(self, message):
        try:
            if message.content.startswith(GlobalAppConfig().prefix):
                command = message.content.strip(GlobalAppConfig().prefix).split(' ')[0]
                _has_prefix = True
            else:
                command = message.content.split(' ')[0]
                _has_prefix = False

            if (self._commands[command].prefix_required and not _has_prefix) or (not self._commands[command].prefix_required and _has_prefix):
                return
            await self._commands[command].on_message(message)
        except KeyError as e:
            print(e)
            for key, value in self._hidden_commands.items():
                await value.on_message(message)

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
