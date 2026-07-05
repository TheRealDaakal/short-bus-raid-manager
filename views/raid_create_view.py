import discord

from views.operation_select import OperationSelect
from views.difficulty_select import DifficultySelect


class RaidCreateView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

        self.operation = None
        self.difficulty = None

        self.add_item(OperationSelect())
        self.add_item(DifficultySelect())

    @discord.ui.button(
        label="Create Raid",
        style=discord.ButtonStyle.green,
        emoji="✅",
        row=2,
    )
    async def create_raid(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):

        if self.operation is None:
            await interaction.response.send_message(
                "Please select an Operation first.",
                ephemeral=True,
            )
            return

        if self.difficulty is None:
            await interaction.response.send_message(
                "Please select a Difficulty first.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"""✅ Raid Creation Started

**Operation**
{self.operation}

**Difficulty**
{self.difficulty}

(Date and Time will be added next.)""",
            ephemeral=True,
        )