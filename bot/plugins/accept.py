from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio, logging
from info import PREFIX


@Client.on_message(filters.command(["run", "approve"], PREFIX) & filters.me)                     
async def approve(client, message):
    Id = message.chat.id
    await message.delete(True)
 
    try:
       while True:
           try:
               result = await client.approve_all_chat_join_requests(Id)
               if not result:  # If no join request is pending
                   break         
           except FloodWait as t:
               asyncio.sleep(t.value)
               await client.approve_all_chat_join_requests(Id) 
           except Exception as e:
               logging.error(str(e))
    except FloodWait as s:
        asyncio.sleep(s.value)
        while True:
           try:
               result = await client.approve_all_chat_join_requests(Id)
               if not result:  # If no join request is pending
                   break
           except FloodWait as t:
               asyncio.sleep(t.value)
               await client.approve_all_chat_join_requests(Id) 
           except Exception as e:
               logging.error(str(e))