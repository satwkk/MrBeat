from discord.ext import commands
from discord import Embed

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def owner(self, ctx):
       await ctx.channel.send(f"Our king 👑 : {ctx.guild.owner.name}") 

    @commands.command(name="users", pass_context=True)
    async def get_member_count(self, ctx):
        await ctx.channel.send(f"Number of throwers {ctx.guild.member_count}")
    
    @commands.command(name="totalmessages", pass_context=True)
    async def message_count(self, ctx):
        count = 0
        async for _ in ctx.channel.history(limit=None):
            count += 1
        await ctx.send(f"There are {count} messages in {ctx.channel.mention}")

    @commands.command(name="commands", pass_context=True)
    async def commands(self, ctx):
        message = Embed(title="Available Commands (Use prefix '-')", color=0x71368a)
        message.add_field(name="Music Commands", value="**play** - Plays the song provided.\n**pause** - Pause the currently playing song.\n**resume** - Resumes the currently paused song.\n**queue** - Adds the song to queue.\n**listqueue** - Lists all songs in queue.\n**flush** - Clears the queue.\n**skip** - Skips the currently played song.")
        message.add_field(name="Server Stats", value="**totalmessages** - No. of messages in the text channel.\n**owner** - Owner of the server.\n**update** - Alert for new updates to the bot.")
        await ctx.channel.send(embed=message)
    
def setup(bot):
    bot.add_cog(Stats(bot))
