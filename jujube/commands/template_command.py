from jujube.utils.debug.logging import log
from jujube.commands.command import Command, OnReactionRemoveInterface, OnReactionAddInterface, OnMessageInterface, CommandOptions


class TemplateCommand(Command, OnMessageInterface, OnReactionAddInterface, OnReactionRemoveInterface):
    def __init__(self, client, command_options: CommandOptions, **kwargs):
        Command.__init__(self, client, command_options)

    async def on_message(self, message, has_prefix: bool, command: str, *args, **kwargs):
        pass

    async def on_reaction_add(self, reaction, user, *args, **kwargs):
        pass

    async def on_reaction_remove(self, reaction, user, *args, **kwargs):
        pass
