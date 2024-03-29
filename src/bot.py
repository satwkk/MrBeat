import discord
from discord.ext import commands

from src.music import BeatCtx
from src.config import COMMAND_PREFIX

class MrBeat(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix=COMMAND_PREFIX, intents=intents)

    async def get_context(self, message, *, cls = BeatCtx):
        return await super().get_context(message, cls = cls)

    
