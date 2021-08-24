import discord


async def on_message(client: discord.Client, message: discord.Message):
    await message.channel.send('testing')


async def on_reaction_add(client: discord.Client, reaction: discord.Reaction, user: discord.User):
    await reaction.message.channel.send('testing')
