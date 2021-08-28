import discord
import jujube
from jujube.app_config import GlobalAppConfig
from jujube.commands.commands import Commands
from jujube.utils.debug.logging import log


class JujubeClient(discord.Client):
    def __init__(self, *, loop=None, **options):
        discord.Client.__init__(self, loop=loop, **options)

        self._commands = options.pop('commands', Commands(self, GlobalAppConfig().prefix))

    @property
    def commands(self):
        return self._commands

    async def on_ready(self):
        log(f'Loaded Discord.py version {discord.__version__}')
        log('Connected as {0.user}'.format(self))
        log(f'{jujube.__title__} version {jujube.__version__}')

    async def on_message(self, message):
        await self.commands.on_message(message)

    async def on_reaction_add(self, reaction, user):
        await self.commands.on_reaction_add(reaction, user)

    async def on_reaction_remove(self, reaction, user):
        await self.commands.on_reaction_remove(reaction, user)
