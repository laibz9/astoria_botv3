import disnake
from disnake.ext import commands
import json

# โหลดคอนฟิกจาก config.json
with open("config/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# 🔹 กำหนดค่าตัวแปร
GUILD_IDS = config.get("guild_ids", [])
CHANNEL_ID = config["channel"].get("verify_channel_id", None)
ROLE_IDS = [
    config["roles"].get("verified", None),
    config["roles"].get("member", None)
]
RULES_CHANNEL_ID = config["channel"].get("rules_channel_id", None)

class VerifyButton(disnake.ui.View):
    def __init__(self, roles: list, timeout=None):  # ปิด timeout
        super().__init__(timeout=timeout)  # ไม่ให้หมดอายุ
        self.roles = roles

    @disnake.ui.button(label="✅ Verify Me!", style=disnake.ButtonStyle.success, custom_id="verify_button")
    async def verify_callback(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        member = interaction.user
        for role in self.roles:
            if role in member.roles:
                return await interaction.response.send_message(f"⚠️ คุณได้รับ Role {role.mention} ไปแล้ว!", ephemeral=True)

        await member.add_roles(*self.roles)
        await interaction.response.send_message("✅ คุณได้รับ Role Verified แล้ว! ยินดีต้อนรับ!", ephemeral=True)

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"📁 Loaded ({self.__class__.__name__}) Succeed.")

        for guild_id in GUILD_IDS:
            guild = self.bot.get_guild(guild_id)  # ดึง guild ตาม ID
            if not guild:
                print(f"❌ ไม่พบเซิร์ฟเวอร์ ID: {guild_id}")
                return

            channel = guild.get_channel(CHANNEL_ID)
            rules_channel = guild.get_channel(RULES_CHANNEL_ID)

            # กรอง role ที่เป็น None ออก
            roles = [guild.get_role(role_id) for role_id in ROLE_IDS if role_id]
            if not channel or not roles or not rules_channel:
                print(f"❌ ไม่พบ Channel หรือ Role ที่จำเป็นในเซิร์ฟเวอร์: {guild.name}")
                return

            embed = disnake.Embed(
                title="🔹 ยินดีต้อนรับสู่เซิร์ฟเวอร์!",
                description="เพื่อเข้าถึงเนื้อหาและห้องแชททั้งหมด กรุณากดยืนยันตัวตนด้านล่าง",
                color=disnake.Color.blue()
            )
            embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
            embed.add_field(name="📜 กฎของเซิร์ฟเวอร์", value=f"โปรดปฏิบัติตามกฎของเรา {rules_channel.mention}", inline=False)
            embed.add_field(name="🎉 สิทธิพิเศษ", value="เมื่อยืนยันตัวตนแล้ว คุณจะสามารถเข้าถึงเนื้อหาและกิจกรรมต่างๆ ได้อย่างเต็มที่!", inline=False)
            embed.set_footer(text="หากมีปัญหา โปรดติดต่อแอดมิน 👨‍💻")

            # ตรวจสอบว่ามีข้อความที่ส่งไปแล้วในช่องนั้นไหม
            async for message in channel.history(limit=10):
                if message.author == self.bot.user and message.embeds:
                    await message.edit(view=VerifyButton(roles))
                    print(f"✅ อัปเดตปุ่มใน ({channel})")
                    return

            # ถ้าไม่มีข้อความที่มีปุ่มในช่องนั้น ให้ส่งข้อความใหม่
            await channel.send(embed=embed, view=VerifyButton(roles))
            print(f"✅ ส่งข้อความยืนยันตัวตนไปยัง {channel.name} เรียบร้อย!")

def setup(bot):
    bot.add_cog(Verify(bot))
