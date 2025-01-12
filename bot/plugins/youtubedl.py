from __future__ import unicode_literals
import os, time
import requests, wget
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from pyrogram import Client, filters
from pyrogram.types import Message
from info import PREFIX


@Client.on_message(filters.command(['song', 'mp3'], PREFIX) & filters.me)
async def song_cmd(client, message):
    query = ' '.join(message.command[1:])
    print(query)
    m = await message.edit(f"Searching...")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        duration = results[0]["duration"]
    except Exception as e:
        print(str(e))
        return await m.edit("Nothing Found")

    await m.edit("Downloading...")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        dur = sum(int(x) * 60**i for i,x in enumerate(reversed(duration.split(':'))))
        await message.reply_audio(
            audio_file,           
            quote=False,
            title=title,
            duration=dur,
            thumb=thumb_name
        )            
        await m.delete()
    except Exception as e:
        await m.edit("An Error Occured While Downloading The Song.")
        print(e)
    finally:
        os.remove(audio_file)
        os.remove(thumb_name)

@Client.on_message(filters.command(['video', 'mp4'], PREFIX) & filters.me)
async def vsong_cmd(client, message: Message):
    try:
        urlissed = message.text.split(None, 1)[1] if " " in message.text else None
        if not urlissed:
            return await message.edit("Invalid Command")
        msg = await message.edit_text("Fetching...")
        search = YoutubeSearch(f"{urlissed}", max_results=1).to_dict()
        video_info = search[0]
        url = f"https://www.youtube.com{video_info['url_suffix']}"
        thumbnail_url = f"https://img.youtube.com/vi/{video_info['id']}/hqdefault.jpg"
        thumbnail_file = wget.download(thumbnail_url)
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        time.sleep(0.5)  # delay for 5 seconds
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
        video_file = f"{ytdl_data['id']}.mp4"

        await client.send_video(
            message.chat.id,
            video=open(video_file, "rb"),
            duration=int(ytdl_data["duration"]),
            file_name=str(ytdl_data["title"]),
            thumb=thumbnail_file,
            supports_streaming=True,
        )
        await msg.delete()
        for files in (thumbnail_file, video_file):
            if files and os.path.exists(files):
                os.remove(files)
    except Exception as e:
        return await message.edit_text(f"An error occurred: `{str(e)}")
