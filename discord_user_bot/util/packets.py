"""
Contains all the hardcoded packets.
"""
class GateWayOpen:
    def __init__(self, token, config):
        self.op = 2
        self.d = {
            "token": token,
            "capabilities": 125,
            "properties": {
                "os": config["os"],
                "browser": "Chrome",
                "device": "",
                "system_locale": config["language"],
                "browser_user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
                "browser_version": "93.0.4577.63",
                "os_version": "",
                "referrer": "",
                "referring_domain": "",
                "referrer_current": "",
                "referring_domain_current": "",
                "release_channel": "stable",
                "client_build_number": 97662,
                "client_event_source": None,
            },
            "presence": {"status": "online", "since": 0, "activities": [], "afk": False},
            "compress": False,
            "client_state": {"guild_hashes": {}, "highest_last_message_id": "0", "read_state_version": 0, "user_guild_settings_version": -1},
        }

class HeartBeat:
    def __init__(self, message_counter):
        self.op = 1
        self.d = message_counter

class GuildRequest:
    def __init__(self, guild_id, limit):
        self.op = 8
        self.d = {
            "guild_id": str(guild_id),
            "query": "",
            "limit": int(limit),
        }

class TokenCheck:
    def __init__(self, token):
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US",
            "authorization": token,
            "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }
        self.referrer = "https://discord.com/login?redirect_to=%2Fchannels%2F%40me"
        self.referrerPolicy = "strict-origin-when-cross-origin"
        self.body = None
        self.method = "GET"
        self.mode = "cors"

# This line makes the classes available for import
__all__ = ["GateWayOpen", "HeartBeat", "GuildRequest", "TokenCheck"]
