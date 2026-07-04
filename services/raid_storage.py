from services.database import get_connection


def create_raid(
    operation: str,
    difficulty: str,
    raid_date: str,
    raid_time: str,
    created_by: int,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO raids (
            operation,
            difficulty,
            raid_date,
            raid_time,
            created_by
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        operation,
        difficulty,
        raid_date,
        raid_time,
        created_by,
    ))

    conn.commit()

    raid_id = cursor.lastrowid

    conn.close()

    return raid_id