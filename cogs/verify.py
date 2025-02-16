import disnake
from disnake.ext import commands
import json

# โหลดคอนฟิกจาก config.json
with open("config/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# 🔹 กำหนดค่าตัวแปรช่องและ Role ที่ต้องการให้
CHANNEL_ID = config["verify"].get("CHANNEL_ID", False)
ROLE_ID = config["verify"].get("ROLE_ID", False)
RULES_CHANNEL_ID = config["verify"].get("RULES_CHANNEL_ID", False)

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"📁 Loaded ({self.__class__.__name__}) Succeed.")

    @commands.slash_command(description="ส่งข้อความยืนยันตัวตนไปยังห้องที่กำหนด (Admin only)")
    async def sendverify(self, interaction: disnake.AppCmdInter):
        guild = interaction.guild
        channel = guild.get_channel(CHANNEL_ID)
        role = guild.get_role(ROLE_ID)
        rules_channel = guild.get_channel(RULES_CHANNEL_ID)

        is_admin = interaction.author.guild_permissions.administrator
        is_owner = interaction.author.id == interaction.guild.owner_id

        if not is_owner and not is_admin:
            await interaction.response.send_message("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!", ephemeral=True)
            return

        class VerifyButton(disnake.ui.View):
            def __init__(self):
                super().__init__()
                self.button = disnake.ui.Button(
                    label="✅ Verify Me!",
                    style=disnake.ButtonStyle.success,
                    custom_id="verify_button"
                )
                self.button.callback = self.verify_callback
                self.add_item(self.button)

            async def verify_callback(self, interaction: disnake.MessageInteraction):
                member = interaction.author
                if role in member.roles:
                    return await interaction.response.send_message("⚠️ คุณได้รับ Role นี้ไปแล้ว!", ephemeral=True)

                await member.add_roles(role)
                await interaction.response.send_message("✅ คุณได้รับ Role Verified แล้ว! ยินดีต้อนรับ!", ephemeral=True)

        view = VerifyButton()

        embed = disnake.Embed(
            title="🔹 ยินดีต้อนรับสู่เซิร์ฟเวอร์!",
            description="เพื่อเข้าถึงเนื้อหาและห้องแชททั้งหมด กรุณากดยืนยันตัวตนด้านล่าง",
            color=disnake.Color.blue()
        )
        embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.add_field(name="📜 กฎของเซิร์ฟเวอร์", value=f"โปรดปฏิบัติตามกฎของเรา {rules_channel.mention}", inline=False)
        embed.add_field(name="🎉 สิทธิพิเศษ", value="เมื่อยืนยันตัวตนแล้ว คุณจะสามารถเข้าถึงเนื้อหาและกิจกรรมต่างๆ ได้อย่างเต็มที่!", inline=False)
        embed.set_footer(text="หากมีปัญหา โปรดติดต่อแอดมิน 👨‍💻")

        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"✅ ส่งข้อความยืนยันตัวตนไปยัง {channel.mention} เรียบร้อย!", ephemeral=True)

def setup(bot):
    bot.add_cog(Verify(bot))