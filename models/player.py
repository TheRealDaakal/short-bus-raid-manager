from dataclasses import dataclass


@dataclass
class Player:
    discord_id: int
    discord_name: str

    character_name: str | None = None
    legacy_name: str | None = None

    player_class: str | None = None
    discipline: str | None = None

    can_tank: bool = False
    can_heal: bool = False
    can_dps: bool = True

    is_main: bool = True

    attendance: float = 0.0