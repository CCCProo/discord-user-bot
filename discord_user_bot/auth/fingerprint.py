class Fingerprint:
    def __init__(self, requester):
        self.requester = requester
        self.fingerprint = None
        self.fingerprint_id = None

    async def request(self):
        info = await self.requester.fetch_request("experiments", method="GET")
        self.fingerprint = info.get("fingerprint")
        return self.fingerprint

    @property
    def id(self):
        if self.fingerprint is None:
            return None
        if self.fingerprint_id is None:
            self.fingerprint_id = self.fingerprint.split(".")[0]
        return self.fingerprint_id
