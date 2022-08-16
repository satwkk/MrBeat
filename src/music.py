import discord

from typing import List
from discord import Embed
from random import shuffle
from discord.ext import commands

from src.playlist import PlayListManager
from src.factory import ExtractorFactory
from src.queue import QueueManager, SONGQUEUE
from src.config import INVOKER_NOT_JOINED_ALERT
from src.extract import YoutubeSongExtractor, SpotifySongExtractor

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.factory = ExtractorFactory()
        self.playlistManager = PlayListManager()
        self.queueManager = QueueManager()
        self.current_song = None
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    '''
    Checks if the author who invoked the command is in any voice channel.
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
    async def play_next_song(self, ctx: commands.Context) -> None:
        if self.queueManager.bIsEmpty(ctx):
            return
        
        if ctx.guild.name in SONGQUEUE:
            await self.play_song(self.queueManager.popSong(ctx), ctx)
            
    '''
    Heart of the play command. It extracts song from the keyword, crafts an embed and plays the song
    @param: url - The keyword or url to the song
    '''
    async def play_song(self, url: str, ctx: commands.Context) -> None:
        if self.bIsVoiceClientActive(ctx):
            ctx.voice_client.stop()

        extractor = self.factory.getExtractor(url)
        if isinstance(extractor, YoutubeSongExtractor):
            song = extractor.extract_song(url)
            
        audio_source = await discord.FFmpegOpusAudio.from_probe(song.url, **self.FFMPEG_OPTIONS)
        if audio_source:
            music_embed = Embed(title="Playing 🎵", colour=discord.Color.dark_gold())
            music_embed.add_field(name=f"{song.title}", value='\u200b')
            music_embed.set_image(url=song.thumbnail)
            await ctx.channel.send(embed=music_embed)
            
        ctx.voice_client.play(audio_source, after=lambda e: self.bot.loop.create_task(self.play_next_song(ctx)))
            
    '''
    Pauses the currently playing song.
    @param: None
    '''
    @commands.command(aliases=['pau', 'paus', 'stop', 'pa'], pass_context=True)
    async def pause(self, ctx: commands.Context):
        if ctx.message.author.voice is None:
            return await ctx.channel.send(INVOKER_NOT_JOINED_ALERT)
           
        await ctx.channel.send("PAUSED ⏸")
        ctx.voice_client.pause()

    '''
    Resumes the currently paused song.
    @param: None
    '''
    @commands.command(aliases=['r', 'res', 'resum', 'resu'], pass_context=True)
    async def resume(self, ctx: commands.Context):
        if ctx.message.author.voice is None:
            return await ctx.channel.send(INVOKER_NOT_JOINED_ALERT)
           
        await ctx.channel.send("RESUMED ⏯")
        ctx.voice_client.resume()

    '''
    Leaves the voice channel and clears all the queue
    @param: None
    '''
    @commands.command(aliases=['lea', 'leav'], pass_context=True)
    async def leave(self, ctx: commands.Context):
        if ctx.message.author.voice is None:
            return await ctx.channel.send(INVOKER_NOT_JOINED_ALERT)
           
        self.queueManager.clearQueue(ctx)
        await ctx.voice_client.disconnect()
    
    '''
    Adds a song to the queue if already playing some audio.
    @param: song - The name of song to add to queue.
    '''
    @commands.command(aliases=['q', 'que'], pass_context=True)
    async def queue(self, ctx: commands.Context, *, song: str):
        if ctx.message.author.voice is None:
            return await ctx.channel.send(INVOKER_NOT_JOINED_ALERT)
           
        if self.bIsVoiceClientActive(ctx):
            self.queueManager.addSong(ctx, song)
            await ctx.channel.send(f"_{song}_ added to the queue.")
        else:
            await ctx.channel.send('Play a fucking music before queuing retard.')
    
    '''
    Lists all songs in the queue.
    @param: None
    '''
    @commands.command(aliases=['l', 'lq', 'listq', 'listqueue'], pass_context=True)
    async def list_queue(self, ctx: commands.Context):
        if self.queueManager.bIsEmpty(ctx):
            return await ctx.channel.send('No songs in queue')
        
        embed = Embed(title="Queued Songs 🎶", colour=discord.Color.red())
        for idx, songs in enumerate(SONGQUEUE[ctx.guild.name]):
            embed.add_field(name="\u200b", value=f"**{idx + 1}. {songs}**", inline=False)
        await ctx.channel.send(embed=embed)

    '''
    Shuffles the queue if it has more than one song.
    @param: None
    '''
    @commands.command(aliases=['shuffleq', 'shuffle'], pass_context=True)
    async def shuffle_queue(self, ctx: commands.Context):
        self.queueManager.shuffleQueue(ctx)
        
    @commands.command(name='debug', pass_context=True)
    @commands.has_role('Developer')
    async def debug(self, ctx: commands.Context):
        print(SONGQUEUE)
    
    '''
    Clears the queue.
    @param: None
    '''  
    @commands.command(aliases=['f', 'fl', 'fq', 'flushq', 'flushqueue'], pass_context=True)
    async def flush(self, ctx: commands.Context):
        if ctx.message.author.voice is None:
            return await ctx.channel.send(INVOKER_NOT_JOINED_ALERT)
        
        if self.queueManager.bIsEmpty(ctx):
            return await ctx.channel.send('No songs in queue.')
        
        self.queueManager.clearQueue(ctx)
    
    '''
    Skips the current song playing and plays another one in the queue. 
    If empty is returns.
    @param: None
    '''
    @commands.command(aliases=['s', 'sk', 'ski'], pass_context=True)
    async def skip(self, ctx: commands.Context):
        if ctx.message.author.voice is None:
            return await ctx.channel.send(INVOKER_NOT_JOINED_ALERT)
        
        if self.queueManager.bIsEmpty(ctx): 
            return await ctx.channel.send('No songs in queue to skip.')
        
        ctx.voice_client.stop()
    
    '''
    Plays a song as requested by user. This takes in a keyword to perform a search 
    and picks the most convinient one from the songs list.
    @param: url - The url of a youtube video or keyword.
    '''    
    @commands.command(aliases=['p', 'pla', 'pl'], pass_context=True)
    async def play(self, ctx: commands.Context, *, url: str):
        if ctx.message.author.voice is None:
            return await ctx.channel.send(INVOKER_NOT_JOINED_ALERT)

        if ctx.voice_client is None: 
            await ctx.author.voice.channel.connect()
        
        if not self.queueManager.bIsEmpty(ctx): 
            return await ctx.channel.send(f"There are music in queues retard.")
        
        await self.play_song(url, ctx)

    '''
    Adds a given spotify playlist into the database to cache the songs based on key, value pair.
    Song - Key
    Author - Value
    TODO: Add check if playlist already exists.
    @param: name - The playlist name to be cached into database.
    @param: url - The spotify playlist url to extract all songs.
    '''
    @commands.command(aliases=['ap', 'add'], pass_context=True)
    async def add_playlist(self, ctx: commands.Context, name: str, url: str):
        if not url.startswith('http') or not url.startswith('https'): 
            return await ctx.channel.send(f"\"{url}\" is not Valid playlist URL.")
        
        if self.playlistManager.bAlreadyExists(name):
            return await ctx.channel.send(f"{name} already exists, try a different name.")

        await ctx.channel.send("Caching all songs. Please wait.")
        async with ctx.channel.typing():
            extractor = self.factory.getExtractor(url)
            if isinstance(extractor, SpotifySongExtractor):
                results = extractor.extract_song(url)
                
                playlistName = self.playlistManager.createPlaylist(name=name)
                
                for song, author in results.items():
                    finalSongName = "{}({})".format(song, author)
                    self.playlistManager.insertPlaylist(name=playlistName, song=finalSongName)
                    
                await ctx.channel.send(f"All songs added to playlist {playlistName} created by user {ctx.author.name}")
    
    '''
    Lists all the playlists in the database.
    TODO: Add playlist specific to channels.
    @param: None
    '''
    @commands.command(aliases=['lp', 'listp'], pass_context=True)
    async def list_playlist(self, ctx: commands.Context):
        playlists = self.playlistManager.listTables()
        
        value = ""
        playlistEmbed = Embed(title="_Available Playlists_ 📻", colour=discord.Color.purple())
        async with ctx.channel.typing():
            for idx, playlist in enumerate(playlists):
                value += f"**{idx + 1}. {playlist[0]}**\n"
            playlistEmbed.add_field(name="-" * len(playlistEmbed.title), value=value)
            await ctx.channel.send(embed=playlistEmbed)
                
    '''
    Plays a playlist requested by user.
    Before playing it clears the queue and adds all the songs to the queue.
    @param: playlist - The name of the playlist to play.
    '''        
    @commands.command(aliases=['pp', 'playp'], pass_context=True)
    async def play_playlist(self, ctx: commands.Context, *, playlist: str):
        if ctx.voice_client is None: 
            await ctx.author.voice.channel.connect()
            
        if not self.queueManager.bIsEmpty(ctx): 
            self.queueManager.clearQueue(ctx)
        
        count = 0
        contents = self.playlistManager.getContents(table=playlist)
        if contents is None:
            return await ctx.channel.send(f"No playlist found by name {playlist} Use listp to list all the playlists.")
        
        for song in contents:
            count += 1
            self.queueManager.addSong(ctx, song[0])
            
        await ctx.channel.send(f"{count} songs added to queue.")
        
        if self.bIsVoiceClientActive(ctx):
            ctx.voice_client.stop()
            return
        
        await self.play_song(self.queueManager.popSong(ctx), ctx)
        
def setup(bot):
    bot.add_cog(Music(bot))
