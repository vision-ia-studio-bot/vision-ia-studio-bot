from telegram import Bot
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)

async def test():
    me = await bot.get_me()
    print(f"Bot connecté : {me.first_name}")

asyncio.run(test())
