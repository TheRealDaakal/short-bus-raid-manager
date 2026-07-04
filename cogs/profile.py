import discord
from discord import app_commands
from discord.ext import commands

from views.profile_modal import ProfileModal


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="profile",
        description="Create or edit your SWTOR profile"
    )
    async def profile(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ProfileModal())


async def setup(bot):
    await bot.add_cog(Profile(bot))