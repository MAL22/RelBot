import discord
from relbot.commands.base_command import BaseCommand, ArgumentsMetadata
from relbot.commands import split_arguments
from relbot.app_config import GlobalLanguageConfig

_COMMAND_NAME = "Reputation"


class ReputationCommand(BaseCommand):
    def __init__(self, client):
        __required_args = {}
        __optional_args = {
            "name": {"display_name": GlobalLanguageConfig().config['Commands']['ReputationMemberParameterName'],
                     "description": GlobalLanguageConfig().config['Commands']['ReputationMemberParameterDesc']}
        }

        super().__init__(client, 'reputation',
                         GlobalLanguageConfig().config['Commands']['ReputationCommandName'],
                         GlobalLanguageConfig().config['Commands']['ReputationLongDesc'],
                         GlobalLanguageConfig().config['Commands']['ReputationShortDesc'],
                         arguments_metadata=ArgumentsMetadata(__required_args, __optional_args))
        self.positive_emoji: discord.Emoji = client.get_emoji(self._extra_parameters['positive_id'])
        self.negative_emoji: discord.Emoji = client.get_emoji(self._extra_parameters['negative_id'])
        self.long_desc = self.long_desc.format(positive_emoji=self.positive_emoji, negative_emoji=self.negative_emoji)

    async def execute(self, message):
        try:
            contains_prefix, command, args = split_arguments(message.content)
            user_id = await self._validate_args(message, *args)
        except ValueError as error:
            await self.on_error(message, error)
        else:
            print('Command: {} {}'.format(self._internal_name, user_id))
            user = self._database_manager.verify_user_exists(user_id)

            if user is None:
                self._database_manager.insert_user(user_id)
                user = self._database_manager.verify_user_exists(user_id)

            if self.positive_emoji is None or self.negative_emoji is None:
                raise ValueError(GlobalLanguageConfig().config['Errors']['emoji.missing'])

            embed_msg = discord.Embed(title=self._display_name, description='<@{0}>'.format(user[0]))
            embed_msg.set_thumbnail(url=self._client.get_user(user[0]).avatar_url)
            embed_msg.add_field(name=('<:{}:{}>'.format(self.positive_emoji.name, self.positive_emoji.id)),
                                value=user[1],
                                inline=True)
            embed_msg.add_field(name=('<:{}:{}>'.format(self.negative_emoji.name, self.negative_emoji.id)),
                                value=user[2],
                                inline=True)

            if self._remove_output:
                await message.channel.send(embed=embed_msg, delete_after=self._app_config['delay_before_deleting'])
                await message.delete(delay=self._app_config['delay_before_deleting'])
            else:
                await message.channel.send(embed=embed_msg)

    async def on_reaction_add(self, reaction, user):
        if user == reaction.message.author:
            return
        author = self._database_manager.verify_user_exists(reaction.message.author.id)

        if reaction.emoji.id == self.command_config['positive_id']:
            if author is None:
                self._database_manager.insert_user(reaction.message.author.id, positive_rep=1)
            else:
                self._database_manager.update_user(reaction.message.author.id, author[1] + 1, author[2])
        elif reaction.emoji.id == self.command_config['negative_id']:
            if author is None:
                self._database_manager.insert_user(reaction.message.author.id, negative_rep=1)
            else:
                self._database_manager.update_user(reaction.message.author.id, author[1], author[2] + 1)

    async def on_reaction_remove(self, reaction, user):
        if user == reaction.message.author:
            return
        author = self._database_manager.verify_user_exists(reaction.message.author.id)

        if reaction.emoji == self.command_config['positive_id']:
            if author is None:
                self._database_manager.insert_user(reaction.message.author.id, positive_rep=0)
            else:
                self._database_manager.update_user(reaction.message.author.id, author[1] - 1, author[2])

        elif reaction.emoji == self.command_config['negative_id']:
            if author is None:
                self._database_manager.insert_user(reaction.message.author.id, negative_rep=0)
            else:
                self._database_manager.update_user(reaction.message.author.id, author[1], author[2] - 1)

    def reload_config(self):
        pass

    async def on_error(self, message, error):
        embed_msg = discord.Embed(title=str(error), description='{0}'.format(self.command_template))
        for _, param in self.arguments_metadata.required_arguments.items():
            embed_msg.add_field(name=param['display_name'], value=param['description'], inline=False)
        for _, param in self.arguments_metadata.optional_arguments.items():
            embed_msg.add_field(name=param['display_name'], value=param['description'], inline=False)
        await message.channel.send(embed=embed_msg)

    async def _validate_args(self, message, *args):
        try:
            await super()._validate_args(message, *args)

            if not args:
                user_id = message.author.id
            else:
                user_id = int(args[0].strip('<@&!>'))

            if self._client.get_user(int(user_id)) is None:
                raise ValueError(self._language_config['Errors']['MemberNotPresent'])

            return user_id
        except ValueError as e:
            raise ValueError(self._language_config['Errors']['InvalidMemberID']) from e
        except SyntaxError as error:
            await self.on_error(message, error)
            raise SyntaxError(error) from None
