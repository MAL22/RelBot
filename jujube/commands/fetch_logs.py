import os
import discord
from jujube.utils.debug.logging import log
from jujube.commands.command import Command, OnReactionRemoveInterface, OnReactionAddInterface, OnMessageInterface, \
    CommandOptions


class FetchLogs(Command, OnMessageInterface):

    folder_path = './logs/'

    def __init__(self, client, command_options: CommandOptions, **kwargs):
        Command.__init__(self, client, command_options)

    async def on_message(self, message, has_prefix: bool, command: str, *args, **kwargs):
        files = []
        for dirpath, dirnames, filenames in os.walk(os.path.realpath(self.folder_path)):
            for filename in filenames:
                if len(files) == 10:
                    break
                file_path = os.path.join(dirpath, filename)
                files.append(discord.File(file_path, filename))

        await message.author.send(files=files)
