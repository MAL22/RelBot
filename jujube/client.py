import discord
import jujube
from jujube.app_config import GlobalAppConfig
from jujube.commands.commands import Commands
from jujube.utils.debug.logging import log


class JujubeClient(discord.Client):
    def __init__(self, *, loop=None, **options):
        discord.Client.__init__(self, loop=loop, **options)
        self._commands: Commands = None

    @property
    def commands(self):
        if self._commands is None:
            raise Exception('Commands object not initialized')
        return self._commands

    async def on_ready(self):
        log(f'Loaded Discord.py version {discord.__version__}')
        log('Connected as {0.user}'.format(self))
        log(f'{jujube.__title__} version {jujube.__version__}')
        self._commands = Commands(self, GlobalAppConfig().prefix)

    async def on_message(self, message):
        await self.commands.on_message(message)

    async def on_message_edit(self, before, after):
        pass

    """ Reaction related event handlers """

    async def on_reaction_add(self, reaction, user):
        await self.commands.on_reaction_add(reaction, user)

    async def on_raw_reaction_add(self, payload):
        pass

    async def on_reaction_remove(self, reaction, user):
        await self.commands.on_reaction_remove(reaction, user)

    async def on_raw_reaction_remove(self, payload):
        pass

