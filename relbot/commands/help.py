import discord


async def on_message(message: discord.Message):
    await message.channel.send('testing')


async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    await reaction.message.channel.send('testing')
