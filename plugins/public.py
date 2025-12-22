# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re
import asyncio 
from .utils import STS
from database import Db, db
from config import temp 
from script import Script
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait 
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate as PrivateChat
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified, ChannelPrivate
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.private & filters.command(["forward"]))
async def run(bot, message):
    buttons = []
    btn_data = {}
    user_id = message.from_user.id
    _bot = await db.get_bot(user_id)
    if not _bot:
      _bot = await db.get_userbot(user_id)
      if not _bot:
          return await message.reply("<code>You didn't added any bot. Please add a bot using /settings !</code>")
    channels = await db.get_user_channels(user_id)
    if not channels:
       return await message.reply_text("please set a to channel in /settings before forwarding")
    if len(channels) > 1:
       for channel in channels:
          buttons.append([KeyboardButton(f"{channel['title']}")])
          btn_data[channel['title']] = channel['chat_id']
       buttons.append([KeyboardButton("cancel")]) 
       _toid = await bot.ask(message.chat.id, Script.TO_MSG.format(_bot['name'], _bot['username']), reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))
       if _toid.text.startswith(('/', 'cancel')):
          return await message.reply_text(Script.CANCEL, reply_markup=ReplyKeyboardRemove())
       to_title = _toid.text
       toid = btn_data.get(to_title)
       if not toid:
          return await message.reply_text("wrong channel choosen !", reply_markup=ReplyKeyboardRemove())
    else:
       toid = channels[0]['chat_id']
       to_title = channels[0]['title']
    
    # Ask for STARTING message (first message in range)
    await bot.send_message(user_id, "**❪ SET STARTING MESSAGE ❫**\n\nForward the FIRST message in the range you want to forward.", reply_markup=ReplyKeyboardRemove())
    start_msg = await bot.ask(user_id, text="**Forward the STARTING message (first message in range) from source chat or send its message link.**\n/cancel - `cancel this process`")
    
    if start_msg.text and start_msg.text.startswith('/'):
        await message.reply(Script.CANCEL)
        return 
    
    # Parse starting message info
    start_chat_id, start_msg_id = await parse_message_info(bot, start_msg)
    if not start_chat_id:
        return
    
    # Ask for ENDING message (last message in range)
    await bot.send_message(user_id, "**❪ SET ENDING MESSAGE ❫**\n\nForward the LAST message in the range you want to forward.", reply_markup=ReplyKeyboardRemove())
    end_msg = await bot.ask(user_id, text="**Forward the ENDING message (last message in range) from source chat or send its message link.**\n/cancel - `cancel this process`")
    
    if end_msg.text and end_msg.text.startswith('/'):
        await message.reply(Script.CANCEL)
        return 
    
    # Parse ending message info
    end_chat_id, end_msg_id = await parse_message_info(bot, end_msg)
    if not end_chat_id:
        return
    
    # Verify both messages are from same chat
    if start_chat_id != end_chat_id:
        await message.reply_text("**Error: Starting and ending messages must be from the same chat!**")
        return
    
    # Calculate range (messages between start and end, inclusive)
    if start_msg_id > end_msg_id:
        # Swap if start is after end
        start_msg_id, end_msg_id = end_msg_id, start_msg_id
    
    total_messages = (end_msg_id - start_msg_id) + 1
    
    if total_messages <= 0:
        await message.reply_text("**Error: Invalid message range!**")
        return
    
    try:
        title = (await bot.get_chat(start_chat_id)).title
    except (PrivateChat, ChannelPrivate, ChannelInvalid):
        title = "private" if start_msg.text else start_msg.forward_from_chat.title
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Invalid Link specified.')
    except Exception as e:
        return await message.reply(f'Errors - {e}')
    
    forward_id = f"{user_id}-{start_msg_id}"
    buttons = [[
        InlineKeyboardButton('Yes', callback_data=f"start_public_{forward_id}"),
        InlineKeyboardButton('No', callback_data="close_btn")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    # Create confirmation message
    confirmation_text = f"""
**BOT DETAILS:**
┣ **BOT:** [{_bot['name']}](t.me/{_bot['username']})

**SOURCE CHAT:** `{title}`
**TARGET CHAT:** `{to_title}`

**MESSAGE RANGE:**
┣ **Start Message ID:** `{start_msg_id}`
┣ **End Message ID:** `{end_msg_id}`
┣ **Total Messages:** `{total_messages}`

**Do you want to start forwarding?**
"""
    
    await message.reply_text(
        text=confirmation_text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )
    # Store: start_msg_id as "skip" (first message), total_messages as "limit"
    STS(forward_id).store(start_chat_id, toid, start_msg_id, total_messages)

async def parse_message_info(bot, msg):
    """Parse message info from forwarded message or link"""
    if msg.text and not msg.forward_date:
        # Use raw string for regex to avoid escape sequence warning
        regex = re.compile(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(msg.text.replace("?single", ""))
        if not match:
            await msg.reply('Invalid link')
            return None, None
        chat_id = match.group(4)
        message_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id = int(("-100" + chat_id))
    elif msg.forward_from_chat.type in [enums.ChatType.CHANNEL, 'supergroup']:
        message_id = msg.forward_from_message_id
        chat_id = msg.forward_from_chat.username or msg.forward_from_chat.id
        if message_id is None:
            await msg.reply_text("**This may be a forwarded message from a group and sent by anonymous admin. Please send message link instead.**")
            return None, None
    else:
        await msg.reply_text("**Invalid message format!**")
        return None, None
    
    return chat_id, message_id

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
