import discord

from random import shuffle
from discord.ext import commands
from typing import List

# ============================ Song Queue for all guilds =================
SONGQUEUE = dict()
# ========================================================================

''' Queue Manager class that handles all operation for song queue on all channels'''
class QueueManager:
    @staticmethod
    def initQueue(guilds: List[discord.Guild]) -> None:
        for guild in guilds:
            SONGQUEUE[guild.name] = list()
    
    def bIsInQueue(self, guild: str) -> bool:
        if guild in SONGQUEUE:
            return True
        return False
    
    def bIsEmpty(self, ctx: commands.Context) -> bool:
        if len(SONGQUEUE[ctx.guild.name]) == 0:
            return True
        return False
    
    def popSong(self, ctx: commands.Context) -> str:
        return SONGQUEUE[ctx.guild.name].pop(0)
    
    def addSong(self, ctx: commands.Context, song: str) -> None:
        if self.bIsEmpty(ctx):
            SONGQUEUE[ctx.guild.name] = [song]
        else:
            SONGQUEUE[ctx.guild.name].append(song)
        
    def clearQueue(self, ctx: commands.Context) -> None:
        SONGQUEUE[ctx.guild.name].clear()
        
    def shuffleQueue(self, ctx: commands.Context) -> None:
        shuffle(SONGQUEUE[ctx.guild.name])
