from jujube.app_config import GlobalLanguageConfig
from jujube.utils.debug.logging import log
from jujube.commands.command import Command, OnReactionRemoveInterface, OnReactionAddInterface, OnMessageInterface, CommandOptions


class ClearDirectMessages(Command, OnMessageInterface):
    def __init__(self, client, command_options: CommandOptions, **kwargs):
        Command.__init__(self, client, command_options)
        OnMessageInterface.__init__(self, self.params.commands)

    @property
    def localized_name(self):
        return self._loc.commands.cmd_cleardirectmessages_name

    @property
    def localized_long_desc(self):
        return self._loc.commands.cmd_cleardirectmessages_long_desc

    @property
    def localized_short_desc(self):
        return self._loc.commands.cmd_cleardirectmessages_short_desc

    async def on_message(self, message, *args, **kwargs):
        async for message_ in message.author.history():
            if message_.author.id == self.client.user.id:
                await message_.delete()
