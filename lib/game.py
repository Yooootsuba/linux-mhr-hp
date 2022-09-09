import struct


from lib.memory import read, read_ptr
from lib.display import quest_status, monster_names


def byte(value):
    return value % 256


class MHRGame:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.quest = MHRQuest()
        self.monsters = [MHRMonster(0), MHRMonster(1), MHRMonster(2)]


class MHRQuest:
    def __init__(self):
        self.pointer = read('int64', 0x140000000 + 0xEE59BC8)

        self.status_code = 0

    def status(self):
        return quest_status[self.status_code]

    def is_in_quest(self):
        return self.status_code == 2

    def update(self):
        self.status_code = read('int32', self.pointer + 0x110)


class MHRMonster:
    def __init__(self, index):
        self.index          = index
        self.id             = 0
        self.current_health = 0
        self.max_health     = 0

    def get_name(self):
        return monster_names[self.id]

    def get_hp(self):
        return self.current_health / self.max_health * 100

    def decode_health(self, value, key):
        decoded = bytearray([0, 0, 0, 0])

        edx = byte(value & 0xFF)
        ecx = key + (key * 2)
        edx += byte(ecx)
        eax = byte(ecx)
        r8d = ecx
        ecx = eax * 0x3F

        r8d += 4
        key = r8d
        r8d += 4

        # First byte
        eax = byte(key >> 8)
        key = (key & 0x00FFFFFF) | (r8d & 0xFF000000)
        r8d += 4
        edx ^= byte(ecx)
        ecx = eax * 0x3F
        decoded[0] = byte(edx)

        # Second byte
        edx = byte(value >> 8)
        edx += eax
        eax = byte(key >> 16)
        key = r8d
        r8d = 0
        edx ^= byte(ecx)
        ecx = eax * 0x3F
        decoded[1] = byte(edx)

        # Third byte
        edx = byte(value >> 16)
        edx += eax
        eax = byte(key >> 24)
        edx ^= byte(ecx)
        ecx = eax * 0x3F
        decoded[2] = byte(edx)

        # Fourth byte
        edx = byte(value >> 24)
        edx += eax
        edx ^= byte(ecx)
        decoded[3] = byte(edx)

        return struct.unpack('f', decoded)[0]

    def update(self):
        self.pointer = read_ptr(0x140000000, [0x0EE4C410, 0x80, 0x10, 0x20 + 0x8 * self.index])

        self.id = read('int32', self.pointer + 0x2C0)

        try:
            self.get_name()
        except:
            self.id = 0
            return

        health_component    = read_ptr(self.pointer    , [0x2F8, 0x48, 0x10, 0x20, 0x10, 0x20])
        encoded_ptr         = read_ptr(health_component, [0x10, 0x18])

        health_encoded_mod  = read('int32', encoded_ptr + 0x18) & 3
        health_encoded      = read('int32', encoded_ptr + health_encoded_mod * 4 + 0x1C)
        health_encoded_key  = read('int32', encoded_ptr + 0x14)

        self.current_health = self.decode_health(health_encoded, health_encoded_key)
        self.max_health     = read('float', health_component + 0x18)
