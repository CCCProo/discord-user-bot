"""
Contains all the error classes to be raised in any of the source files.
"""

class DiscordUserBotsError(Exception):
    def __init__(self, message):
        super().__init__(f"Discord User Bots: {message}")

class DiscordAPIError(Exception):
    def __init__(self, message):
        super().__init__(f"Discord API Error: {message}")

class DiscordUserBotsInternalError(DiscordUserBotsError):
    def __init__(self, message):
        super().__init__(f"(Internal Error): {message}")

# Exporting the error classes
__all__ = ["DiscordUserBotsInternalError", "DiscordUserBotsError", "DiscordAPIError"]
