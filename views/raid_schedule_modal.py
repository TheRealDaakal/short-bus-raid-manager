import discord

from services.raid_storage import create_raid
from services.raid_manager import RaidManager
from views.raid_view import RaidView
from utils.embed_builder import build_raid_embed


class RaidScheduleModal(discord.ui.Modal, title="Schedule a SWTOR Raid"):

    operation = discord.ui.TextInput(
        label="Operation",
        placeholder="Temple of Sacrifice",
        required=True,
        max_length=100,
    )

    difficulty = discord.ui.TextInput(
        label="Difficulty",
        placeholder="Nightmare Mode (NiM)",
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

        # Save the raid to the database
        raid_id = create_raid(
            operation=self.operation.value,
            difficulty=self.difficulty.value,
            raid_date=self.raid_date.value,
            raid_time=self.raid_time.value,
            created_by=interaction.user.id,
        )

        # Create the live raid session
        session = RaidManager.create_session(
            raid_id=raid_id,
            operation=self.operation.value,
            difficulty=self.difficulty.value,
            raid_date=self.raid_date.value,
            raid_time=self.raid_time.value,
            raid_leader=interaction.user.display_name,
        )

        # Tell the officer the raid was created
        await interaction.response.send_message(
            f"✅ Raid #{raid_id} created! Posting signup...",
            ephemeral=True,
        )

        # Post the live signup board
        message = await interaction.channel.send(
            embed=build_raid_embed(session),
            view=RaidView(session.raid_id),
        )

        # Save the Discord message information for future updates
        session.message_id = message.id
        session.channel_id = interaction.channel.id