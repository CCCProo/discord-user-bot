import random
from datetime import datetime

class EventNode:
    def __init__(self, client_data, type):
        self.type = type
        self.properties = {
            "client_track_timestamp": 0,
            "client_heartbeat_session_id": client_data.session_id,
            "client_uuid": client_data.generate_uuid(),
            "client_send_timestamp": 0,
        }

class ScienceBody:
    def __init__(self, client_data):
        self.client_data = client_data
        self.body = {
            "events": [],
        }

    def event_view(self, type, page_name, previous_page_name, previous_link_location, has_session):
        node = EventNode(self.client_data, type)
        node.properties["page_name"] = page_name
        node.properties["previous_page_name"] = previous_page_name
        node.properties["previous_link_location"] = previous_link_location
        node.properties["has_session"] = has_session
        self.body["events"].append(node)
        return self

    def user_triggered(self, type, name, revision, bucket, population):
        node = EventNode(self.client_data, type)
        node.properties["name"] = name
        node.properties["revision"] = revision
        node.properties["bucket"] = bucket
        node.properties["population"] = population
        self.body["events"].append(node)
        return self

    def event_click(self, type, button_state, page_name):
        node = EventNode(self.client_data, type)
        node.properties["button_state"] = button_state
        node.properties["page_name"] = page_name
        self.body["events"].append(node)
        return self

    def export(self):
        time_sent = int(datetime.now().timestamp() * 1000)
        delay = random.randint(1000, 2000)
        delay_it = delay / len(self.body["events"])

        for i, event in enumerate(self.body["events"]):
            inv_it = len(self.body["events"]) - i
            event.properties["client_track_timestamp"] = time_sent - int(delay_it * inv_it) + random.randint(-10, 10)
            event.properties["client_send_timestamp"] = time_sent

        return self.body
