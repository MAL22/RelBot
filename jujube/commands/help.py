import discord
from jujube.utils.logging import log
from jujube.commands.commands import Commands
from jujube.commands import split_arguments

commands = Commands()


async def on_message(client, message: discord.Message):
    try:
        contains_prefix, command, args = split_arguments(message.content)
        command_help = commands.get_command(args[0])
    except IndexError as e:
        embed_msg = discord.Embed()
        for command in commands.get_commands(refer_by_alias=False):
            print(command)
            embed_msg.add_field(name=f'({", ".join(command.params.commands)}) {command.params.expected_args}', value='lol' , inline=False)
        await message.channel.send(embed=embed_msg)
    else:
        embed_msg = discord.Embed()
        embed_msg = discord.Embed(title=command_help.command_template, description=command_help.long_desc)
        for _, param in command_help.arguments_metadata.required_arguments.items():
            embed_msg.add_field(name=param['display_name'], value=param['description'], inline=False)
        for _, param in command_help.arguments_metadata.optional_arguments.items():
            embed_msg.add_field(name=param['display_name'], value=param['description'], inline=False)
        await message.channel.send(embed=embed_msg)
