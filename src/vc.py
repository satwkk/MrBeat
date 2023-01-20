from src.extract import Song
from discord import Embed, Color, FFmpegOpusAudio
from discord.ext import commands
from src.config import FFMPEG_OPTIONS

class BeatClient:
    def __init__(self, context: commands.Context):
        self.context = context
        self.vc = self.context.voice_client
        
    def is_active(self) -> bool:
        if self.vc.is_paused() or self.vc.is_playing():
            return True
        return False
    
    async def play(self, song, after) -> None:
        audio_source = await FFmpegOpusAudio.from_probe(song.audioStream, **FFMPEG_OPTIONS)
        musicEmbed = Embed(title="Playing 🎵", colour=Color.random())
        musicEmbed.add_field(name=f"{song.title}", value='\u200b')
        musicEmbed.set_image(url=song.thumbnail)
        await self.context.send(embed=musicEmbed)
        self.vc.play(audio_source, after=after)
        