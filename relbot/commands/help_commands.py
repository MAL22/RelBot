import discord
import importlib
from relbot.commands.base_command import BaseCommand, ArgumentsMetadata
from relbot.commands import split_arguments
from relbot.app_config import GlobalLanguageConfig

_COMMAND_TRACKER_MODULE = 'relbot.commands.command_tracker'
_COMMAND_TRACKER_CLASS = 'CommandTracker'


class HelpCommand(BaseCommand):
    def __init__(self, client):
        __required_args = {}
        __optional_args = {
            "name": {"display_name": GlobalLanguageConfig().config['Commands']['HelpCommandParameterName'],
                     "description": GlobalLanguageConfig().config['Commands']['HelpCommandParameterDesc']}
        }

        super().__init__(client, 'help',
                         GlobalLanguageConfig().config['Commands']['HelpCommandName'],
                         GlobalLanguageConfig().config['Commands']['HelpLongDesc'],
                         GlobalLanguageConfig().config['Commands']['HelpShortDesc'],
                         arguments_metadata=ArgumentsMetadata(required_arguments=__required_args, optional_arguments=__optional_args))
        __module = importlib.import_module(_COMMAND_TRACKER_MODULE)
        __class = getattr(__module, _COMMAND_TRACKER_CLASS)
        self.commands_tracker = __class()

    async def execute(self, message):
        try:
            contains_prefix, command, args = split_arguments(message.content)
            command_help = await self._validate_args(message, *args)
        except Exception as error:
            await self.on_error(message, error)
            raise Exception from error
        else:
            print(command_help)
            if command_help is None:
                embed_msg = discord.Embed()
                for name, command in self.commands_tracker.get_commands(refer_by_alias=False):
                    print(name, command)
                    embed_msg.add_field(name=command.command_template, value=command.long_desc, inline=False)
            else:
                embed_msg = discord.Embed(title=command_help.command_template, description=command_help.long_desc)
                for _, param in command_help.arguments_metadata.required_arguments.items():
                    embed_msg.add_field(name=param['display_name'], value=param['description'], inline=False)
                for _, param in command_help.arguments_metadata.optional_arguments.items():
                    embed_msg.add_field(name=param['display_name'], value=param['description'], inline=False)
            await message.channel.send(embed=embed_msg)

    async def on_reaction_add(self, reaction, user):
        pass

    async def on_reaction_remove(self, reaction, user):
        pass

    def reload_config(self):
        pass

    async def on_error(self, message, error):
        embed_msg = discord.Embed(title=str(error), description='{0}'.format(self.command_template))
        for _, param in self.arguments_metadata.required_arguments.items():
            embed_msg.add_field(name=param['display_name'], value=param['description'], inline=False)
        for _, param in self.arguments_metadata.optional_arguments.items():
            embed_msg.add_field(name=param['display_name'], value=param['description'], inline=False)
        await message.channel.send(embed=embed_msg)

    async def _validate_args(self, message, *args):
        try:
            await super()._validate_args(message, *args)
            command = self.commands_tracker.get_command(args[0])
            return command
        except ValueError as error:
            raise ValueError('Value error') from error
        except SyntaxError as error:
            raise SyntaxError('Syntax error') from error
        except IndexError:
            return None
