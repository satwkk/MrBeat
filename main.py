import os

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

if __name__ == "__main__":
    bot = MrBeat()
    for cog in COGS:
        bot.load_extension(cog)
    bot.run(TOKEN)
