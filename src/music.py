import discord

from discord import Embed, FFmpegOpusAudio, Color
from discord.ext import commands

from src.extract import Song
from src.youtube import Youtube
from src.factory import ExtractorFactory
from src.queue import QueueManager, SongQueue
from src.config import FFMPEG_OPTIONS
from src.exceptions import InvokerClientError, QueueIsEmpty, QueueNotEmpty

def craft_embed(**kwargs):
    ''' Crafts an embed '''
    song_title = kwargs.get('song_title') 
    song_thumbnail = kwargs.get('song_thumbnail')
    
    music_embed = Embed(title="Playing 🎵", colour=Color.random())
    music_embed.add_field \
    (
        name=f"{song_title if song_title else 'n/a'}", 
        value="\u200b"
    )
    if song_thumbnail: music_embed.set_thumbnail(url=song_thumbnail)
    return music_embed

class BeatCtx(commands.Context):
    ''' Custom context class around commands.Context'''
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def is_vc_active(self):
        if self.voice_client.is_playing() or self.voice_client.is_paused(): return True
        return False

    def is_valid_author(self) -> bool:
        return False if not self.message.author.voice else True

    async def play(self, song: Song, after):
        audio_source = await FFmpegOpusAudio.from_probe(song.audioStream, **FFMPEG_OPTIONS)
        await self.send(embed=craft_embed(song_title=f'{song.title}', song_thumbnail=song.thumbnail))
        self.voice_client.play(audio_source, after=after)
    
    def stop(self):
        self.voice_client.stop()

class Music(commands.Cog):
    ''' Music class for all music related command handling '''
    def __init__(self, bot) -> None:
        self.bot = bot
        self.loop = self.bot.loop
        self.currentSong = None
        self.player = Youtube()
        self.factory = ExtractorFactory()
        self.queueManager = QueueManager()
    
    def play_next_song(self, ctx: BeatCtx) -> None:
        if self.queueManager.is_empty(ctx): return
        if ctx.guild.name in SongQueue:
            self.loop.create_task(self.play_song(self.queueManager.pop_song(ctx), ctx))
            
    async def play_song(self, url: str, ctx: BeatCtx) -> None:
        if ctx.is_vc_active(): ctx.voice_client.stop()
        extractor = self.factory.getExtractor(url)
        song = extractor.extract(url)
        if isinstance(song, dict):
            self.queueManager.add_songs(ctx, song)
            song = self.factory.getYoutubeSongExtractor().extract(self.queueManager.pop_song(ctx))
        self.loop.create_task(ctx.play(song, after=lambda e=None: self.play_next_song(ctx)))
            
    @commands.command(aliases=['pau', 'paus', 'stop', 'pa'], pass_context=True)
    async def pause(self, ctx: BeatCtx) -> None:
        if not ctx.is_valid_author(): raise InvokerClientError
        if not ctx.voice_client.is_playing(): return
        ctx.voice_client.pause()
        await ctx.send(f"PAUSED ⏸ ")

    @commands.command(aliases=['r', 'res', 'resum', 'resu'], pass_context=True)
    async def resume(self, ctx: BeatCtx) -> None:
        if not ctx.is_valid_author(): raise InvokerClientError
        await ctx.send(f"RESUMED ⏯ ")
        ctx.voice_client.resume()

    @commands.command(aliases=['lea', 'leav'], pass_context=True)
    async def leave(self, ctx: BeatCtx) -> None:
        if not ctx.is_valid_author(): raise InvokerClientError
        self.queueManager.clear_queue(ctx)
        await ctx.voice_client.disconnect()
    
    @commands.command(aliases=['q', 'que'], pass_context=True)
    async def queue(self, ctx: BeatCtx, *, song: str) -> None:
        if not ctx.is_valid_author(): raise InvokerClientError
        if not ctx.is_vc_active(): return await ctx.send('Not playing any track. Use play command to play a song directly.')
        self.queueManager.add_song(ctx, song)
        await ctx.send(f"**{song}** added to the queue.")
    
    @commands.command(aliases=['l', 'lq', 'listq', 'listqueue'], pass_context=True)
    async def list_queue(self, ctx: BeatCtx) -> None:
        if self.queueManager.is_empty(ctx): return await ctx.send('No songs in queue')
        queueEmbed = Embed(title="Queued Songs 🎶", colour=discord.Color.red())
        for idx, songs in enumerate(SongQueue[ctx.guild.name]):
            queueEmbed.add_field(name="\u200b", value=f"**{idx + 1}. {songs}**\n", inline=False)
        await ctx.send(embed=queueEmbed)
        
    @commands.command(aliases=['shuffleq', 'shuffle'], pass_context=True)
    async def shuffle_queue(self, ctx: BeatCtx) -> None:
        if self.queueManager.is_empty(ctx): return await ctx.send('No songs in queue')
        self.queueManager.shuffle_queue(ctx)
    
    # NOTE: Debug Only
    @commands.command(name='debug', pass_context=True)
    @commands.has_role('Developer')
    async def debug(self, ctx: BeatCtx):
        print(ctx.voice_client)
        print(SongQueue)
    
    @commands.command(aliases=['f', 'fl', 'fq', 'flushq', 'flushqueue'], pass_context=True)
    async def flush(self, ctx: BeatCtx) -> None:
        if not ctx.is_valid_author(): raise InvokerClientError
        if self.queueManager.is_empty(ctx): raise QueueIsEmpty
        self.queueManager.clear_queue(ctx)
        
    @commands.command(aliases=['sw'], pass_context=True)
    @commands.has_role('Developer')
    async def swap(self, ctx: BeatCtx, i1: str, i2: str) -> None:
        if self.queueManager.is_empty(ctx): raise QueueIsEmpty
        self.queueManager.swap(ctx, int(i1), int(i2))
    
    @commands.command(aliases=['s', 'sk', 'ski'], pass_context=True)
    async def skip(self, ctx: BeatCtx) -> None:
        if not ctx.is_valid_author(): raise InvokerClientError
        if self.queueManager.is_empty(ctx): raise QueueIsEmpty
        ctx.stop()
        
    @commands.command(aliases=['p', 'pla', 'pl'], pass_context=True)
    async def play(self, ctx: BeatCtx, *, url: str) -> None:
        if not ctx.is_valid_author(): raise InvokerClientError
        if not ctx.voice_client: await ctx.author.voice.channel.connect()
        if not self.queueManager.is_empty(ctx): raise QueueNotEmpty
        self.loop.create_task(self.play_song(url, ctx))

    # ERROR HANDLING
    @skip.error
    async def skip_error(self, ctx: BeatCtx, err: commands.CommandError):
        if isinstance(err, QueueIsEmpty): return await ctx.send("No songs in queue")
        
    @flush.error
    async def flush_error(self, ctx: BeatCtx, err: commands.CommandError):
        if isinstance(err, QueueIsEmpty): await ctx.send('No songs in queue')

    @swap.error
    async def swap_error(self, ctx: BeatCtx, err: commands.CommandError):
        if isinstance(err, QueueIsEmpty): return await ctx.send('No songs in queue')

    @play.error
    async def play_err(self, ctx: BeatCtx, err: commands.CommandError):
        if isinstance(err, QueueNotEmpty): return await ctx.send(f'There are musics in queues. Add song to queue or flush it.')
    
def setup(bot):
    bot.add_cog(Music(bot))
