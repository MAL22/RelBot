from jujube.utils.debug.logging import log
from jujube.commands.command import Command, OnReactionRemoveInterface, OnReactionAddInterface, OnMessageInterface, CommandOptions


class ClearDirectMessages(Command, OnMessageInterface):
    def __init__(self, client, command_options: CommandOptions, **kwargs):
        Command.__init__(self, client, command_options)

    async def on_message(self, message, has_prefix: bool, command: str, *args, **kwargs):
        async for message_ in message.author.history():
            if message.author.id == self.client.user.id:
                await message_.delete()
