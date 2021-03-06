# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ Commands Available -

• `{i}addai <reply to user/give username/userid>`
   Add a AI ChatBot to reply to that user.

• `{i}remai <reply to user/give username/userid>`
   Remove the AI ChatBot.

• `{i}repai <reply to user/give a message>`
   Reply to the user with a message by an AI.

• `{i}listai`
   List the currently AI added users.
"""

from pyUltroid.dB.chatBot_db import add_chatbot, get_all_added, rem_chatbot
from pyUltroid.functions.tools import get_chatbot_reply

from . import eod, eor, get_string, inline_mention, ultroid_cmd


@ultroid_cmd(pattern="repai")
async def im_lonely_chat_with_me(event):
    if event.reply_to:
        message = (await event.get_reply_message()).message
    else:
        try:
            message = event.text.split(" ", 1)[1]
        except IndexError:
            return await eod(event, get_string("tban_1"), time=10)
    reply_ = await get_chatbot_reply(message=message)
    await eor(event, reply_)


@ultroid_cmd(pattern="addai")
async def add_chatBot(event):
    await chat_bot_fn(event, type_="add")


@ultroid_cmd(pattern="remai")
async def rem_chatBot(event):
    await chat_bot_fn(event, type_="remov")


@ultroid_cmd(pattern="listai")
async def lister(event):
    users = get_all_added(event.chat_id)
    if not users:
        return await eor(event, get_string("chab_2"), time=5)
    msg = "**Total List Of AI Enabled Users In This Chat :**\n\n"
    for i in users:
        try:
            user = await event.client.get_entity(int(i))
            user = inline_mention(user)
        except BaseException:
            user = f"`{i}`"
        msg += "• {}\n".format(user)
    await eor(event, msg, link_preview=False)


async def chat_bot_fn(event, type_):
    if event.reply_to:
        re_ = await event.get_reply_message()
        user = await re_.get_sender()
        user_id = re_.sender_id
    else:
        temp = event.text.split(maxsplit=1)
        try:
            user = await event.client.get_entity(temp[1])
            user_id = user.id
        except BaseException:
            if event.is_private:
                user_id = event.chat_id
                user = await event.get_chat()
            else:
                return await eod(
                    event,
                    get_string("chab_1"),
                )
    if type_ == "add":
        add_chatbot(event.chat_id, user_id)
    if type_ == "remov":
        rem_chatbot(event.chat_id, user_id)
    await eor(
        event, f"**ChatBot:**\n{type_}ed {inline_mention(user)}"
    )
