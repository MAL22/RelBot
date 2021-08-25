import discord


async def on_message(client, message: discord.Message):
    await message.channel.send('testing')
