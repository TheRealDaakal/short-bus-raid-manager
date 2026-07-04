from dataclasses import dataclass
from datetime import datetime


@dataclass
class Raid:
    id: int | None = None

    operation: str = ""
    difficulty: str = "NiM"

    raid_date: str = ""
    raid_time: str = ""

    created_by: int = 0

    tanks_needed: int = 2
    healers_needed: int = 2
    dps_needed: int = 4

    created_at: datetime | None = None