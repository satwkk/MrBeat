import discord
from discord.ext import commands

from src.config import COMMAND_PREFIX

class MrBeat(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix=COMMAND_PREFIX, intents=intents)
