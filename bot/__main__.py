from bot import TelegramBot
from bot.server.serve import web_server
import asyncio
from aiohttp import web

async def webrun():
    app = web.AppRunner(await web_server())
    await app.setup()
    site = web.TCPSite(app, "0.0.0.0", 5050)
    await site.start()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(webrun())
    TelegramBot.run()
    loop.run_forever()
