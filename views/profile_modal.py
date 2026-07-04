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
            discord_name=str(interaction.user),
            character_name=self.character.value,
            legacy_name=self.legacy.value,
            player_class=self.player_class.value,
            discipline=self.discipline.value,
        )

        embed = discord.Embed(
            title="✅ Profile Saved!",
            description="Your SWTOR profile has been saved successfully.",
            color=discord.Color.green(),
        )

        embed.add_field(
            name="Character",
            value=self.character.value,
            inline=True,
        )

        embed.add_field(
            name="Legacy",
            value=self.legacy.value or "Not Set",
            inline=True,
        )

        embed.add_field(
            name="Class",
            value=self.player_class.value,
            inline=True,
        )

        embed.add_field(
            name="Discipline",
            value=self.discipline.value,
            inline=True,
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )