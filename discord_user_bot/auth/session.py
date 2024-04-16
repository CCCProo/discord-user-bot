import random
import time
import uuid
import re

class Session:
    def __init__(self):
        self.r = [random.choice("0123456789abcdef") for _ in range(256)]
        self.clock_seq = random.randint(0, 16383)
        self.msecs = int(time.time() * 1000)
        self.nsecs = 0
        self.last_msecs = self.msecs
        self.last_nsecs = self.nsecs
        self.node = [random.randint(0, 255) for _ in range(6)]

    def getRandoms(self):
        return bytes([random.randint(0, 255) for _ in range(16)])

    def v1(self):
        now = int(time.time() * 1000)
        elapsed = (now - self.last_msecs) + (self.nsecs - self.last_nsecs) / 1e4
        if elapsed < 0:
            self.clock_seq = (self.clock_seq + 1) & 16383
        if elapsed < 0 or now > self.last_msecs:
            self.nsecs = 0
        if self.nsecs >= 1e4:
            raise ValueError("Can't create more than 10M uuids/sec")
        self.last_msecs = now
        self.last_nsecs = self.nsecs
        time_low = now & 0xffffffff
        time_mid = (now >> 32) & 0xffff
        time_hi_version = (now >> 48) & 0x0fff
        clock_seq_low = self.clock_seq & 0xff
        clock_seq_hi_variant = (self.clock_seq >> 8) & 0x3f
        return uuid.UUID(fields=(time_low, time_mid, time_hi_version, clock_seq_hi_variant, clock_seq_low, bytes(self.node)))

    def v4(self):
        return uuid.uuid4()

    def parse(self, uuid_string):
        return bytes.fromhex(re.sub(r'[^0-9a-fA-F]', '', uuid_string))

    def unparse(self, uuid_bytes):
        return str(uuid.UUID(bytes=uuid_bytes))
