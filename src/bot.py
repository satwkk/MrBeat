import discord
from discord.ext import commands

CMD_PREFIX = "."

class MrBeat(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix=CMD_PREFIX, intents=intents)

