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
        ... 
        
    @staticmethod
    def init_queue(guilds: List[Guild]) -> None:
        for guild in guilds:
            SongQueue[guild.name] = list()
    
    def get_queue(self, ctx: commands.Context) -> List[str]:
        return SongQueue[ctx.guild.name]

    def b_in_queue(self, guild: str) -> bool:
        if guild in SongQueue:
            return True
        return False
    
    def is_empty(self, ctx: commands.Context) -> bool:
        if len(SongQueue[ctx.guild.name]) == 0:
            return True
        return False

    def pop_song(self, ctx: commands.Context) -> str:
        return SongQueue[ctx.guild.name].pop(0)

    def swap(self, ctx: commands.Context, i1: int, i2: int) -> None:
        queue = self.get_queue(ctx)
        i1 = i1 - 1
        i2 = i2 - 1
        temp = queue[i1]
        queue[i1] = queue[i2]
        queue[i2] = temp
    
    def add_song(self, ctx: commands.Context, song: str) -> None:
        if self.is_empty(ctx):
            SongQueue[ctx.guild.name] = [song]
        else:
            SongQueue[ctx.guild.name].append(song)
            
    def add_songs(self, ctx: commands.Context, songs: Union[List[str], dict]) -> None:
        if isinstance(songs, list):
            for song in songs:
                self.add_song(ctx, song)
                
        elif isinstance(songs, dict):
            for k, v in songs.items():
                self.add_song(ctx, f"{k} - ({v})")
            
    def clear_queue(self, ctx: commands.Context) -> None:
        SongQueue[ctx.guild.name].clear()
        
    def shuffle_queue(self, ctx: commands.Context) -> None:
        shuffle(SongQueue[ctx.guild.name])
