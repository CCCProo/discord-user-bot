from . import uuid
from .util import gen_component, gen_ua
from .xtrack import generate_xtrack
from .fingerprint import Fingerprint
from .session import Session

class ClientData:
    def __init__(self, os=None, browser=None, browser_version=None, ua=None, xtrack=None, fingerprint=None, uuid=None, authorization=None):
        self.os = os
        self.browser = browser
        self.browser_version = browser_version
        self.ua = ua
        self.xtrack = xtrack
        self.fingerprint = fingerprint
        self.uuid = uuid
        self.authorization = authorization
        self.session = Session()
        self.session_id = self.session.v4()

    async def gen(self, requester):
        requester.default_data = self
        self.os = gen_component("OS")
        self.browser = gen_component("browser")
        self.browser_version = gen_component("browserVersion")
        self.ua = gen_ua()
        self.xtrack = generate_xtrack(self.os, self.browser, self.browser_version, self.ua)
        
        self.fingerprint = Fingerprint(requester)
        await self.fingerprint.request()
        
        self.uuid = uuid.UUID(self.generate_uuid())

    def generate_uuid(self):
        return str(self.uuid) if self.fingerprint else None

