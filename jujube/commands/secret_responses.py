from jujube.commands.base_command import BaseCommand


class SecretResponses(BaseCommand):
    def __init__(self, client):
        BaseCommand.__init__(client)
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
