import base64
import time

import struct
import random

class UUID:
    def __init__(self):
        self.random_prefix = int(4294967296 * random.random())
        self.creation_time = int(time.time() * 1000)
        self.sequence = 0

    @staticmethod
    def from_2x32(l, r):
        return (l << 32) | r

    @staticmethod
    def fit32(num):
        return num % 4294967296

    @staticmethod
    def shift32(num):
        return num >> 32

    def generate(self, fingerprint_id):
        id_ = fingerprint_id
        sequence_id = self.sequence
        self.sequence += 1

        data = struct.pack('QQIII', id_, self.random_prefix, self.creation_time, sequence_id, 0)
        return base64.b64encode(data).decode()

    def parse(self, uuid_str):
        data = base64.b64decode(uuid_str)
        id_, random_prefix, creation_time, sequence_id, _ = struct.unpack('QQIII', data)

        return {
            'id': id_,
            'randomPrefix': random_prefix,
            'creationTime': creation_time,
            'sequenceID': sequence_id
        }
