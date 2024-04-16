import json
import base64

def generate_xtrack(os, browser, browser_version, ua):
    x_track_data = {
        "os": os,
        "browser": browser,
        "device": "",
        "system_locale": "en-US",
        "browser_user_agent": ua,
        "browser_version": browser_version,
        "os_version": "",
        "referrer": "",
        "referring_domain": "",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": 9999,
        "client_event_source": None
    }

    x_track_json = json.dumps(x_track_data)
    x_track_base64 = base64.b64encode(x_track_json.encode()).decode()

    return x_track_base64
