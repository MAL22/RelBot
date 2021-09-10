from jujube.app_config import GlobalLanguageConfig
from jujube.utils.debug.logging import log
from jujube.commands.command import Command, OnReactionRemoveInterface, OnReactionAddInterface, OnMessageInterface, CommandOptions


class ClearDirectMessages(Command, OnMessageInterface):
    def __init__(self, client, command_options: CommandOptions, **kwargs):
        Command.__init__(self, client, command_options)

    @property
    def localized_name(self):
        return GlobalLanguageConfig()['commands']['cmd_reputation_command_name']

    @property
    def localized_long_desc(self):
        return GlobalLanguageConfig()['commands']['cmd_reputation_long_desc']

    @property
    def localized_short_desc(self):
        return GlobalLanguageConfig()['commands']['cmd_reputation_short_desc']

    @property
    def command_template(self):
        pass

    async def on_message(self, message, has_prefix: bool, command: str, *args, **kwargs):
        async for message_ in message.author.history():
            if message_.author.id == self.client.user.id:
                await message_.delete()
