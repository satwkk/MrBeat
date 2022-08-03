from cprint import cprint
from discord.ext import commands
from typing import AsyncIterator, List

from src.logger import ErrorLogMessage, DebugLogMessage, log
from src.queue import SONGQUEUE, QueueManager

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        
        # Initializing the song queue
        QueueManager.initQueue(self.bot.guilds)
        
        # Printing debug info about bot and guilds
        await self.load_bot_info()
        
    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context) -> None:
        log(DebugLogMessage(ctx.message))
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        log(ErrorLogMessage(ctx.message))
        
    async def load_channels(self, guilds: AsyncIterator):
        async for guild in guilds:
            cprint.info("============================= " + guild.name + " ============================= ")
            for channel in await guild.fetch_channels():
                cprint.info(channel.name)
                
    async def load_bot_info(self):
        cprint.info(f"[DEBUG] Mr Beat Online. Latency: {self.bot.latency}")
        cprint.info(f"[DEBUG] Guilds Loaded: {', '.join([guild.name for guild in self.bot.guilds])}\n")
        await self.load_channels(self.bot.fetch_guilds())
        cprint.ok("Bot ready to use !!! \n")
    
def setup(bot):
    bot.add_cog(Events(bot))
