import discord

from threading import Thread
from discord.ext import commands
from discord import Embed, FFmpegOpusAudio, Color

from src.extract import extract
from src.models.track import Track
from src.queue import QueueManager, SongQueue
from src.extractors.youtube import search_track
from src.config import FFMPEG_OPTIONS, YT_SEARCH_FMT
from src.exceptions import InvokerClientError, QueueIsEmpty, QueueNotEmpty

def craft_embed(**kwargs):
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
    def __init__(self, **attrs) -> None:
        super().__init__(**attrs)

    def is_vc_active(self):
        if self.voice_client.is_playing() or self.voice_client.is_paused(): return True
        return False

    def is_valid_author(self) -> bool:
        return False if not self.message.author.voice else True

    async def play(self, song: Track, after):
        audio_source = await FFmpegOpusAudio.from_probe(song.audio_stream_url, **FFMPEG_OPTIONS)
        await self.send(embed=craft_embed(song_title=f'{song.track_title}', song_thumbnail=song.thumbnail_url))
        self.voice_client.play(audio_source, after=after)
    
    def stop(self):
        self.voice_client.stop()
        
# TODO: All exception handling and user feedback
class Music(commands.Cog):
    ''' Music class for all music related command handling '''
    def __init__(self, bot) -> None:
        self.bot = bot
        self.loop = self.bot.loop
        self.queueManager = QueueManager()
        
    def search_song_in_queue(self, ctx: BeatCtx) -> Track:
        song = self.queueManager.pop_song(ctx)
        return search_track(YT_SEARCH_FMT.format(song.track_title, song.author_name))
    
    def play_next_song(self, ctx: BeatCtx) -> None:
        if self.queueManager.is_empty(ctx): 
            return
        
        next_song = self.queueManager.pop_song(ctx)
        if not next_song.playable:
            next_song = search_track(YT_SEARCH_FMT.format(next_song.track_title, next_song.author_name))
        self.loop.create_task(self.play_song(next_song, ctx))

    async def play_song(self, song: Track, ctx: BeatCtx) -> None:
        await ctx.play(song, after=lambda e=None: self.play_next_song(ctx))
        
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
        # Extracts the track content beforehand to save time.
        # TODO: Add multithreading maybe ?
        track = extract(song)
        # If the url entered is playlist then add all song from the playlist into the queue
        if isinstance(track, list): self.queueManager.add_songs(ctx, track)
        else: self.queueManager.add_song(ctx, track)
        await ctx.send(f"**{song}** added to the queue.")
    
    @commands.command(aliases=['l', 'lq', 'listq', 'listqueue'], pass_context=True)
    async def list_queue(self, ctx: BeatCtx) -> None:
        if self.queueManager.is_empty(ctx): return await ctx.send('No songs in queue')
        queueEmbed = Embed(title="Queued Songs 🎶", colour=discord.Color.red())
        for idx, songs in enumerate(SongQueue[ctx.guild.name]):
            queueEmbed.add_field(name="\u200b", value=f"**{idx + 1}. {songs.track_title}**\n", inline=False)
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
    
    # TODO: Refactor all these checks for the play command        
    @commands.command(aliases=['p', 'pla', 'pl'], pass_context=True)
    async def play(self, ctx: BeatCtx, *, url: str) -> None:
        if not ctx.is_valid_author():  raise InvokerClientError
        if not ctx.voice_client:  await ctx.author.voice.channel.connect()
        if not self.queueManager.is_empty(ctx):  return await ctx.send('There are musics in queues. Add song to queue or flush it.')
        if ctx.is_vc_active():  ctx.voice_client.stop()
            
        song = extract(url)
        if isinstance(song, list):
            self.queueManager.add_songs(ctx, song)
            song = self.search_song_in_queue(ctx)
        print('PLAYING SONG')
        await self.play_song(song, ctx)

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

async def setup(bot):
    await bot.add_cog(Music(bot))
