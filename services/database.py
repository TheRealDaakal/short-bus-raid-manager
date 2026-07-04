import sqlite3
from pathlib import Path

print(">>> database.py loaded <<<")

# Database location
DATABASE_FILE = Path("database") / "short_bus_jawa.db"


def get_connection():
    """Return a connection to the SQLite database."""

    DATABASE_FILE.parent.mkdir(exist_ok=True)

    return sqlite3.connect(DATABASE_FILE)


def initialize_database():
    """Create all required database tables."""

    print(">>> initialize_database() called <<<")

    conn = get_connection()
    cursor = conn.cursor()

    # Players table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            discord_id INTEGER PRIMARY KEY,
            discord_name TEXT NOT NULL,

            character_name TEXT,
            legacy_name TEXT,

            player_class TEXT,
            discipline TEXT,

            can_tank INTEGER DEFAULT 0,
            can_heal INTEGER DEFAULT 0,
            can_dps INTEGER DEFAULT 1,

            is_main INTEGER DEFAULT 1,

            attendance REAL DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Raids table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            operation TEXT NOT NULL,
            difficulty TEXT NOT NULL,

            raid_date TEXT NOT NULL,
            raid_time TEXT NOT NULL,

            created_by INTEGER NOT NULL,

            tanks_needed INTEGER DEFAULT 2,
            healers_needed INTEGER DEFAULT 2,
            dps_needed INTEGER DEFAULT 4,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("✅ Database initialized.")