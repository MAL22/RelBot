import discord
from relbot.commands import Command

_COMMAND_NAME = "reputation"
PARAMS_DEFINITION = {"required_params": [], "optional_params": [{"name": "user", "description": "Target user ID"}]}


class ReputationCommand(Command):
    def __init__(self, client):
        super().__init__(client, _COMMAND_NAME, required_params=PARAMS_DEFINITION['required_params'], optional_params=PARAMS_DEFINITION['optional_params'])

    async def verify(self, message):
        try:
            # args = await self._parse_args(message)
            return await self.execute(message)
        except Exception as error:
            await self.on_error(message, error)
            return None

    async def execute(self, message):
        user_id = await self._parse_args(message)
        if self.client.get_user(user_id) is None:
            raise ValueError('User is not present on this server')

        print('Command: {} {}'.format(self.name, user_id))
        user = self._database_manager.verify_user_exists(user_id)

        if user is None:
            self._database_manager.insert_user(user_id)
            user = self._database_manager.verify_user_exists(user_id)

        positive_emoji: discord.Emoji = self.client.get_emoji(self.params['positive_id'])
        negative_emoji: discord.Emoji = self.client.get_emoji(self.params['negative_id'])

        if positive_emoji is None or negative_emoji is None:
            raise ValueError("Emojis don't exist.")

        embed_msg = discord.Embed(title='Reputation', description='<@{0}>'.format(user[0]))
        embed_msg.set_thumbnail(url=self.client.get_user(user[0]).avatar_url)
        embed_msg.add_field(name=('<:{}:{}>'.format(positive_emoji.name, positive_emoji.id)), value=user[1],
                            inline=True)
        embed_msg.add_field(name=('<:{}:{}>'.format(negative_emoji.name, negative_emoji.id)), value=user[2],
                            inline=True)

        if self.automatic_removal:
            await message.channel.send(embed=embed_msg, delete_after=self._app_config['delay_before_deleting'])
            await message.delete(delay=self._app_config['delay_before_deleting'])
        else:
            await message.channel.send(embed=embed_msg)

    async def on_reaction_add(self, reaction, user):
        if user == reaction.message.author:
            return
        author = self._database_manager.verify_user_exists(reaction.message.author.id)

        if reaction.emoji.id == self.config['positive_id']:
            if author is None:
                self._database_manager.insert_user(reaction.message.author.id, positive_rep=1)
            else:
                self._database_manager.update_user(reaction.message.author.id, author[1] + 1, author[2])
        elif reaction.emoji.id == self.config['negative_id']:
            if author is None:
                self._database_manager.insert_user(reaction.message.author.id, negative_rep=1)
            else:
                self._database_manager.update_user(reaction.message.author.id, author[1], author[2] + 1)

    async def on_reaction_remove(self, reaction, user):
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
        for argument in self.required_params:
            embed_msg.add_field(name=argument['name'], value=argument['description'], inline=False)
        for argument in self.optional_params:
            embed_msg.add_field(name=argument['name'], value=argument['description'], inline=False)
        await message.channel.send(embed=embed_msg, delete_after=self._app_config['delay_before_deleting'])
        await message.delete(delay=self._app_config['delay_before_deleting'])

    async def _parse_args(self, message):
        try:
            args = await super()._parse_args(message)
            if len(args) == 0:
                return message.author.id
            return int(args[0].strip('<@!>'))
        except ValueError as error:
            await self.on_error(message, error)
            raise ValueError('Target user is not a numerical value.') from error
        except SyntaxError as error:
            await self.on_error(message, error)
            raise SyntaxError('Syntax error') from error
