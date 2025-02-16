# จัดการข้อผิดพลาดของบอท
import disnake
from disnake.ext import commands, tasks

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"📁 Loaded ({self.__class__.__name__}) Succeed.")

def setup(bot):
    bot.add_cog(ErrorHandler(bot))