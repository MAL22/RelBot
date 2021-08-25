import discord
import relbot.json.json_reader as json_reader
from relbot.database.database_manager import DatabaseManager

database_manager = DatabaseManager()
command_config = json_reader.read('./commands/reputation.json')


async def on_message(message: discord.Message):
    await message.channel.send('testing')


async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    if user == reaction.message.author:
        return
    author = database_manager.verify_user_exists(reaction.message.author.id)

    if reaction.emoji.id == command_config['parameters']['positive_id']:
        if author is None:
            database_manager.insert_user(reaction.message.author.id, positive_rep=1)
        else:
            database_manager.update_user(reaction.message.author.id, author[1] + 1, author[2])
    elif reaction.emoji.id == command_config['parameters']['negative_id']:
        if author is None:
            database_manager.insert_user(reaction.message.author.id, negative_rep=1)
        else:
            database_manager.update_user(reaction.message.author.id, author[1], author[2] + 1)


async def on_reaction_remove(reaction: discord.Reaction, user: discord.User):
    if user == reaction.message.author:
        return
    author = database_manager.verify_user_exists(reaction.message.author.id)

    if reaction.emoji.id == command_config['parameters']['positive_id']:
        if author is None:
            database_manager.insert_user(reaction.message.author.id, positive_rep=1)
        else:
            database_manager.update_user(reaction.message.author.id, author[1] - 1, author[2])
    elif reaction.emoji.id == command_config['parameters']['negative_id']:
        if author is None:
            database_manager.insert_user(reaction.message.author.id, negative_rep=1)
        else:
            database_manager.update_user(reaction.message.author.id, author[1], author[2] - 1)
