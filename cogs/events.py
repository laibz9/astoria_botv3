# Event listeners เช่น on_message, on_member_join
import disnake
from disnake.ext import commands, tasks
import datetime


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
    @tasks.loop(minutes=3)  # ตั้งเวลาให้ทำงานทุกๆ 3 นาที
    async def clear_messages(self):
        self.channel_id = 1338384698380128326  # Channel ID
        self.exempt_message_id = 1340587021189779499  # ข้อความที่ต้องการยกเว้นจากการลบ
        if self.channel_id is None:
            return
        
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            # ตรวจสอบข้อความที่ตรงกับเงื่อนไขก่อน
            messages = await channel.history(limit=100).flatten()  # กำหนดจำนวนข้อความที่ต้องการดึงมา
            filtered_messages = [msg for msg in messages if msg.id != self.exempt_message_id]
            
            if filtered_messages:
                # ถ้ามีข้อความที่ตรงกับเงื่อนไขก็ให้ลบ
                await channel.purge(check=lambda msg: msg.id != self.exempt_message_id)
                print(f"📌 ลบข้อความในห้อง {channel.name} แล้ว")
    
    @clear_messages.before_loop
    async def before_clear_messages(self):
        await self.bot.wait_until_ready()  # รอให้บอทพร้อมก่อนเริ่มทำงาน

def setup(bot):
# Join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"➕ {member} join the server!")
        RULES_CHANNEL_ID = 1338224430219919380
        WELCOME_CHANNEL_ID = 1338376280428773397
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        rules_channel = self.bot.get_channel(RULES_CHANNEL_ID)
        if channel and rules_channel:
            embed = disnake.Embed(
                title="🎉 ยินดีต้อนรับ!",
                description=f"👋 สวัสดี {member.mention}!\n"
                            "เราดีใจที่คุณเข้าร่วมกับเรา 💖\n\n"
                            f"📌 กรุณาอ่านกฎของเซิร์ฟเวอร์ที่นี่: {rules_channel.mention}\n"
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
            embed.set_image(url="https://i0.wp.com/www.galvanizeaction.org/wp-content/uploads/2022/06/Wow-gif.gif?fit=450%2C250&ssl=1")

            # ส่งข้อความไปยังช่องที่กำหนด
            await channel.send(embed=embed)
        else:
            print(f"❌ Error: Channel ID {WELCOME_CHANNEL_ID} or {RULES_CHANNEL_ID} not found.")

# Leave
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"➖ {member} has left the server!")
        LEAVE_CHANNEL_ID = 1338376280428773397  # ใส่ ID ของช่องที่คุณต้องการให้บอทส่งข้อความ
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
            embed.set_image(url="https://media1.giphy.com/media/PiceuRrhk1nshZDduv/giphy.gif?cid=6c09b952r5al7nzzqz996hl8hucr0vaelfvc4o9f69wwqvvn&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g")

            # ส่งข้อความไปยังช่องที่กำหนด
            await channel.send(embed=embed)
        else:
            print(f"❌ Error: Channel ID {LEAVE_CHANNEL_ID} not found.")

def setup(bot):
    bot.add_cog(Events(bot))