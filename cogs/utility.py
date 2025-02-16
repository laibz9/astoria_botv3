# คำสั่งเครื่องมือ เช่น serverinfo, userinfo
import disnake
from disnake.ext import commands, tasks

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"📁 Loaded ({self.__class__.__name__}) Succeed.")

    @commands.command()
    async def userinfo(self, ctx, member: disnake.Member = None):
        member = member or ctx.author
        embed = disnake.Embed(title=f"{member}", description=f"ID: {member.id}", color=disnake.Color.blue())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))