from telegram import Bot
import asyncio

TOKEN = "8753108669:AAHH0qc5kZCjTnyhVvnhaNwDlGO1oapXEME"

bot = Bot(token=TOKEN)

async def test():
    me = await bot.get_me()
    print(f"Bot connecté : {me.first_name}")

asyncio.run(test())