import discord

from utils.constants import EMOJIS

DIVIDER = "━━━━━━━━━━━━━━━━━━━━"


def build_raid_embed(session):

    # -----------------------------
    # Raid Status
    # -----------------------------
    status = "🟢 **OPEN FOR SIGNUPS**"

    if getattr(session, "locked", False):
        status = "🔴 **RAID LOCKED**"

    if getattr(session, "completed", False):
        status = "🏁 **RAID COMPLETED**"

    # -----------------------------
    # Description
    # -----------------------------
    operation = session.operation.title()

    description = status
    description += f"\n\n# ⭐ {operation} ⭐"

    if getattr(session, "difficulty", None):
        description += f"\n⚔ **{session.difficulty}**"

    description += f"\n\n{DIVIDER}"

    if getattr(session, "raid_date", None):
        description += f"\n📅 **Date**\n{session.raid_date}"

    if getattr(session, "raid_time", None):
        description += f"\n\n🕗 **Time**\n{session.raid_time}"

    if getattr(session, "raid_leader", None):
        description += f"\n\n👑 **Raid Leader**\n{session.raid_leader}"

    description += f"\n\n{DIVIDER}"

    embed = discord.Embed(
        title="🚌 Short Bus Jawa Raid Board",
        description=description,
        color=discord.Color.orange(),
    )

    tanks = "\n".join(f"• {p.display_name}" for p in session.tanks)
    healers = "\n".join(f"• {p.display_name}" for p in session.healers)
    dps = "\n".join(f"• {p.display_name}" for p in session.dps)
    bench = "\n".join(f"• {p.display_name}" for p in session.bench)

    embed.add_field(
        name=f"{EMOJIS['tank']} Tanks ({len(session.tanks)}/2)",
        value=tanks if tanks else "• Empty",
        inline=False,
    )

    embed.add_field(
        name=f"{EMOJIS['healer']} Healers ({len(session.healers)}/2)",
        value=healers if healers else "• Empty",
        inline=False,
    )

    embed.add_field(
        name=f"{EMOJIS['dps']} DPS ({len(session.dps)}/4)",
        value=dps if dps else "• Empty",
        inline=False,
    )

    embed.add_field(
        name=f"{EMOJIS['bench']} Bench ({len(session.bench)})",
        value=bench if bench else "• Empty",
        inline=False,
    )

    if getattr(session, "raid_id", None):
        embed.set_footer(
            text=f"Raid #{session.raid_id} • Short Bus Jawa"
        )
    else:
        embed.set_footer(
            text="Short Bus Jawa"
        )

    return embed