import json
import random
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_greetings(self):
        with open('config.json') as file_handle:
            cmds = json.load(file_handle)
        return cmds

    @commands.command(pass_context=True)
    async def hello(self, ctx):
        greet = random.choice(self.get_greetings()["greeting"])
        await ctx.channel.send(f"{greet} {ctx.message.author.mention}")

async def setup(bot):
    await bot.add_cog(Greetings(bot))
