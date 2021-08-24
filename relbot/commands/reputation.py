import discord


async def on_message(client: discord.Client, message: discord.Message):
    await message.channel.send('testing')
