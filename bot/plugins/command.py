import time, asyncio, aiohttp, os, sys
from info import DEPLOY_HOOK, PREFIX
from pyrogram import Client, filters, enums

@Client.on_message(filters.command(["help", "h"], PREFIX) & filters.me)
async def help_cmd(client, message):
    await message.edit_text(
        f"**Commands**\n\n"
        f"`{PREFIX}ping` - Check the bot's ping\n"
        f"`{PREFIX}urban or .ud <word>` - Get the urban dictionary meaning of the word\n"
        f"`{PREFIX}meaning or .m <word>` - Get the meaning of the word\n"
        f"`{PREFIX}emoji or {PREFIX}e <text>` - To generate emoji text\n"
        f"`{PREFIX}facts or {PREFIX}f` - Get random facts\n"
        f"`{PREFIX}quotes or {PREFIX}q` - Get random quotes\n"
        f"`{PREFIX}ask or {PREFIX}a <question>` - Ask a question\n"
        f"`{PREFIX}pfq` - Change your profile picture with random quotes\n"
        f"`{PREFIX}bio` - Change your bio with random quotes\n"
        f"`{PREFIX}iquotes` - Generate image with random quotes\n"
        f"`{PREFIX}telegraph` - Create a telegraph post\n"
        f"`{PREFIX}song <song name | song url>` - Download song from youtube\n"
        f"`{PREFIX}video <video url>` - Download video from youtube\n"
        f"`{PREFIX}spam or {PREFIX}s <number> <text>` - Spam the text\n"
        f"`{PREFIX}on9 <on | off>` - To activate One9word game cheat\n"
        f"`{PREFIX}approve` - Approve all joinRequest\n"
        f"`{PREFIX}deletechat` - Delete all chat message from your group\n"
        f"`{PREFIX}update` - Deploy the latest changes\n"
        f"`{PREFIX}dl` - download from http url\n"
        f"`{PREFIX}hack` - Hack animation\n"
        f"`{PREFIX}action <t | p | c` - Start action\n"
        f"`{PREFIX}afk <reason>` - Set AFK\n",
        parse_mode=enums.ParseMode.MARKDOWN
    )

@Client.on_message(filters.command("ping", PREFIX) & filters.me)   
async def ping(client, message):
    start = time.time()  
    m = await message.edit("Pong!")
    end = time.time()
    await m.edit(f"Pong! {round(end-start, 2)}s") 
    
action_on = False
action_type = None
action_dict = {
    't': enums.ChatAction.TYPING,
    'p': enums.ChatAction.PLAYING,
    'c': enums.ChatAction.CHOOSE_STICKER,
}

@Client.on_message(filters.command("action", PREFIX) & filters.me)
async def send_action(client, message):
    global action_on, action_type
    if len(message.text.split()) > 1:
        action_on = not action_on
        action_type = message.text.split()[1]
    else:
        action_on = False
    await message.delete()
    if action_on and action_type in action_dict:
        while action_on:
            await client.send_chat_action(message.chat.id, action_dict[action_type])
            await asyncio.sleep(5)
        
@Client.on_message(filters.command(["spam", "s"], PREFIX) & filters.me)
async def spam_message(client, message):
    _, *text_parts = message.text.split()
    await message.delete()
    try:
        number_of_messages = int(text_parts[0])
        text = ' '.join(text_parts[1:])
    except ValueError:
        number_of_messages = 10
        text = ' '.join(text_parts)
    if text:  # Only send messages if there's text to be spammed
        for _ in range(number_of_messages):
            await message.reply_text(text)
            await asyncio.sleep(0.1)

@Client.on_message(filters.command("restart", PREFIX) & filters.me)
async def restart_services(client, message):
    msg = await message.edit(text="**Process stoped, bot is restarting...**")       
    await asyncio.sleep(3)
    await msg.edit("**Bot restarted**")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.command("update", PREFIX) & filters.me)
async def deploy_bot(client, message):
    m = await message.edit("Deploying the latest changes...")
    await asyncio.sleep(2)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(DEPLOY_HOOK) as resp:
                if resp.status == 200:
                    await m.edit("Deploying...!")
                else:
                    await m.edit("Failed to deploy!")
    except Exception as e:
        await message.edit(f"Error: {str(e)}")