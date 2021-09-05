import urllib.request
import discord
from jujube.enums.color import Color
from jujube.utils.debug.logging import log
from jujube.commands.command import Command, OnMessageInterface, CommandOptions


class MinecraftServerInfo(Command, OnMessageInterface):
    def __init__(self, client, command_options: CommandOptions, **kwargs):
        Command.__init__(self, client, command_options)

        self.ip_url = kwargs.pop('ip_url', None)
        if self.ip_url:
            self.ip = urllib.request.urlopen(self.ip_url).read().decode('utf8')
        else:
            self.ip = "127.0.0.1"
        self.mc_port = kwargs.pop('mc_port', 25565)

    async def on_message(self, message, has_prefix: bool, command: str, *args, **kwargs):
        if self.ip == "127.0.0.1":
            raise Exception('Invalid IP!')
        embed_msg = discord.Embed(title="Minecraft Server Info", color=Color.INDIGO)
        embed_msg.set_thumbnail(url='attachment://mc_logo.png')
        embed_msg.add_field(name="IP", value=self.ip, inline=True)
        embed_msg.add_field(name="Port", value=self.mc_port, inline=True)
        await message.channel.send(embed=embed_msg, file=discord.File('./assets/mc_logo.png', 'mc_logo.png'))
