import discord

from utils.constants import DIFFICULTIES


class DifficultySelect(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label=difficulty,
                value=difficulty,
            )
            for difficulty in DIFFICULTIES
        ]

        super().__init__(
            placeholder="Choose a Difficulty...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):

        # Save the selected difficulty to the parent view
        self.view.difficulty = self.values[0]

        await interaction.response.edit_message(
            content=(
                f"✅ **Operation:** {self.view.operation or 'Not selected'}\n"
                f"✅ **Difficulty:** {self.values[0]}"
            ),
            view=self.view,
        )