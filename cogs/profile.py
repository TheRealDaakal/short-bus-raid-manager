import discord
from discord import app_commands
from discord.ext import commands

from services.player_service import get_player
from views.profile_modal import ProfileModal
from views.profile_view import ProfileView


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="profile",
        description="View your SWTOR profile"
    )
    async def profile(self, interaction: discord.Interaction):

        player = get_player(interaction.user.id)

        # No profile yet
        if (
            player is None
            or player.character_name is None
        ):
            await interaction.response.send_modal(ProfileModal())
            return

        embed = discord.Embed(
            title="🤎 Short Bus Jawa Profile",
            color=discord.Color.orange()
        )

        embed.add_field(
            name="Discord",
            value=player.discord_name,
            inline=False
        )

        embed.add_field(
            name="Character",
            value=player.character_name,
            inline=True
        )

        embed.add_field(
            name="Legacy",
            value=player.legacy_name or "Not Set",
            inline=True
        )

        embed.add_field(
            name="Class",
            value=player.player_class or "Not Set",
            inline=True
        )

        embed.add_field(
            name="Discipline",
            value=player.discipline or "Not Set",
            inline=True
        )

        embed.add_field(
            name="Attendance",
            value=f"{player.attendance:.1f}%",
            inline=False
        )

        await interaction.response.send_message(
            embed=embed,
            view=ProfileView(),
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(Profile(bot))