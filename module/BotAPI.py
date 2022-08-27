from module.config import TEL_HASH,TEL_ID

import re

import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import (
    PeerChannel,
    PeerUser,
    PeerChat,
)

# TEL_ID = os.environ.get('TEL_ID')
# TEL_HASH = os.environ.get('TEL_HASH')


TARGET = '@Mohammad_Amin_R'
INPUT_CHANNEL = 'me'
FILTER = ['Python', 'python', 'PYTHON', 'پایتون', 'security', 'Security', 'SECURITY', 'network', 'NETWORK', 'Network',
          'امنیت', 'شبکه']

client = TelegramClient('main', TEL_ID, TEL_HASH)


async def main():
    # Getting information about yourself
    me = await client.get_me()

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    username = me.username
    print(username)
    print(me.phone)

    # You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

    # You can send messages to yourself...
    await client.send_message('me', 'Hello, myself!')
    # ...to some chat ID
    await client.send_message('@Mohammad_Amin_R', 'Testing Telethon!')

    # You can, of course, use markdown in your messages:
    message = await client.send_message(
        'me',
        'This message has **bold**, `code`, __italics__ and '
        'a [nice website](https://example.com)!',
        link_preview=False
    )

    # Sending a message returns the sent message object, which you can use
    print(message.raw_text)

    # You can reply to messages directly if you have a message object
    await message.reply('Cool!')

    # Or send files, songs, documents, albums...
    await client.send_file('me', 'media/test.png')

    # You can print the message history of any chat:
    async for message in client.iter_messages('me'):
        print(message.id, message.text)

        # You can download media from messages, too!
        # The method will return the path where the file was saved.
        if message.photo:
            path = await message.download_media()
            print('File saved to', path)  # printed after download is done

# @client.on(events.NewMessage(chats=INPUT_CHANNEL))
# async def new_msg_listener(events):
#         # get msg text
#         new_msg = event.message.message
#         filtred_msg = re.findall(
#             r"(?=(" + '|'.join(FILTER) + r"))", new_msg, re.IGNORECASE)
#         if len(filtred_msg) != 0:
#             await self.client.forward_messages(entity=TARGET, messages=event.message)

@client.on(events.NewMessage)
async def my_event_handler(event):
    if re.match(r'(?i).*(hello)$', event.raw_text, re.IGNORECASE):
        user = PeerUser((await event.message.get_sender()).id)
        user = await client.get_entity(user)
        await event.reply('سلام{}, من ربات بررسی چنل های شما هستم'.format(user.first_name))


with client:
    # client.loop.run_until_complete(main())
    # client.run_until_disconnected(new_msg_listener())
    client.run_until_disconnected()
