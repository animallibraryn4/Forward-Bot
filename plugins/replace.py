# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import asyncio
from database import Db, db
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.private & filters.command(['replace']))
async def replace_command(client, message):
    user_id = message.from_user.id
    args = message.text.split()
    
    if len(args) < 3:
        await message.reply_text(
            "**Usage:**\n"
            "`/replace @old_text @new_text`\n\n"
            "**Example:**\n"
            "`/replace @anime4 @nikhil`\n\n"
            "This will replace @anime4 with @nikhil in captions when forwarding files.\n\n"
            "**Other commands:**\n"
            "`/replace list` - List all replacement rules\n"
            "`/replace remove @old_text` - Remove a replacement rule\n"
            "`/replace clear` - Clear all replacement rules"
        )
        return
    
    action = args[1].lower()
    
    if action == "list":
        rules = await db.get_replace_rules(user_id)
        if not rules:
            await message.reply_text("**No replacement rules set.**")
            return
        
        rules_text = "**Your Replacement Rules:**\n\n"
        for i, rule in enumerate(rules, 1):
            rules_text += f"{i}. `{rule['old_text']}` → `{rule['new_text']}`\n"
        
        buttons = [
            [InlineKeyboardButton("🗑 Clear All", callback_data="replace_clear")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="settings#main")]
        ]
        
        await message.reply_text(rules_text, reply_markup=InlineKeyboardMarkup(buttons))
    
    elif action == "remove":
        if len(args) < 3:
            await message.reply_text("**Usage:** `/replace remove @old_text`")
            return
        
        old_text = args[2]
        await db.remove_replace_rule(user_id, old_text)
        await message.reply_text(f"**Replacement rule removed:**\n`{old_text}`")
    
    elif action == "clear":
        await db.clear_all_replace_rules(user_id)
        await message.reply_text("**All replacement rules cleared.**")
    
    else:
        # Add new replacement rule
        old_text = args[1]
        new_text = args[2]
        
        await db.add_replace_rule(user_id, old_text, new_text)
        
        await message.reply_text(
            f"**Replacement rule added:**\n\n"
            f"`{old_text}` → `{new_text}`\n\n"
            f"This rule will be applied to captions when forwarding files."
        )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^replace_clear$'))
async def replace_clear_callback(bot, query):
    user_id = query.from_user.id
    await db.clear_all_replace_rules(user_id)
    await query.answer("All replacement rules cleared!", show_alert=True)
    await query.message.edit_text("**All replacement rules cleared.**")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
