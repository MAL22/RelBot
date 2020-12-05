import discord
from relbot.commands import Command, ErrorType

CFG_FILENAME = "reputation.json"


class ReputationCommand(Command):
    def __init__(self, client):
        super().__init__(client, CFG_FILENAME)

    async def verify(self, message):
        print('Validating {}...'.format(self.name))
        try:
            args = await self._parse_args(message)
            return await self.execute(message, *args)
        except Exception as e:
            await self.on_error(message, e)
            return None

    async def execute(self, message, *args):
        try:
            if len(args) == 0:
                user_id = int(message.author.id)
            else:
                user_id = int(args[0].strip('<@!>'))
        except ValueError as e:
            raise ValueError(ErrorType.InvalidArguments)

        if self.client.get_user(user_id) is None:
            raise ValueError(ErrorType.InvalidArguments)

        print('Command: {} {}'.format(self.name, user_id))
        user = self._database_manager.verify_user_exists(user_id)

        if user is None:
            self._database_manager.insert_user(user_id)
            user = self._database_manager.verify_user_exists(user_id)

        positive_emoji: discord.Emoji = self.client.get_emoji(self.config['positive_id'])
        negative_emoji: discord.Emoji = self.client.get_emoji(self.config['negative_id'])

        if positive_emoji is None or negative_emoji is None:
            raise ValueError(ErrorType.InvalidArguments)

        embed_msg = discord.Embed(title='Reputation', description='<@{0}>'.format(user[0]))
        embed_msg.set_thumbnail(url=self.client.get_user(user[0]).avatar_url)
        embed_msg.add_field(
            name=('<:{}:{}>'.format(positive_emoji.name, positive_emoji.id)),
            value=user[1],
            inline=True
        )
        embed_msg.add_field(
            name=('<:{}:{}>'.format(negative_emoji.name, negative_emoji.id)),
            value=user[2],
            inline=True
        )

        if self.automatic_removal:
            await message.channel.send(embed=embed_msg, delete_after=self._app_config['delay_before_deleting'])
            await message.delete(delay=self._app_config['delay_before_deleting'])
        else:
            await message.channel.send(embed=embed_msg)

    def on_reaction_add(self, reaction, user):
        if user == reaction.message.author:
            return
        author = self._database_manager.verify_user_exists(reaction.message.author.id)

        if reaction.emoji.id == self.config['positive_id']:
            if author is None:
                self._database_manager.insert_user(reaction.message.author.id, positive_rep=1)
            else:
                self._database_manager.update_user(reaction.message.author.id, author[1] + 1, author[2])
        elif reaction.emoji.id != self.config['negative_id']:
            if author is None:
                self._database_manager.insert_user(reaction.message.author.id, negative_rep=1)
            else:
                self._database_manager.update_user(reaction.message.author.id, author[1], author[2] + 1)

    def on_reaction_remove(self, reaction, user):
        if user == reaction.message.author:
            return
        author = self._database_manager.verify_user_exists(reaction.message.author.id)

        if reaction.emoji == self.config['positive_id']:
            if author is None:
                self._database_manager.insert_user(reaction.message.author.id, positive_rep=0)
            else:
                self._database_manager.update_user(reaction.message.author.id, author[1] - 1, author[2])

        elif reaction.emoji == self.config['negative_id']:
            if author is None:
                self._database_manager.insert_user(reaction.message.author.id, negative_rep=0)
            else:
                self._database_manager.update_user(reaction.message.author.id, author[1], author[2] - 1)

    def reload_config(self):
        pass

    async def on_error(self, message, error):
        embed_msg = discord.Embed(title=str(error), description='{0}'.format(self.template))
        for argument in self.required_args:
            embed_msg.add_field(name=argument['name'], value=argument['description'], inline=False)
        for argument in self.optional_args:
            embed_msg.add_field(name=argument['name'], value=argument['description'], inline=False)
        await message.channel.send(embed=embed_msg, delete_after=self._app_config['delay_before_deleting'] * 5)
        await message.delete(delay=self._app_config['delay_before_deleting'] * 5)
