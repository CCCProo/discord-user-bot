"""
Specifies IDs as variable names just like C++ enums.
"""

class ReadyStates:
    OFFLINE = 0
    CONNECTING = 1
    CONNECTED = 2

    @classmethod
    def get_name(cls, value):
        return cls.__dict__.get(value)

    @classmethod
    def get_value(cls, name):
        for key, val in cls.__dict__.items():
            if val == name:
                return key

    def get_v(num):
        if num == 0:
            return "OFFLINE"
        elif num == 1:
            return "CONNECTING"
        elif num == 2:
            return "CONNECTED"


__all__ = ["ReadyStates"]
