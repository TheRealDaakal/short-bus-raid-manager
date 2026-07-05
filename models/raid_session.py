from models.raid_member import RaidMember


class RaidSession:
    def __init__(
        self,
        operation,
        difficulty="",
        raid_date="",
        raid_time="",
        raid_leader="",
        raid_leader_id=None,
        raid_id=None,
    ):
        self.raid_id = raid_id

        self.operation = operation
        self.difficulty = difficulty
        self.raid_date = raid_date
        self.raid_time = raid_time

        self.raid_leader = raid_leader
        self.raid_leader_id = raid_leader_id

        # Raid Status
        self.locked = False
        self.completed = False

        # Discord Message Tracking
        self.message_id = None
        self.channel_id = None

        # Raid Members
        self.tanks: list[RaidMember] = []
        self.healers: list[RaidMember] = []
        self.dps: list[RaidMember] = []
        self.bench: list[RaidMember] = []

    def remove_player(self, user_id: int):

        self.tanks = [
            player for player in self.tanks
            if player.id != user_id
        ]

        self.healers = [
            player for player in self.healers
            if player.id != user_id
        ]

        self.dps = [
            player for player in self.dps
            if player.id != user_id
        ]

        self.bench = [
            player for player in self.bench
            if player.id != user_id
        ]