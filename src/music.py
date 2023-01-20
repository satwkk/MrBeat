from urllib import parse
import discord

from discord import Embed
from discord.ext import commands

from src.vc import BeatClient
from src.youtube import Youtube
from src.factory import ExtractorFactory
from src.queue import QueueManager, SongQueue
from src.config import AVAILABLE_STREAMING_DOMAINS
from src.exceptions import AlreadyPlayingAudio, InvalidStreamingUrl, InvokerClientError, QueueIsEmpty, QueueNotEmpty, VoiceClientAlreadyActive

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.loop = self.bot.loop
        self.currentSong = None
        self.queryFormat = "{} - ({})"
        self.player = Youtube()
        self.factory = ExtractorFactory()
        self.queueManager = QueueManager()
    
    '''
    Checks the status of voice client.
    Note: Always true once play command is invoked.
    @param: None
    '''
    def bIsVoiceClientActive(self, ctx: commands.Context) -> bool:
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            return True
        return False

    '''
    Plays the next song in queue.
    @param: None
    '''
    def play_next_song(self, ctx: commands.Context) -> None:
        if self.queueManager.is_empty(ctx):
            return
        
        if ctx.guild.name in SongQueue:
            self.loop.create_task(self.play_song(self.queueManager.pop_song(ctx), ctx))
            
    '''
    Heart of the play command. It extracts song from the keyword, crafts an embed and plays the song
    @param: url - The keyword or url to the song
    '''
    async def play_song(self, url: str, ctx: commands.Context) -> None:
        if self.bIsVoiceClientActive(ctx):
            ctx.voice_client.stop()

        extractor = self.factory.getExtractor(url)
        song = extractor.extract(url)

        if isinstance(song, dict):
            self.queueManager.add_songs(
                ctx,
                song
            )
            song = self.factory.getYoutubeSongExtractor().extract(self.queueManager.pop_song(ctx))
        
        self.loop.create_task(BeatClient(ctx).play(song, after=lambda e=None: self.play_next_song(ctx)))
            
    '''
    Pauses the currently playing song.
    @param: None
    '''
    @commands.command(aliases=['pau', 'paus', 'stop', 'pa'], pass_context=True)
    async def pause(self, ctx: commands.Context):
        if ctx.message.author.voice is None:
            raise InvokerClientError
           
        await ctx.send(f"PAUSED ⏸ ")
        ctx.voice_client.pause()

    '''
    Resumes the currently paused song.
    @param: None
    '''
    @commands.command(aliases=['r', 'res', 'resum', 'resu'], pass_context=True)
    async def resume(self, ctx: commands.Context):
        if ctx.message.author.voice is None:
            raise InvokerClientError
           
        await ctx.send(f"RESUMED ⏯ ")
        ctx.voice_client.resume()

    '''
    Leaves the voice channel and clears all the queue
    @param: None
    '''
    @commands.command(aliases=['lea', 'leav'], pass_context=True)
    async def leave(self, ctx: commands.Context):
        if ctx.message.author.voice is None:
            raise InvokerClientError
           
        self.queueManager.clear_queue(ctx)
        await ctx.voice_client.disconnect()
    
    '''
    Adds a song to the queue if already playing some audio.
    @param: song - The name of song to add to queue.
    '''
    @commands.command(aliases=['q', 'que'], pass_context=True)
    async def queue(self, ctx: commands.Context, *, song: str):
        if ctx.message.author.voice is None:
            raise InvokerClientError
           
        if not self.bIsVoiceClientActive(ctx):
            return await ctx.send('Not playing any track. Use play command to play a song directly.')
        
        self.queueManager.add_song(ctx, song)
        await ctx.send(f"**{song}** added to the queue.")
    
    '''
    Lists all songs in the queue.
    @param: None
    '''
    @commands.command(aliases=['l', 'lq', 'listq', 'listqueue'], pass_context=True)
    async def list_queue(self, ctx: commands.Context):
        if self.queueManager.is_empty(ctx):
            return await ctx.send('No songs in queue')
        
        queueEmbed = Embed(title="Queued Songs 🎶", colour=discord.Color.red())
        for idx, songs in enumerate(SongQueue[ctx.guild.name]):
            queueEmbed.add_field(name="\u200b", value=f"**{idx + 1}. {songs}**\n", inline=False)
        await ctx.send(embed=queueEmbed)
        
    '''
    Shuffles the queue if it has more than one song.
    @param: None
    '''
    @commands.command(aliases=['shuffleq', 'shuffle'], pass_context=True)
    async def shuffle_queue(self, ctx: commands.Context):
        if self.queueManager.is_empty(ctx): 
            return await ctx.send('No songs in queue')
        
        self.queueManager.shuffle_queue(ctx)
    
    '''
    NOTE: Debug Only
    '''
    @commands.command(name='debug', pass_context=True)
    @commands.has_role('Developer')
    async def debug(self, ctx: commands.Context):
        print(SongQueue)
    
    '''
    Clears the queue.
    @param: None
    '''  
    @commands.command(aliases=['f', 'fl', 'fq', 'flushq', 'flushqueue'], pass_context=True)
    async def flush(self, ctx: commands.Context):
        if ctx.message.author.voice is None: raise InvokerClientError
        if self.queueManager.is_empty(ctx): raise QueueIsEmpty
        
        self.queueManager.clear_queue(ctx)
        
    @flush.error
    async def flush_error(self, ctx: commands.Context, err: commands.CommandError):
        if isinstance(err, QueueIsEmpty):
            await ctx.send('No songs in queue')
    
    '''
    Skips the current song playing and plays another one in the queue. 
    If empty is returns.
    @param: None
    '''
    @commands.command(aliases=['s', 'sk', 'ski'], pass_context=True)
    async def skip(self, ctx: commands.Context):
        if ctx.message.author.voice is None: raise InvokerClientError
        
        if self.queueManager.is_empty(ctx): 
            return await ctx.send('No songs in queue')
        
        if not self.queueManager.is_empty(ctx) and ctx.voice_client is None:
            self.loop.create_task(self.play_song(self.queueManager.pop_song(ctx), ctx))
        else:
            ctx.voice_client.stop()
        
    '''
    Plays a song as requested by user. This takes in a keyword to perform a search 
    and picks the most convinient one from the songs list.
    @param: url - The url of a youtube video or keyword.
    '''    
    @commands.command(aliases=['p', 'pla', 'pl'], pass_context=True)
    async def play(self, ctx: commands.Context, *, url: str):
        if ctx.message.author.voice is None:
            return await ctx.send(f"There are musics in queues.")

        if ctx.voice_client is None: 
            await ctx.author.voice.channel.connect()
        
        if not self.queueManager.is_empty(ctx): 
            raise QueueNotEmpty

        await self.play_song(url, ctx)
    
def setup(bot):
    bot.add_cog(Music(bot))
