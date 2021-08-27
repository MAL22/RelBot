from abc import abstractmethod
from jujube.commands.base_command import BaseCommand


class HiddenCommand(BaseCommand):
    def __init__(self, client, name):
        super().__init__(client, name)

    @abstractmethod
    async def on_message(self, message):
        raise NotImplementedError

    @abstractmethod
    async def on_reaction_add(self, reaction, user):
        raise NotImplementedError

    @abstractmethod
    async def on_reaction_remove(self, reaction, user):
        raise NotImplementedError

    @abstractmethod
    async def on_error(self, message, error):
        raise NotImplementedError

    @abstractmethod
    async def _validate_args(self, message, *args):
        raise NotImplementedError
