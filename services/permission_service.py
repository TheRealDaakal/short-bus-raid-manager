import discord


OFFICER_ROLES = {
    "Raid Officer",
    "Guild Master",
    "Officer",
}


class PermissionService:

    @staticmethod
    def is_officer(member: discord.Member) -> bool:

        if member.guild_permissions.administrator:
            return True

        return any(role.name in OFFICER_ROLES for role in member.roles)