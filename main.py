import os
import asyncio

from dotenv import load_dotenv

from src.bot import MrBeat

load_dotenv()
TOKEN = os.getenv("TOKEN")

COGS = [
        "src.greetings",
        "src.stats",
        "src.music",
        "src.events"
    ]

async def main():
    bot = MrBeat()
    for cog in COGS:
        await bot.load_extension(cog)
    await bot.start(TOKEN)

asyncio.run(main())
