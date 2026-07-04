import discord

from services.raid_storage import create_raid


class RaidScheduleModal(discord.ui.Modal, title="Schedule a SWTOR Raid"):

    operation = discord.ui.TextInput(
        label="Operation",
        placeholder="Temple of Sacrifice",
        required=True,
        max_length=100,
    )

    difficulty = discord.ui.TextInput(
        label="Difficulty",
        placeholder="Master Mode",
        required=True,
        max_length=50,
    )

    raid_date = discord.ui.TextInput(
        label="Raid Date",
        placeholder="2026-07-10",
        required=True,
        max_length=20,
    )

    raid_time = discord.ui.TextInput(
        label="Raid Time",
        placeholder="8:00 PM CST",
        required=True,
        max_length=20,
    )

    async def on_submit(self, interaction: discord.Interaction):

        raid_id = create_raid(
            operation=self.operation.value,
            difficulty=self.difficulty.value,
            raid_date=self.raid_date.value,
            raid_time=self.raid_time.value,
            created_by=interaction.user.id,
        )

        embed = discord.Embed(
            title="✅ Raid Scheduled",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Operation",
            value=self.operation.value,
            inline=True
        )

        embed.add_field(
            name="Difficulty",
            value=self.difficulty.value,
            inline=True
        )

        embed.add_field(
            name="Date",
            value=self.raid_date.value,
            inline=True
        )

        embed.add_field(
            name="Time",
            value=self.raid_time.value,
            inline=True
        )

        embed.set_footer(text=f"Raid ID: {raid_id}")

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )