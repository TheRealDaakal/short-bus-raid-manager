import calendar
from datetime import datetime

import discord

from utils.wizard_embed_builder import build_wizard_embed

_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


class MonthSelect(discord.ui.Select):
    def __init__(self, session):
        options = [
            discord.SelectOption(label=name, value=str(i + 1), default=(session.wizard_month == i + 1))
            for i, name in enumerate(_MONTHS)
        ]

        super().__init__(placeholder="Month...", options=options, row=0)

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        session = view.session

        session.wizard_month = int(self.values[0])

        await _advance_if_ready(interaction, view, session)


class _DaySelectBase(discord.ui.Select):
    """
    Discord caps a select at 25 options, and months can have up to 31
    days, so Day is split across two selects (1-25, 26-31) rather than
    one - the year (needed to know exact days-in-month) also isn't known
    until both Month and Day are picked anyway, see _advance_if_ready.
    """

    def __init__(self, session, days: range, row: int):
        options = [
            discord.SelectOption(label=str(d), value=str(d), default=(session.wizard_day == d))
            for d in days
        ]

        super().__init__(placeholder=f"Day ({days[0]}-{days[-1]})...", options=options, row=row)

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        session = view.session

        session.wizard_day = int(self.values[0])

        await _advance_if_ready(interaction, view, session)


class DaySelectLow(_DaySelectBase):
    def __init__(self, session):
        super().__init__(session, range(1, 26), row=1)


class DaySelectHigh(_DaySelectBase):
    def __init__(self, session):
        super().__init__(session, range(26, 32), row=2)


async def _advance_if_ready(interaction: discord.Interaction, view, session):
    if session.wizard_month is None or session.wizard_day is None:
        # Only one of the two picked so far - just reflect the choice
        # and stay on this step until both are set.
        view.refresh()
        await interaction.response.edit_message(embed=build_wizard_embed(session), view=view)
        return

    now = datetime.utcnow()
    year = now.year

    day = min(session.wizard_day, calendar.monthrange(year, session.wizard_month)[1])
    candidate = datetime(year, session.wizard_month, day)

    if candidate.date() < now.date():
        # That date already passed this year - assume they mean next year.
        year += 1
        day = min(session.wizard_day, calendar.monthrange(year, session.wizard_month)[1])
        candidate = datetime(year, session.wizard_month, day)

    session.raid_date = candidate.strftime("%m/%d/%Y")
    session.wizard_month = None
    session.wizard_day = None
    session.step = 6

    view.refresh()
    await interaction.response.edit_message(embed=build_wizard_embed(session), view=view)
