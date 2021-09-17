import discord
import inspect
from jujube.commands.command import Command, CommandOptions, OnMessageInterface
from jujube.commands import split_arguments
from jujube.app_config import GlobalLanguageConfig, GlobalAppConfig
from jujube.enums.color import Color
from jujube.utils.debug.logging import log

_COMMAND_TRACKER_MODULE = 'jujube.commands.command_tracker'
_COMMAND_TRACKER_CLASS = 'CommandTracker'


class HelpCommand(Command, OnMessageInterface):
    def __init__(self, client, command_options: CommandOptions):
        Command.__init__(self, client, command_options)

    @property
    def localized_name(self):
        return self._loc.commands.cmd_help_command_name

    @property
    def localized_long_desc(self):
        return self._loc.commands.commands.cmd_help_long_desc

    @property
    def localized_short_desc(self):
        return self._loc.commands.cmd_help_short_desc

    async def on_message(self, message, *args, **kwargs):
        commands = self.client.commands.get_commands(False)
        command_help: Command = None
        print(args)
        if args:
            for command in commands:
                if args[0] in command.params.commands:
                    command_help = command

        if command_help is None:
            embed_msg = discord.Embed(color=Color.INDIGO)
            for command in commands:
                if not command.params.enabled or command.params.hidden:
                    continue
                embed_msg.add_field(name=f'{GlobalAppConfig().prefix}[{", ".join(command.params.commands)}] {command.params.expected_args}', value="test", inline=False)
        else:
            embed_msg = discord.Embed(title=command_help.command_template, description=command_help.localized_long_desc, color=Color.INDIGO)
            sig = inspect.signature(command_help.on_message)
            for k, v in command_help.localized_params.items():
                embed_msg.add_field(name=k, value=v, inline=False)

        if message.guild.id == 428918656697892885:
            await message.channel.send(embed=embed_msg)
        else:
            await message.author.send(embed=embed_msg)
        await message.channel.send(GlobalLanguageConfig().localization['Commands']['HelpCommandNotifyUser'].format(message.author.id))
