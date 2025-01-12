from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio
from info import PREFIX


# command to delete all messages
@Client.on_message(filters.me & filters.command("deletechat", PREFIX) & filters.reply)
async def clearchat(client, message):
    chat_id = message.chat.id

    # send msg to show that bot is working
    await message.edit("Deleting all messages...")
    await asyncio.sleep(2)

    # get all messages
    async for msg in client.get_chat_history(chat_id):
        if not msg.message_id:
            break
        try:
            # delete message
            await client.delete_user_history(chat_id, msg.from_user.id)
        except FloodWait as e:
            # wait for a while
            print(e)
            await asyncio.sleep(e.x)
        except Exception as e:
            print(e)
            pass