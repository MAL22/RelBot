import discord


async def on_message(message: discord.Message):
    await message.channel.send('testing')
