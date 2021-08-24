# from relbot.commands.hidden_command import HiddenCommand
from relbot.commands.base_command import BaseCommand


class SecretResponses(BaseCommand):
    def __init__(self, client):
        super().__init__(client, 'secret_responses', '', '', '', hidden=True)
        self._last_message = {}

    async def on_message(self, message):
        if message.content != '':
            if message.channel.id not in self._last_message:
                print(f'Adding message #{message.id} to entry for channel #{message.channel.id}')
                self._last_message[message.channel.id] = (message, 1)
            else:
                previous_message, streak = self._last_message[message.channel.id]
                if previous_message.content == message.content:
                    streak += 1
                    self._last_message[message.channel.id] = (message, streak)
                    if streak == 3:
                        await message.channel.send(message.content)
                        del self._last_message[message.channel.id]
                else:
                    print(f'replacing entry for channel #{message.channel.id} with message #{message.id}')
                    self._last_message[message.channel.id] = (message, 1)
                del previous_message, streak

            if 'ayy' in message.content:
                await message.channel.send('lmao')

    async def on_reaction_add(self, reaction, user):
        pass

    async def on_reaction_remove(self, reaction, user):
        pass

    async def on_error(self, message, error):
        pass

    async def _validate_args(self, message, *args):
        pass

    def reload_config(self):
        pass
