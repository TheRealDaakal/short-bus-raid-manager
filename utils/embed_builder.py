import discord

from utils.constants import EMOJIS

DIVIDER = "━━━━━━━━━━━━━━━━━━━━"


def format_role(players, limit):
    """Formats a raid role with numbered slots."""

    lines = []

    for i in range(limit):
        if i < len(players):
            lines.append(
                f"{i + 1}. {players[i].summary()}"
            )
        else:
            lines.append(
                f"{i + 1}. — Empty —"
            )

    return "\n\n".join(lines)


def build_raid_embed(session):

    # ---------------------------------
    # Raid Status
    # ---------------------------------

    if getattr(session, "completed", False):
        status = "🏁 **RAID COMPLETED**"
        color = discord.Color.dark_grey()

    elif getattr(session, "locked", False):
        status = "🔴 **RAID LOCKED**"
        color = discord.Color.red()

    else:
        status = "🟢 **OPEN FOR SIGNUPS**"
        color = discord.Color.orange()

    # ---------------------------------
    # Description
    # ---------------------------------

    description = status
    description += f"\n\n# ⭐ {session.operation} ⭐"

    if session.difficulty:
        description += f"\n⚔ **{session.difficulty}**"

    description += f"\n\n{DIVIDER}"

    if session.raid_date:
        description += f"\n📅 **Date**\n{session.raid_date}"

    if session.raid_time:
        description += f"\n\n🕗 **Time**\n{session.raid_time}"

    if session.raid_leader:
        description += f"\n\n👑 **Raid Leader**\n{session.raid_leader}"

    description += f"\n\n{DIVIDER}"

    # ---------------------------------
    # Embed
    # ---------------------------------

    embed = discord.Embed(
        title="🚌 Short Bus Jawa Raid Board",
        description=description,
        color=color,
    )

    # ---------------------------------
    # Raid Roles
    # ---------------------------------

    embed.add_field(
        name=f"{EMOJIS['tank']} Tanks ({len(session.tanks)}/2)",
        value=format_role(session.tanks, 2),
        inline=False,
    )

    embed.add_field(
        name=f"{EMOJIS['healer']} Healers ({len(session.healers)}/2)",
        value=format_role(session.healers, 2),
        inline=False,
    )

    embed.add_field(
        name=f"{EMOJIS['dps']} DPS ({len(session.dps)}/4)",
        value=format_role(session.dps, 4),
        inline=False,
    )

    # ---------------------------------
    # Bench
    # ---------------------------------

    if session.bench:

        bench = "\n\n".join(
            f"{i + 1}. {player.summary()}"
            for i, player in enumerate(session.bench)
        )

    else:

        bench = "— Empty —"

    embed.add_field(
        name=f"{EMOJIS['bench']} Bench ({len(session.bench)})",
        value=bench,
        inline=False,
    )

    # ---------------------------------
    # Missing Roles
    # ---------------------------------

    missing = []

    if len(session.tanks) < 2:
        needed = 2 - len(session.tanks)
        missing.append(
            f"{EMOJIS['tank']} {needed} Tank{'s' if needed != 1 else ''}"
        )

    if len(session.healers) < 2:
        needed = 2 - len(session.healers)
        missing.append(
            f"{EMOJIS['healer']} {needed} Healer{'s' if needed != 1 else ''}"
        )

    if len(session.dps) < 4:
        needed = 4 - len(session.dps)
        missing.append(
            f"{EMOJIS['dps']} {needed} DPS"
        )

    if missing:

        embed.add_field(
            name="⚠️ Still Needed",
            value="\n".join(missing),
            inline=False,
        )

    else:

        embed.add_field(
            name="✅ Raid Status",
            value="🎉 Raid is Full!",
            inline=False,
        )

    # ---------------------------------
    # Footer
    # ---------------------------------

    if session.raid_id:

        embed.set_footer(
            text=f"Raid #{session.raid_id} • Short Bus Jawa v1.0"
        )

    else:

        embed.set_footer(
            text="Short Bus Jawa v1.0"
        )

    return embed