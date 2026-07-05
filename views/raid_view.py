import discord
from discord.ui import View, Button

from services.raid_manager import RaidManager
from utils.embed_builder import build_raid_embed


class RaidView(View):
    def __init__(self, raid_id: int):
        super().__init__(timeout=None)

        self.raid_id = raid_id

    @property
    def session(self):
        return RaidManager.get_session(self.raid_id)

    @discord.ui.button(label="🛡 Tank", style=discord.ButtonStyle.blurple)
    async def tank(self, interaction: discord.Interaction, button: Button):

        if not RaidManager.join_tank(self.session, interaction.user):
            await interaction.response.send_message(
                "🛡 Tank role is already full!",
                ephemeral=True,
            )
            return

        await interaction.response.edit_message(
            embed=build_raid_embed(self.session),
            view=self,
        )

    @discord.ui.button(label="⚕️ Healer", style=discord.ButtonStyle.green)
    async def healer(self, interaction: discord.Interaction, button: Button):

        if not RaidManager.join_healer(self.session, interaction.user):
            await interaction.response.send_message(
                "⚕️ Healer role is already full!",
                ephemeral=True,
            )
            return

        await interaction.response.edit_message(
            embed=build_raid_embed(self.session),
            view=self,
        )

    @discord.ui.button(label="⚔ DPS", style=discord.ButtonStyle.red)
    async def dps(self, interaction: discord.Interaction, button: Button):

        if not RaidManager.join_dps(self.session, interaction.user):
            await interaction.response.send_message(
                "⚔ DPS role is already full!",
                ephemeral=True,
            )
            return

        await interaction.response.edit_message(
            embed=build_raid_embed(self.session),
            view=self,
        )

    @discord.ui.button(label="🪑 Bench", style=discord.ButtonStyle.secondary)
    async def bench(self, interaction: discord.Interaction, button: Button):

        RaidManager.join_bench(self.session, interaction.user)

        await interaction.response.edit_message(
            embed=build_raid_embed(self.session),
            view=self,
        )

    @discord.ui.button(label="❌ Leave", style=discord.ButtonStyle.gray)
    async def leave(self, interaction: discord.Interaction, button: Button):

        RaidManager.leave(self.session, interaction.user)

        await interaction.response.edit_message(
            embed=build_raid_embed(self.session),
            view=self,
        )