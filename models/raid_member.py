from dataclasses import dataclass

import discord


@dataclass
class RaidMember:
    """
    Represents a player signed up for a raid.
    """

    member: discord.Member

    combat_style: str = ""
    discipline: str = ""

    @property
    def id(self) -> int:
        return self.member.id

    @property
    def display_name(self) -> str:
        return self.member.display_name

    def summary(self) -> str:
        if self.combat_style and self.discipline:
            return (
                f"{self.display_name}\n"
                f"{self.combat_style} • {self.discipline}"
            )

        return self.display_name