from relbot.commands import Command
from relbot.singleton import Singleton
from relbot.reputation import reputation_commands


def _get_subclasses(client):
    return [cls(client) for cls in Command.__subclasses__()]


class CommandsTracker(Singleton):
    def init(self, client, *args, **kwargs):
        self.commands = _get_subclasses(client)
