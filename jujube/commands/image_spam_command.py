import discord
from jujube.utils.timer import Timer
from jujube.commands.command import Command,  OnMessageInterface, CommandOptions


class UserInfractionInfo:
    def __init__(self):
        self.infraction_score = 26
        self.warning_issued = False
        self.flagged_messages = []


class ImageSpamCommand(Command, OnMessageInterface):
    def __init__(self, client, command_options: CommandOptions, **kwargs):
        Command.__init__(self, client, command_options)

        self._channel_blocklist = kwargs.pop('blocklist', [])
        self._content_blocklist = kwargs.pop('content_blocklist', [])
        self.channels = dict.fromkeys(self._channel_blocklist, {})

    @property
    def localized_name(self):
        return ""

    @property
    def localized_long_desc(self):
        return ""

    @property
    def localized_short_desc(self):
        return ""

    async def on_message(self, message, *args, **kwargs):
        if message.channel.id not in self._channel_blocklist:
            return

        if message.author.id not in self.channels[message.channel.id]:
            print(f'Added user {message.author.id} to channel {message.channel.id}')
            self.channels[message.channel.id] = {message.author.id: UserInfractionInfo()}
        print(self.channels[message.channel.id])

        infraction_info: UserInfractionInfo = self.channels[message.channel.id][message.author.id]

        if not message.attachments:
            if infraction_info.infraction_score > 0:
                infraction_info.infraction_score -= 1
                print(f'Decremented infraction count of user {message.author.id}: {infraction_info.infraction_score}')
                if infraction_info.infraction_score < 25:
                    infraction_info.warning_issued = False

        for attachment in message.attachments:
            if attachment.content_type in self._content_blocklist:
                infraction_info.infraction_score += 5
                infraction_info.flagged_messages.append(message.id)
                print(f'Incremented infraction count for {message.author.id}: {infraction_info.infraction_score}')

        if infraction_info.infraction_score >= 25:
            if not infraction_info.warning_issued:
                await message.channel.send(f'<@!{message.author.id}> You have sent too many images recently. Any subsequent images will be removed.')
                infraction_info.warning_issued = True
            for message_id in infraction_info.flagged_messages:
                msg = await message.channel.fetch_message(message_id)
                await msg.delete()
            print('starto')
            t = Timer(5.0, test, False, message.channel)

            infraction_info.flagged_messages = []


async def test(self, channel):
    await channel.send('donezo!')
