# คำสั่งทั่วไป เช่น ping, hello
import disnake
from disnake.ext import commands, tasks
import json

# โหลดคอนฟิกจาก config.json
with open("config/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"📁 Loaded ({self.__class__.__name__}) Succeed.")

    @commands.command()
    async def ping(self, ctx):
        latency = round(ctx.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latency: `{latency}ms`")

    @commands.slash_command(guild_ids=config["guild_ids"], description="Check bot latency.")
    async def ping_slash_command(self, ctx):
        latency = round(ctx.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latency: `{latency}ms`")

def setup(bot):
    bot.add_cog(GeneralCommands(bot))