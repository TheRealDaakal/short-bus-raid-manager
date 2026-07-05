import discord

from utils.constants import OPERATIONS


class OperationSelect(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label=operation,
                value=operation,
            )
            for operation in OPERATIONS
        ]

        super().__init__(
            placeholder="Choose an Operation...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):

        # Save the selected operation to the parent view
        self.view.operation = self.values[0]

        await interaction.response.edit_message(
            content=f"✅ **Operation:** {self.values[0]}",
            view=self.view,
        )