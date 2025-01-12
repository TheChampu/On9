from pyrogram import Client, filters
from pyrogram.types import Message
from info import PREFIX, ADMIN
import asyncio


user = {}
afk_status = {}
notified_users = set()
@Client.on_message(filters.command("afk", PREFIX) & filters.private & filters.me)
async def set_afk(client, message: Message):
    user_id = message.from_user.id
    if user_id == ADMIN:
        afk_reason = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else "No reason provided."
        afk_status[user_id] = afk_reason
        m = await message.edit(f"You are now AFK: {afk_reason}")
        await asyncio.sleep(3)
        await m.delete()

@Client.on_message(filters.text & filters.private)
async def greet_user(client, message: Message):
    user_id = message.from_user.id
    if message.from_user.is_bot:
        return
    # Greet new users
    if user_id not in user and user_id != ADMIN:
        user[user_id] = 1
        await message.reply_text(f"Hello, How can I help you?")
    
    # Check if the admin is back from AFK
    if user_id == ADMIN and user_id in afk_status:
        del afk_status[user_id]
        m = await message.reply_text("You are no longer AFK.")
        await asyncio.sleep(2)
        await m.delete()
        notified_users.clear()
    
    # Notify others if the admin is AFK
    if user_id != ADMIN and ADMIN in afk_status and user_id not in notified_users:
        await message.reply_text(f"My owner is currently AFK!\n**Reason:** {afk_status[ADMIN]}")
        notified_users.add(user_id)