import discord
import importlib
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

    async def on_message(self, message, has_prefix: bool, command: str, *args, **kwargs):
        commands = self.client.commands.get_commands(False)
        command_help = None
        if args:
            command_help = commands[args[0]]

        if command_help is None:
            embed_msg = discord.Embed(color=Color.INDIGO)
            for command in commands:
                if not command.params.enabled or command.params.hidden:
                    continue
                embed_msg.add_field(name=f'{GlobalAppConfig().prefix}[{", ".join(command.params.commands)}] {command.params.expected_args}', value="test", inline=False)
        else:
            embed_msg = discord.Embed(title=command_help.command_template, description=command_help.long_desc, color=Color.INDIGO)
            for _, param in command_help.arguments_metadata.required_arguments.items():
                embed_msg.add_field(name=param['display_name'], value=param['description'], inline=False)
            for _, param in command_help.arguments_metadata.optional_arguments.items():
                embed_msg.add_field(name=param['display_name'], value=param['description'], inline=False)

        await message.author.send(embed=embed_msg)
        await message.channel.send(GlobalLanguageConfig().config['Commands']['HelpCommandNotifyUser'].format(message.author.id))

    async def on_error(self, message, error):
        embed_msg = discord.Embed(title=str(error), description='{0}'.format(self.command_template))
        for _, param in self.arguments_metadata.required_arguments.items():
            embed_msg.add_field(name=param['display_name'], value=param['description'], inline=False)
        for _, param in self.arguments_metadata.optional_arguments.items():
            embed_msg.add_field(name=param['display_name'], value=param['description'], inline=False)
        await message.channel.send(embed=embed_msg)
