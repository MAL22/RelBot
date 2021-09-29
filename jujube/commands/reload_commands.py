from jujube.commands.command import Command, OnMessageInterface, CommandOptions


class ReloadCommands(Command, OnMessageInterface):
    def __init__(self, client, command_options: CommandOptions, **kwargs):
        Command.__init__(self, client, command_options)

    async def on_message(self, message, *args, **kwargs):
        from jujube.commands.commands import Commands
        Commands().reload_commands()
