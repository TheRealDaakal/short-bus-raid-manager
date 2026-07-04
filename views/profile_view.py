import discord

from .profile_modal import ProfileModal


class ProfileView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Edit Profile",
        emoji="✏️",
        style=discord.ButtonStyle.primary,
    )
    async def edit_profile(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.response.send_modal(ProfileModal())