from discord import Guild

from typing import List, Optional
from typing import Union
from random import shuffle
from discord.ext import commands

# ============================ Song Queue for all guilds =================
SongQueue = dict()
# ========================================================================

''' Queue Manager class that handles all operation for song queue on all channels'''
class QueueManager:
    def __init__(self):
        self.position = 0
        
    @staticmethod
    def initQueue(guilds: List[Guild]) -> None:
        for guild in guilds:
            SongQueue[guild.name] = list()
    
    def bIsInQueue(self, guild: str) -> bool:
        if guild in SongQueue:
            return True
        return False
    
    def bIsEmpty(self, ctx: commands.Context) -> bool:
        if len(SongQueue[ctx.guild.name]) == 0:
            return True
        return False

    def popSong(self, ctx: commands.Context) -> str:
        return SongQueue[ctx.guild.name].pop(0)
    
    def addSong(self, ctx: commands.Context, song: str) -> None:
        if self.bIsEmpty(ctx):
            SongQueue[ctx.guild.name] = [song]
        else:
            SongQueue[ctx.guild.name].append(song)
            
    def addSongs(self, ctx: commands.Context, songs: Union[List[str], dict]) -> None:
        if isinstance(songs, list):
            for song in songs:
                self.addSong(ctx, song)
                
        elif isinstance(songs, dict):
            for k, v in songs.items():
                self.addSong(ctx, f"{k} - ({v})")
            
    def clearQueue(self, ctx: commands.Context) -> None:
        SongQueue[ctx.guild.name].clear()
        
    def shuffleQueue(self, ctx: commands.Context) -> None:
        shuffle(SongQueue[ctx.guild.name])
