# คำสั่งสำหรับแอดมิน เช่น kick, ban, mute
import disnake
from disnake.ext import commands
import json

# โหลดคอนฟิกจาก config.json
with open("config/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"📁 Loaded ({self.__class__.__name__}) Succeed.")

    # คำสั่ง Kick
    @commands.slash_command(guild_ids=config["guild_ids"], name="kick", description="Kick a user from the server")
    async def kick(self, interaction: disnake.AppCmdInter, member: disnake.Member, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("You do not have permission to kick members.", ephemeral=True)
            return
        
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.name} has been kicked for: {reason}")

    # คำสั่ง Ban
    @commands.slash_command(guild_ids=config["guild_ids"], name="ban", description="Ban a user from the server")
    async def ban(self, interaction: disnake.AppCmdInter, member: disnake.Member, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("You do not have permission to ban members.", ephemeral=True)
            return
        
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member.name} has been banned for: {reason}")

    # คำสั่ง Mute
    @commands.slash_command(guild_ids=config["guild_ids"], name="mute", description="Mute a user in the server")
    async def mute(self, interaction: disnake.AppCmdInter, member: disnake.Member, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("You do not have permission to mute members.", ephemeral=True)
            return
        
        mute_role = disnake.utils.get(interaction.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await interaction.guild.create_role(name="Muted", permissions=disnake.Permissions(send_messages=False))
        
        await member.add_roles(mute_role, reason=reason)
        await interaction.response.send_message(f"{member.name} has been muted for: {reason}")

def setup(bot):
    bot.add_cog(AdminCommands(bot))