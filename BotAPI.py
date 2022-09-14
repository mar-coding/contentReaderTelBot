from module.config import TEL_HASH, TEL_ID
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
    UserNotParticipantError,
)

from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest


BOT_ADMIN = {
    'id': 1430850866,
    'title': "Amin",
}

channels = []
client = TelegramClient('main', TEL_ID, TEL_HASH)
my_keyword = []
my_target = None


@client.on(events.NewMessage)
async def my_test(event):
    """
    just test method to check bot is ready.
    """
    if re.match(r'(?i).*(hello)$', event.raw_text, re.IGNORECASE):
        user = PeerUser((await event.message.get_sender()).id)
        user = await client.get_entity(user)
        await event.reply('Hello {}, This is test.'.format(user.first_name))


@client.on(events.NewMessage)
async def commands(event):
    """
    it handles the command that we type and check if command
    send from admin answer them and provide controlling on 
    on our bot
    """
    cmd_msg = ""
    msgs = event.raw_text.split('\n')
    try:
        chat = await client.get_entity(PeerChat((await event.message.get_chat())).chat_id)
        # check whether sender is admin or not
        if chat.id == BOT_ADMIN['id']:
            # add channel to automatically listen for new posts
            # check ":add ch:" has sended from admin
            cmd_msg = msgs[0]
            if cmd_msg != None and ":add ch:".lower() in cmd_msg.lower():
                if len(msgs) == 1:
                    await event.reply('🙂Empty list.🙂')
                else:
                    tmp = await event.reply('⏳Checking channel link...⏳')
                    res = ''
                    async with client.action(chat, 'typing'):
                        # loop on the list of channel that send from admin
                        # check if they are joinable then join them and finally
                        # add them to "channels" list
                        for i, item in zip(range(len(msgs)), msgs[1:len(msgs)]):
                            try:
                                channel = await client.get_entity(item)
                                if await client(JoinChannelRequest(channel)):
                                    res += '✅Successful joining on channel ({})'.format(
                                        channel.title, i + 1) + '\n'
                                if re.findall(r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', item):
                                    channels.append(
                                        (channel.id, item, channel.title))
                                else:
                                    if "@" in item:
                                        item = item.replace("@", "")
                                    channels.append(
                                        (channel.id, 'https://t.me/' + item, channel.title))
                                await client(JoinChannelRequest(channel))
                            except UsernameInvalidError:
                                res += '❌Joining on link ({}th) failed. Username not found.\n'.format(
                                    i+1)
                            except ValueError:
                                res += '❌Joining on link ({}th) failed. Channel not found.\n'.format(
                                    i+1)
                            except TypeError:
                                res += '❌Joining on link ({}th) failed. Enter only channel link.\n'.format(
                                    i+1)
                    await client.delete_messages(chat, tmp)
                    await client.send_message(chat, res, reply_to=event.message)

            # send list of channel to chat
            # check ":list ch:" has sended from admin
            elif cmd_msg != None and ":list ch:".lower() in cmd_msg.lower():
                try:
                    tmp = await event.reply('⏳Checking list of channels...⏳')
                    res = ''
                    async with client.action(chat, 'typing'):
                        # gather all the name and link of channel
                        # then send them to chat
                        for ch in channels:
                            res += 'Channel name: {}\nChannel link: {}\n ---------- \n'.format(
                                ch[2], ch[1])
                    await client.delete_messages(chat, tmp)
                    await client.send_message(chat, res, reply_to=event.message)
                except ValueError:
                    res += '❌Channel list is empty.❌'
                    await client.send_message(chat, res)

            # check the link that admin send and then
            # leave them and show the results.
            elif cmd_msg != None and ":rem ch:".lower() in cmd_msg.lower():
                if len(msgs) == 1:
                    await event.reply('🙂Empty list.🙂')
                else:
                    res = ''
                    for i, item in zip(range(len(msgs)), msgs[1:len(msgs)]):
                        try:
                            channel = await client.get_entity(item)
                            if await client(LeaveChannelRequest(channel)):
                                res += '✅Successful leaving from link ({})'.format(
                                    channel.title, i + 1) + '\n'
                            if re.findall(r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', item):
                                channels.remove(
                                    (channel.id, item, channel.title))
                            else:
                                if "@" in item:
                                    item = item.replace("@", "")
                                channels.remove(
                                    (channel.id, 'https://t.me/' + item, channel.title))
                        except UsernameInvalidError:
                            res += '❌leaving from link ({}th) failed. Username not found.\n'.format(
                                i+1)
                        except ValueError:
                            res += '❌leaving from link ({}th) failed. Channel not found.\n'.format(
                                i+1)
                        except TypeError:
                            res += '❌leaving from link ({}th) failed. Enter only channel link.\n'.format(
                                i+1)
                        except UserNotParticipantError:
                            res += '❌leaving from link ({}th) failed. You are not member of this channel.\n'.format(
                                i+1)
                await event.reply(res)

            # check the keyword that admin send
            # and add them to "my_keyword"
            elif cmd_msg != None and ":add key:".lower() in cmd_msg.lower():
                if len(msgs) == 1:
                    await event.reply('🙂Empty list.🙂')
                else:
                    # TODO: solve the problem of is_en method
                    # remove command msg from keyword list
                    msgs.remove(msgs[0])
                    for kw in msgs[:len(msgs)]:
                        # to handel all keyword without thinking about
                        # they are persion or english
                        # if is_en(kw):
                        #     my_keyword.append(kw.lower())
                        # else:
                        my_keyword.append(kw)
                    await event.reply('✅Successful adding keywords.')

            # check the keyword that admin send
            # and remove them and show the result
            elif cmd_msg != None and ":rem key:".lower() in cmd_msg.lower():
                res = '❌These keywords not found:\n'
                error_flag = False
                if len(msgs) == 1:
                    await event.reply('🙂Empty list.🙂')
                else:
                    for kw in msgs[:len(msgs)]:
                        if kw in my_keyword:
                            my_keyword.remove(kw)
                        else:
                            res += "-{} \n".format(kw)
                            error_flag = True
                    if error_flag:
                        print(res)
                    await event.reply('✅Successful removing keywords.')

            # send list of keyword to chat
            # check ":list ch:" has sended from admin
            elif cmd_msg != None and ":list key:".lower() in cmd_msg.lower():
                try:
                    tmp = await event.reply('⏳Checking list of keywords...⏳')
                    res = ''
                    async with client.action(chat, 'typing'):
                        # gather all the keywords
                        # then send them to chat
                        for i, key in enumerate(my_keyword):
                            res += 'keyword {}: {}\n'.format(i, key)
                    await client.delete_messages(chat, tmp)
                    await client.send_message(chat, res, reply_to=event.message)
                except ValueError:
                    res += '❌Keyword list is empty.❌'
                    await client.send_message(chat, res)

            # adding and updating channel
            elif cmd_msg != None and ":add target:".lower() in cmd_msg.lower():
                if len(msgs) == 1:
                    await event.reply('🙂Empty list.🙂')
                else:
                    t = msgs[1]
                    global my_target
                    if my_target is None:
                        entity = await client.get_entity(t)
                        my_target = entity
                        await event.reply('✅Successful adding target.')
                    else:
                        entity = await client.get_entity(t)
                        my_target = entity
                        await event.reply('✅Successful updating target.')

    except ChatIdInvalidError:
        pass
    except AttributeError:
        await event.reply('❗️access out of bounds❗️ \n')


@client.on(events.NewMessage)
async def post_checker(event):
    """
    check the post of specific channels and compare 
    them with our keywords then forward them to our
    specific target.
    """
    msgs = event.raw_text
    try:
        ch = PeerChannel((await event.message.get_sender()).id)
        ch = await client.get_entity(ch)
        # check if sender of msg is in our specific list
        # of listening channel and then check for keywords.
        if any(item[0] == ch.id for item in channels):
            find_flag = False
            for key in my_keyword:
                if key in event.raw_text:
                    find_flag = True
                    break
            if find_flag:
                if my_target is not None:
                    entity = my_target
                    await client.forward_messages(entity, event.message)
    except ValueError:
        pass

if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
    client.disconnect()
