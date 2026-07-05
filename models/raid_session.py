class RaidSession:
    def __init__(
        self,
        operation,
        difficulty="",
        raid_date="",
        raid_time="",
        raid_leader="",
        raid_id=None,
    ):
        self.raid_id = raid_id

        self.operation = operation
        self.difficulty = difficulty
        self.raid_date = raid_date
        self.raid_time = raid_time
        self.raid_leader = raid_leader

        # Raid Status
        self.locked = False
        self.completed = False

        # Discord message ID (used later for live updates)
        self.message_id = None

        # Signup Lists
        self.tanks = []
        self.healers = []
        self.dps = []
        self.bench = []

    def remove_player(self, user_id):
        self.tanks = [p for p in self.tanks if p.id != user_id]
        self.healers = [p for p in self.healers if p.id != user_id]
        self.dps = [p for p in self.dps if p.id != user_id]
        self.bench = [p for p in self.bench if p.id != user_id]