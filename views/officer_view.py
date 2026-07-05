import discord

from services.raid_manager import RaidManager
from services.permission_service import PermissionService


class OfficerView(discord.ui.View):
    def __init__(self, raid_id: int):
        super().__init__(timeout=None)

        self.raid_id = raid_id

    @property
    def session(self):
        return RaidManager.get_session(self.raid_id)

    @discord.ui.button(
        label="🔒 Lock Raid",
        style=discord.ButtonStyle.danger,
    )
    async def lock(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):

        if not PermissionService.is_officer(interaction.user):
            await interaction.response.send_message(
                "❌ Only raid officers can lock raids.",
                ephemeral=True,
            )
            return

        RaidManager.lock_raid(self.session)

        await interaction.response.send_message(
            "🔒 Raid locked.",
            ephemeral=True,
        )

    @discord.ui.button(
        label="🔓 Unlock Raid",
        style=discord.ButtonStyle.success,
    )
    async def unlock(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):

        if not PermissionService.is_officer(interaction.user):
            await interaction.response.send_message(
                "❌ Only raid officers can unlock raids.",
                ephemeral=True,
            )
            return

        RaidManager.unlock_raid(self.session)

        await interaction.response.send_message(
            "🔓 Raid unlocked.",
            ephemeral=True,
        )

    @discord.ui.button(
        label="🏁 Finish Raid",
        style=discord.ButtonStyle.primary,
    )
    async def finish(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):

        if not PermissionService.is_officer(interaction.user):
            await interaction.response.send_message(
                "❌ Only raid officers can finish raids.",
                ephemeral=True,
            )
            return

        RaidManager.finish_raid(self.raid_id)

        await interaction.response.send_message(
            "🏁 Raid finished.",
            ephemeral=True,
        )