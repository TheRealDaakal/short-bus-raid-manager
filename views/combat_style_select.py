import discord

from utils.swtor_data import COMBAT_STYLES


class CombatStyleSelect(discord.ui.Select):
    def __init__(self, role: str):

        self.role = role

        options = [
            discord.SelectOption(
                label=style,
                value=style,
            )
            for style in COMBAT_STYLES[role].keys()
        ]

        super().__init__(
            placeholder=f"Choose a {role} Combat Style...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):

        combat_style = self.values[0]

        await interaction.response.send_message(
            f"✅ Selected **{combat_style}**\n\n"
            "Discipline selection is next.",
            ephemeral=True,
        )


class CombatStyleView(discord.ui.View):
    def __init__(self, role: str):
        super().__init__(timeout=120)

        self.add_item(
            CombatStyleSelect(role)
        )