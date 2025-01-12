import os
import logging
from telegraph import upload_file
from pyrogram import Client, filters
from info import PREFIX


logging.basicConfig(level=logging.ERROR)

@Client.on_message(filters.command("telegraph", PREFIX) & filters.me)
async def telegraph(client, message):
    if not message.reply_to_message:
        await message.edit('Reply to a message with .telegraph')
        return
    reply = message.reply_to_message
    if reply.media or reply.photo or reply.document or reply.animation:
        file = await client.download_media(reply)
        file_size = os.path.getsize(file)
        if file_size > 5242880:
            await message.edit('File size exceeds 5MB.')
            os.remove(file)
            return
        try:
            media = upload_file(file)
            if media:
                await message.edit(f"Telegraph Link - <code>https://telegra.ph{media[0]}</code>")
            os.remove(file)
        except Exception as e:
            await message.edit(str(e))
    else:
        await message.edit('Reply to a media file with .telegraph')