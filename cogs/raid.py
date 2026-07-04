import random

import discord
from discord import app_commands
from discord.ext import commands

from models.raid_session import RaidSession
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

        session = RaidSession(operation)

        await interaction.response.send_message(
            embed=build_raid_embed(session),
            view=RaidView(session)
        )

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