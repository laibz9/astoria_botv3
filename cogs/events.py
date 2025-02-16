# Event listeners เช่น on_message, on_member_join
import disnake
from disnake.ext import commands, tasks
import datetime
import json

# โหลดคอนฟิกจาก config.json
with open("config/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clear_messages.start()  # เริ่ม task เมื่อลงทะเบียน Cog

    def cog_unload(self):
        self.clear_messages.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"📁 Loaded ({self.__class__.__name__}) Succeed.")

# Auto remove message in channel every 3 minutes
    @tasks.loop(minutes=3)  # ตั้งเวลาให้ทำงาน
    async def clear_messages(self):
        # Channel ID
        self.channel_id = config["channel"].get("command_channel_id", False)
        # ข้อความที่ต้องการยกเว้นจากการลบ
        self.exempt_message_id = config["message"].get("exempt_message_id", False)
        if self.channel_id is None:
            return
        
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            # ตรวจสอบข้อความที่ตรงกับเงื่อนไขก่อน
            messages = await channel.history(limit=100).flatten()
            filtered_messages = [msg for msg in messages if msg.id != self.exempt_message_id]
            
            if filtered_messages:
                # ถ้ามีข้อความที่ตรงกับเงื่อนไขก็ให้ลบ
                await channel.purge(check=lambda msg: msg.id != self.exempt_message_id)
                print(f"📌 ลบข้อความในห้อง {channel.name} แล้ว")
    
    @clear_messages.before_loop
    async def before_clear_messages(self):
        await self.bot.wait_until_ready()

# Join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"➕ {member} join the server!")
        WELCOME_CHANNEL_ID = config["channel"].get("welcome_channel_id", False)
        RULES_CHANNEL_ID = config["channel"].get("rules_channel_id", False)
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        rules_channel = self.bot.get_channel(RULES_CHANNEL_ID)
        if channel and rules_channel:
            embed = disnake.Embed(
                title="🎉 ยินดีต้อนรับ!",
                description=f"👋 สวัสดี {member.mention}!\n"
                            "เราดีใจที่คุณเข้าร่วมกับเรา 💖\n\n"
                            f"📌 กรุณาอ่านกฎของเซิร์ฟเวอร์: {rules_channel.mention}\n"
                            "✨ มาทำความรู้จักกันและสนุกไปด้วยกันเถอะ!",
                color=disnake.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.set_footer(text="เราหวังว่าคุณจะมีช่วงเวลาที่ดี!")
            icon_url = None
            if self.bot.user:
                icon_url = self.bot.user.avatar.url if self.bot.user.avatar else self.bot.user.default_avatar.url
            embed.set_author(name="Astoria", icon_url=icon_url)
            embed.set_image(url="https://cdn.discordapp.com/attachments/1340681369000607869/1340683537786867824/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f6734304331744352746b464157513d3d2d313233343136323632342e313666366434343536363131386337653737393032.gif?ex=67b34058&is=67b1eed8&hm=1095df4f8936d8caed9b4e253bac0fec805cc052f97255252218fe0a65562b4d&")

            await channel.send(embed=embed)
        else:
            print(f"❌ Error: Channel ID {WELCOME_CHANNEL_ID} or {RULES_CHANNEL_ID} not found.")

# Leave
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"➖ {member} has left the server!")
        LEAVE_CHANNEL_ID = config["channel"].get("leave_channel_id", False)
        channel = self.bot.get_channel(LEAVE_CHANNEL_ID)

        if channel:
            embed = disnake.Embed(
                title="👋 ลาก่อน!",
                description=f"😢 ไม่นะคุณ {member.mention}!\n"
                            "ได้ออกจากเซิร์ฟเวอร์แล้ว...\n"
                            "ขอให้โชคดีและหวังว่าจะได้พบกันอีกนะ! 💔\n"
                            "ถ้าอยากกลับมาเมื่อไหร่ เรายินดีต้อนรับเสมอ! 🤗",
                color=disnake.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.set_footer(text="เราหวังว่าคุณจะมีช่วงเวลาที่ดี!")
            icon_url = self.bot.user.avatar.url if self.bot.user.avatar else self.bot.user.default_avatar.url
            embed.set_author(name="Astoria", icon_url=icon_url)
            embed.set_image(url="https://cdn.discordapp.com/attachments/1340681369000607869/1340683538441175101/4c441d3e17bdc8f0654a3ebad8c4b217c7a15652_hq.gif?ex=67b34058&is=67b1eed8&hm=7cdffa8deb963e3041bc3123e205138b7e63e847ec6038e3b9c1094a16d4bb3e&")

            await channel.send(embed=embed)
        else:
            print(f"❌ Error: Channel ID {LEAVE_CHANNEL_ID} not found.")

def setup(bot):
    bot.add_cog(Events(bot))