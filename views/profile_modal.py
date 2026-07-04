import discord

from services.player_service import save_player_profile


class ProfileModal(discord.ui.Modal, title="Create Your SWTOR Profile"):

    character = discord.ui.TextInput(
        label="Character Name",
        placeholder="Darth Jawa",
        required=True,
        max_length=32,
    )

    legacy = discord.ui.TextInput(
        label="Legacy Name",
        placeholder="The Short Bus",
        required=False,
        max_length=32,
    )

    player_class = discord.ui.TextInput(
        label="Class",
        placeholder="Mercenary, Juggernaut, Sorcerer...",
        required=True,
        max_length=32,
    )

    discipline = discord.ui.TextInput(
        label="Discipline",
        placeholder="Arsenal, Vengeance, Madness...",
        required=True,
        max_length=32,
    )

    async def on_submit(self, interaction: discord.Interaction):

        save_player_profile(
            discord_id=interaction.user.id,
            character_name=str(self.character),
            legacy_name=str(self.legacy),
            player_class=str(self.player_class),
            discipline=str(self.discipline),
        )

        embed = discord.Embed(
            title="✅ Profile Saved",
            description="Your SWTOR profile has been updated.",
            color=discord.Color.green(),
        )

        embed.add_field(
            name="Character",
            value=str(self.character),
            inline=True,
        )

        embed.add_field(
            name="Legacy",
            value=str(self.legacy) or "None",
            inline=True,
        )

        embed.add_field(
            name="Class",
            value=str(self.player_class),
            inline=True,
        )

        embed.add_field(
            name="Discipline",
            value=str(self.discipline),
            inline=True,
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )