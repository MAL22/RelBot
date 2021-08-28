import discord
import os
import jujube.json.json_reader as json_reader
from jujube.utils.debug.logging import log
from jujube.commands import split_arguments
from jujube.app_config import GlobalLanguageConfig
from jujube.database.database_manager import DatabaseManager

database_manager = DatabaseManager()
command_config = json_reader.read(os.path.realpath('./jujube/json/commands/reputation.json'))


async def on_message(client: discord.Client, message: discord.Message, *args):
    positive_emoji: discord.Emoji = client.get_emoji(command_config['parameters']['positive_id'])
    negative_emoji: discord.Emoji = client.get_emoji(command_config['parameters']['negative_id'])

    try:
        has_prefix, command, args = split_arguments(message.content)

        if not args:
            user_id = message.author.id
        else:
            user_id = int(args[0].strip('<@&!>'))

    except ValueError as e:
        log(__name__, e)
    else:
        log('Command: {} {}'.format("reputation", user_id))
        user = database_manager.verify_user_exists(user_id)

        if user is None:
            database_manager.insert_user(user_id)
            user = database_manager.verify_user_exists(user_id)

        if positive_emoji is None or negative_emoji is None:
            raise ValueError(GlobalLanguageConfig().config['Errors']['ReputationEmojisMissing'])

        embed_msg = discord.Embed(title=GlobalLanguageConfig().config['Commands']['ReputationCommandName'], description='<@{0}>'.format(user[0]))
        embed_msg.set_thumbnail(url=client.get_user(user[0]).avatar_url)
        embed_msg.add_field(name=('<:{}:{}>'.format(positive_emoji.name, positive_emoji.id)), value=user[1], inline=True)
        embed_msg.add_field(name=('<:{}:{}>'.format(negative_emoji.name, negative_emoji.id)), value=user[2], inline=True)
        await message.channel.send(embed=embed_msg)


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
