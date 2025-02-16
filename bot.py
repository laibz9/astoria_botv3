import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv
import json

# โหลดคอนฟิกจาก config.json
with open("config/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
# โหลด Token .env 
load_dotenv("config/.env")

# ตั้งค่า intents ใน config
intents = disnake.Intents.default()
intents.messages = config["intents"].get("messages", False)
intents.members = config["intents"].get("members", False)
intents.guilds = config["intents"].get("guilds", False)
intents.message_content = config["intents"].get("message_content", False)

# เปิดการดีบักซิงค์คำสั่ง
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

class astoria_bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.TOKEN = os.getenv("TOKEN")
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["prefix"]),
            command_sync_flags=command_sync_flags,
            intents = intents,
            *args,
            **kwargs
        )

bot = astoria_bot(owner_id=config["owner_id"], case_insensitive=True)

@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user} is ready!')

# โหลด cogs จากโฟลเดอร์ cogs/
if __name__ == "__main__":
    for file in os.listdir('./cogs'):
        if file.endswith('.py') and not file.startswith('_') and file != "__init__.py":
            try:
                bot.load_extension(f'cogs.{file[:-3]}')  # เอา ".py" ออก
            except Exception as e:
                print(f"❌ Failed to load {file}: {e}")

    bot.run(bot.TOKEN)