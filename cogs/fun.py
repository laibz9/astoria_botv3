# คำสั่งสนุกๆ เช่น meme, joke, roll dice
import disnake
from disnake.ext import commands, tasks

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"📁 Loaded ({self.__class__.__name__}) Succeed.")

    @commands.command()
    async def roll(self, ctx):
        import random
        await ctx.send(f"🎲 You rolled: {random.randint(1, 6)}")

def setup(bot):
    bot.add_cog(FunCommands(bot))