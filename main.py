from src.bot import MrBeat

TOKEN = ""

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
