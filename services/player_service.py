from models.player import Player
from services.database import get_connection


def add_player(member):
    """Add a Discord member to the database."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO players
        (discord_id, discord_name)
        VALUES (?, ?)
    """, (
        member.id,
        str(member)
    ))

    conn.commit()
    conn.close()


def save_player_profile(
    discord_id: int,
    character_name: str,
    legacy_name: str,
    player_class: str,
    discipline: str,
):
    """Create or update a player's profile."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE players
        SET
            character_name = ?,
            legacy_name = ?,
            player_class = ?,
            discipline = ?
        WHERE discord_id = ?
    """, (
        character_name,
        legacy_name,
        player_class,
        discipline,
        discord_id,
    ))

    conn.commit()
    conn.close()


def get_player(discord_id: int) -> Player | None:
    """Retrieve a player from the database."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM players
        WHERE discord_id = ?
    """, (discord_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return Player(
        discord_id=row[0],
        discord_name=row[1],
        character_name=row[2],
        legacy_name=row[3],
        player_class=row[4],
        discipline=row[5],
        can_tank=bool(row[6]),
        can_heal=bool(row[7]),
        can_dps=bool(row[8]),
        is_main=bool(row[9]),
        attendance=row[10],
    )