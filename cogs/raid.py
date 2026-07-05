import random

import discord
from discord import app_commands
from discord.ext import commands

from services.raid_manager import RaidManager
from views.raid_view import RaidView
from views.raid_schedule_modal import RaidScheduleModal
from utils.embed_builder import build_raid_embed
from utils.constants import OPERATIONS

print(">>> raid.py loaded <<<")


class Raid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    raid = app_commands.Group(
        name="raid",
        description="Raid management"
    )

    @raid.command(
        name="spin",
        description="Spin the SWTOR Operations Wheel"
    )
    async def spin(self, interaction: discord.Interaction):

        operation = random.choice(OPERATIONS)

        raid_id = random.randint(100000, 999999)

        session = RaidManager.create_session(
            raid_id=raid_id,
            operation=operation,
        )

        await interaction.response.send_message(
            embed=build_raid_embed(session),
            view=RaidView(raid_id)
        )

        message = await interaction.original_response()

        session.message = message
        session.message_id = message.id
        session.channel_id = message.channel.id

    @raid.command(
        name="schedule",
        description="Schedule a new raid"
    )
    async def schedule(self, interaction: discord.Interaction):

        await interaction.response.send_modal(
            RaidScheduleModal()
        )


async def setup(bot):
    await bot.add_cog(Raid(bot))