import disnake
from disnake.ext import commands
import json

# โหลดคอนฟิกจาก config.json
with open("config/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"📁 Loaded ({self.__class__.__name__}) Succeed.")

# Purge Message
    @commands.slash_command(
        guild_ids=config["guild_ids"],
        default_permissions=False,
        name="purge",
        description="คำสั่งสำหรับลบข้อความในช่องแชทจำนวนที่ระบุ (Admin only)"
    )
    async def purge(self, interaction: disnake.AppCmdInter, number: int):
        # ตรวจสอบว่าจำนวนที่ป้อนมาต้องมากกว่า 0
        if number <= 0:
            await interaction.response.send_message("❌ โปรดระบุจำนวนข้อความที่มากกว่า 0!", ephemeral=True)
            return

        # ดึงค่า role ของ moderator จาก config
        moderators = config.get("roles", {}).get("moderators", [])

        # ถ้าเป็น int ให้แปลงเป็น list
        if isinstance(moderators, int):
            moderators = [moderators]
        elif not isinstance(moderators, list):
            moderators = []  # ป้องกัน error ถ้าข้อมูลผิดพลาด

        # ตรวจสอบว่ายูเซอร์มี role ที่อนุญาต
        has_role = any(disnake.utils.get(interaction.user.roles, id=role_id) for role_id in moderators)
        is_admin = interaction.user.guild_permissions.administrator
        is_owner = interaction.user.id == interaction.guild.owner_id

        if not has_role and not is_admin and not is_owner:
            await interaction.response.send_message("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!", ephemeral=True)
            return

        # ใช้ defer() เพื่อป้องกัน timeout
        await interaction.response.defer(ephemeral=True)

        # ลบข้อความ
        deleted_messages = await interaction.channel.purge(limit=number)
        await interaction.followup.send(f"✅ ลบข้อความไปแล้ว {len(deleted_messages)} ข้อความ!", ephemeral=True)

def setup(bot):
    bot.add_cog(ModerationCommands(bot))
