from jujube.app_config import GlobalLanguageConfig
from jujube.utils.debug.logging import log
from jujube.commands.command import Command, OnReactionRemoveInterface, OnReactionAddInterface, OnMessageInterface, CommandOptions


class TemplateCommand(Command, OnMessageInterface, OnReactionAddInterface, OnReactionRemoveInterface):
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

    async def on_message(self, message, *args, **kwargs):
        pass

    async def on_reaction_add(self, reaction, user, *args, **kwargs):
        pass

    async def on_reaction_remove(self, reaction, user, *args, **kwargs):
        pass
