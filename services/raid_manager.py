from models.raid_session import RaidSession


class RaidManager:

    active_raids: dict[int, RaidSession] = {}

    # -------------------------
    # Session Management
    # -------------------------

    @classmethod
    def create_session(
        cls,
        raid_id: int,
        operation: str,
        difficulty: str = "",
        raid_date: str = "",
        raid_time: str = "",
        raid_leader: str = "",
    ):

        session = RaidSession(
            operation=operation,
            difficulty=difficulty,
            raid_date=raid_date,
            raid_time=raid_time,
            raid_leader=raid_leader,
            raid_id=raid_id,
        )

        cls.active_raids[raid_id] = session

        return session

    @classmethod
    def get_session(cls, raid_id):

        return cls.active_raids.get(raid_id)

    @classmethod
    def remove_session(cls, raid_id):

        cls.active_raids.pop(raid_id, None)

    # -------------------------
    # Signup Logic
    # -------------------------

    @classmethod
    def join_tank(cls, session, user):

        session.remove_player(user.id)

        if len(session.tanks) >= 2:
            return False

        session.tanks.append(user)
        return True

    @classmethod
    def join_healer(cls, session, user):

        session.remove_player(user.id)

        if len(session.healers) >= 2:
            return False

        session.healers.append(user)
        return True

    @classmethod
    def join_dps(cls, session, user):

        session.remove_player(user.id)

        if len(session.dps) >= 4:
            return False

        session.dps.append(user)
        return True

    @classmethod
    def join_bench(cls, session, user):

        session.remove_player(user.id)
        session.bench.append(user)
        return True

    @classmethod
    def leave(cls, session, user):

        session.remove_player(user.id)

    # -------------------------
    # Officer Tools (Coming Soon)
    # -------------------------

    @classmethod
    def lock_raid(cls, session):

        session.locked = True

    @classmethod
    def unlock_raid(cls, session):

        session.locked = False

    @classmethod
    def finish_raid(cls, raid_id):

        cls.remove_session(raid_id)