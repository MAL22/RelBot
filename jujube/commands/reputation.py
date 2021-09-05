import discord
from jujube.commands.command import Command, OnMessageInterface, OnReactionAddInterface, OnReactionRemoveInterface, \
    CommandOptions
from jujube.app_config import GlobalLanguageConfig
from jujube.database.database_manager import DatabaseManager
from jujube.utils.debug.logging import log


class ReputationCommand(Command, OnMessageInterface, OnReactionAddInterface, OnReactionRemoveInterface):
    def __init__(self, client, command_options: CommandOptions, **kwargs):
        Command.__init__(self, client, command_options)
        self.positive_emoji = self.fetch_emoji(kwargs.pop('emoji_positive', None))
        self.negative_emoji = self.client.get_emoji(kwargs.pop('emoji_negative', None))

    async def on_message(self, message, has_prefix: bool, command: str, *args, **kwargs):
        try:
            if not args:
                user_id = message.author.id
            else:
                user_id = int(args[0].strip('<@!>'))
        except ValueError as error:
            log(error)
        else:
            if not self.client.get_user(user_id):
                return

            print('Command: {} {}'.format(command, user_id))
            user = DatabaseManager().verify_user_exists(user_id)

            if user is None:
                DatabaseManager().insert_user(user_id)
                user = DatabaseManager().verify_user_exists(user_id)

            if self.positive_emoji is None or self.negative_emoji is None:
                raise ValueError(GlobalLanguageConfig().config['Errors']['emoji.missing'])

            embed_msg = discord.Embed(title=GlobalLanguageConfig().config['Commands']['ReputationCommandName'], description='<@{0}>'.format(user[0]))
            embed_msg.set_thumbnail(url=self.client.get_user(user[0]).avatar_url)
            embed_msg.add_field(name=('<:{}:{}>'.format(self.positive_emoji.name, self.positive_emoji.id)),
                                value=user[1],
                                inline=True)
            embed_msg.add_field(name=('<:{}:{}>'.format(self.negative_emoji.name, self.negative_emoji.id)),
                                value=user[2],
                                inline=True)
            await message.channel.send(embed=embed_msg)

    async def on_reaction_add(self, reaction, user, *args, **kwargs):
        if user == reaction.message.author:
            return
        author = DatabaseManager().verify_user_exists(reaction.message.author.id)

        if reaction.emoji is self.positive_emoji:
            if author is None:
                DatabaseManager().insert_user(reaction.message.author.id, positive_rep=1)
            else:
                DatabaseManager().update_user(reaction.message.author.id, author[1] + 1, author[2])
        elif reaction.emoji == self.negative_emoji:
            if author is None:
                DatabaseManager().insert_user(reaction.message.author.id, negative_rep=1)
            else:
                DatabaseManager().update_user(reaction.message.author.id, author[1], author[2] + 1)

    async def on_reaction_remove(self, reaction, user, *args, **kwargs):
        if user == reaction.message.author:
            return
        author = DatabaseManager().verify_user_exists(reaction.message.author.id)

        if reaction.emoji is self.positive_emoji:
            if author is None:
                DatabaseManager().insert_user(reaction.message.author.id, positive_rep=1)
            else:
                DatabaseManager().update_user(reaction.message.author.id, author[1] - 1, author[2])
        elif reaction.emoji == self.negative_emoji:
            if author is None:
                DatabaseManager().insert_user(reaction.message.author.id, negative_rep=1)
            else:
                DatabaseManager().update_user(reaction.message.author.id, author[1], author[2] - 1)

    def fetch_emoji(self, raw_emoji):
        if isinstance(raw_emoji, int):
            return self.client.get_emoji(raw_emoji)
        try:
            return self.client.get_emoji(int(raw_emoji))
        except ValueError as error:
            """ If this exception is triggered then the emoji is most likely a unicode emoji. """
            return raw_emoji
        except Exception as error:
            """ Handle any unexpected errors. E.g. emoji doesn't exist """
            log(error)
            return None

