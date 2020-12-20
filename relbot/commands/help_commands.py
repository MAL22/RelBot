import discord
from relbot.commands import Command

REQUIRED_PARAMS = [],
OPTIONAL_PARAMS = [{"name": "user", "description": "Target user ID"}]


class HelpCommand(Command):
    def __init__(self, client):
        super().__init__(client, "help", required_params=REQUIRED_PARAMS, optional_params=OPTIONAL_PARAMS)

    async def verify(self, message):
        pass

    async def execute(self, message):
        pass

    async def on_reaction_add(self, reaction, user):
        pass

    async def on_reaction_remove(self, reaction, user):
        pass

    def reload_config(self):
        pass

    async def on_error(self, message, error):
        embed_msg = discord.Embed(title=str(error), description='{0}'.format(await self._build_cmd_template()))
        for argument in self.required_params:
            embed_msg.add_field(name=argument['name'], value=argument['description'], inline=False)
        for argument in self.optional_params:
            embed_msg.add_field(name=argument['name'], value=argument['description'], inline=False)
        await message.channel.send(embed=embed_msg, delete_after=self._app_config['delay_before_deleting'])
        await message.delete(delay=self._app_config['delay_before_deleting'])

    async def _parse_args(self, message):
        try:
            return await super()._parse_args(message)
        except ValueError as error:
            raise ValueError('Value error') from error
        except SyntaxError as error:
            raise SyntaxError('Syntax error') from error
