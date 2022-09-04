from config import TEL_HASH, TEL_ID

import re

import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import (
    PeerChannel,
    PeerUser,
    PeerChat,
)

from telethon.errors.rpcerrorlist import (
    MessageAuthorRequiredError,
    ChatIdInvalidError,
    MessageIdInvalidError,
    UsernameInvalidError,
)

from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest


TARGET = '@Mohammad_Amin_R'
BOT_ADMIN = {
    'id': 1430850866,
    'title': "Amin",
}
FILTER = ['Python', 'python', 'PYTHON', 'پایتون', 'security', 'Security', 'SECURITY', 'network', 'NETWORK', 'Network',
          'امنیت', 'شبکه']

channels = []
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


@client.on(events.NewMessage)
async def my_test(event):
    if re.match(r'(?i).*(hello)$', event.raw_text, re.IGNORECASE):
        user = PeerUser((await event.message.get_sender()).id)
        user = await client.get_entity(user)
        await event.reply('Hello {}, This is test.'.format(user.first_name))


@client.on(events.NewMessage)
async def commands(event):
    cmd_msg = ""
    msgs = event.raw_text.split('\n')
    try:
        chat = await client.get_entity(PeerChat((await event.message.get_chat())).chat_id)
        # check whether sender is admin or not
        if chat.id == BOT_ADMIN['id']:
            # add channel to automatically listen for new posts
            # check "add ch" has sended from admin
            # if re.findall(r'(?i)add[ ]*ch$', event.raw_text):
            cmd_msg = msgs[0]
            if cmd_msg != None and "add ch".lower() in cmd_msg.lower():
                if len(msgs) == 1:
                    await event.reply('🙂Empty list.🙂')
                else:
                    tmp = await event.reply('⏳Checking channel link...⏳')
                    res = ''
                    async with client.action(chat, 'typing'):
                        for i, item in zip(range(len(msgs)), msgs[1:len(msgs)]):
                            try:
                                channel = await client.get_entity(item)
                                if await client(JoinChannelRequest(channel)):
                                    res += '✅Successful joining on link ({})'.format(
                                        channel.title, i + 1) + '\n'
                                if re.findall(r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', item):
                                    channels.append(
                                        (channel.id, item, channel.title))
                                else:
                                    channels.append(
                                        (channel.id, 'https://t.me/' + item, channel.title))
                                await client(JoinChannelRequest(channel))
                            except UsernameInvalidError:
                                res += '❌Joining on link ({}) failed. Username not found.\n'.format(
                                    i+1)
                            except ValueError:
                                res += '❌Joining on link ({}) failed. Channel not found.\n'.format(
                                    i+1)
                            except TypeError:
                                res += '❌Joining on link ({}) failed. Enter only channel link.\n'.format(
                                    i+1)
                    await client.delete_messages(chat, tmp)
                    await client.send_message(chat, res, reply_to=event.message)
            elif cmd_msg != None and "list ch".lower() in cmd_msg.lower():
                await client.send_message(chat, channels)
    except ChatIdInvalidError:
        pass
    except AttributeError:
        await event.reply('❗️access out of bounds❗️ \n')


with client:
    # client.loop.run_until_complete(main())
    # client.run_until_disconnected(new_msg_listener())
    client.run_until_disconnected()
