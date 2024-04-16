"""
Defines a class to read from buffers.
Defines a class to write to buffers.
"""

import struct
import array

class Reader:
    def __init__(self, buffer, little_endian=True):
        self.array_view = memoryview(buffer)
        self.offset = 0
        self.little_endian = little_endian

    def get_i8(self):
        data, = struct.unpack_from('<b' if self.little_endian else '>b', self.array_view, self.offset)
        self.offset += 1
        return data

    def get_i16(self):
        data, = struct.unpack_from('<h' if self.little_endian else '>h', self.array_view, self.offset)
        self.offset += 2
        return data

    def get_i32(self):
        data, = struct.unpack_from('<i' if self.little_endian else '>i', self.array_view, self.offset)
        self.offset += 4
        return data

    def get_i64(self):
        data, = struct.unpack_from('<q' if self.little_endian else '>q', self.array_view, self.offset)
        self.offset += 8
        return data

    def get_u8(self):
        data, = struct.unpack_from('<B', self.array_view, self.offset)
        self.offset += 1
        return data

    def get_u16(self):
        data, = struct.unpack_from('<H' if self.little_endian else '>H', self.array_view, self.offset)
        self.offset += 2
        return data

    def get_u32(self):
        data, = struct.unpack_from('<I' if self.little_endian else '>I', self.array_view, self.offset)
        self.offset += 4
        return data

    def get_u64(self):
        data, = struct.unpack_from('<Q' if self.little_endian else '>Q', self.array_view, self.offset)
        self.offset += 8
        return data

    def get_f32(self):
        data, = struct.unpack_from('<f' if self.little_endian else '>f', self.array_view, self.offset)
        self.offset += 4
        return data

    def get_f64(self):
        data, = struct.unpack_from('<d' if self.little_endian else '>d', self.array_view, self.offset)
        self.offset += 8
        return data

class Writer:
    def __init__(self, size=1024, little_endian=True):
        self.array = array.array('B', [0] * size)
        self.offset = 0
        self.little_endian = little_endian

    def set_i8(self, value):
        struct.pack_into('<b' if self.little_endian else '>b', self.array, self.offset, value)
        self.offset += 1

    def set_i16(self, value):
        struct.pack_into('<h' if self.little_endian else '>h', self.array, self.offset, value)
        self.offset += 2

    def set_i32(self, value):
        struct.pack_into('<i' if self.little_endian else '>i', self.array, self.offset, value)
        self.offset += 4

    def set_i64(self, value):
        struct.pack_into('<q' if self.little_endian else '>q', self.array, self.offset, value)
        self.offset += 8

    def set_u8(self, value):
        struct.pack_into('<B', self.array, self.offset, value)
        self.offset += 1

    def set_u16(self, value):
        struct.pack_into('<H' if self.little_endian else '>H', self.array, self.offset, value)
        self.offset += 2

    def set_u32(self, value):
        struct.pack_into('<I' if self.little_endian else '>I', self.array, self.offset, value)
        self.offset += 4

    def set_u64(self, value):
        struct.pack_into('<Q' if self.little_endian else '>Q', self.array, self.offset, value)
        self.offset += 8

    def set_f32(self, value):
        struct.pack_into('<f' if self.little_endian else '>f', self.array, self.offset, value)
        self.offset += 4

    def set_f64(self, value):
        struct.pack_into('<d' if self.little_endian else '>d', self.array, self.offset, value)
        self.offset += 8

    @property
    def length(self):
        return self.offset

    @property
    def buffer(self):
        return self.array[:self.length].tobytes()

    def to_base64(self):
        import base64
        return base64.b64encode(self.buffer).decode('utf-8')

__all__ = ["Reader", "Writer"]
