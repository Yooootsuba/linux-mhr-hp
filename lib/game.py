import struct


from lib.memory import read, read_ptr


quest_status = {
    0 : 'In village',
    1 : 'Loading quest',
    2 : 'In Quest',
    3 : 'Victory',
    4 : 'Defeat',
    5 : 'Quest reset',
    6 : 'Quest time out',
    7 : 'Exit quest',
}


monster_names = {
    98   : 'Great Izuchi',
    54   : 'Great Baggi',
    107  : 'Kulu-Ya-Ku',
    59   : 'Great Wroggi',
    60   : 'Arzuros',
    61   : 'Lagombi',
    62   : 'Volvidon',
    91   : 'Aknosom',
    47   : 'Royal Ludroth',
    44   : 'Barroth',
    3    : 'Khezu',
    92   : 'Tetranadon',
    90   : 'Bishaten',
    102  : 'Pukei-Pukei',
    108  : 'Jyuratodus',
    4    : 'Basarios',
    93   : 'Somnacanth',
    1    : 'Rathian',
    42   : 'Barioth',
    109  : 'Tobi-Kadachi',
    89   : 'Magnamalo',
    100  : 'Anjanath',
    37   : 'Nargacuga',
    82   : 'Mizutsune',
    97   : 'Goss Harag',
    2    : 'Rathalos',
    95   : 'Almudron',
    57   : 'Zinogre',
    32   : 'Tigrex',
    7    : 'Diablos',
    94   : 'Rakna-Kadaki',
    24   : 'Kushala Daora',
    25   : 'Chameleos',
    27   : 'Teostra',
    23   : 'Rajang',
    118  : 'Bazelgeuse',
    96   : 'Wind Serpent Ibushi',
    99   : 'Thunder Serpent Narwa+',
    1379 : 'Narwa the Allmother+',
    1366 : 'Crimson Glow Valstrax',
    1852 : 'Apex Arzuros',
    1793 : 'Apex Rathian',
    1874 : 'Apex Mizutsune',
    1794 : 'Apex Rathalos',
    1799 : 'Apex Diablos',
    1849 : 'Apex Zinogre+',
    81   : 'Astalos',
    132  : 'Malzeno',
    19   : 'Daimyo Hermitaur',
    346  : 'Blood Orange Bishaten',
    134  : 'Garangolm',
    349  : 'Aurora Somnacanth',
    133  : 'Lunagaron',
    136  : 'Espinas',
    135  : 'Gaismagorm',
    71   : 'Gore Magala',
    77   : 'Seregios',
    351  : 'Magma Almudron',
    350  : 'Pyre Rakna-Kadaki',
    72   : 'Shagaru Magala',
    20   : 'Shogun Ceanataur',
    1303 : 'Furious Rajang',
    1369 : 'Scorned Magnamalo',
    1398 : 'Seething Bazelgeuse',
    514  : 'Silver Rathalos',
    513  : 'Gold Rathian',
    549  : 'Lucent Nargacuga',
}


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

    def update(self):
        self.status_code = read('int32', self.pointer + 0x110)


class MHRMonster:
    def __init__(self, index):
        self.pointer = read_ptr(0x140000000, [0x0EE4C410, 0x80, 0x10, 0x20 + 0x8 * index])

        self.index          = index
        self.id             = 0
        self.current_health = 0
        self.max_health     = 0

    def get_monster_id(self):
        return self.id

    def get_monster_name(self):
        return monster_names[self.id]

    def get_current_health(self):
        return self.current_health

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
        self.id = read('int32', self.pointer + 0x2C0)

        health_component    = read_ptr(self.pointer    , [0x2F8, 0x48, 0x10, 0x20, 0x10, 0x20])
        encoded_ptr         = read_ptr(health_component, [0x10, 0x18])

        health_encoded_mod  = read('int32', encoded_ptr + 0x18) & 3
        health_encoded      = read('int32', encoded_ptr + health_encoded_mod * 4 + 0x1C)
        health_encoded_key  = read('int32', encoded_ptr + 0x14)

        self.current_health = self.decode_health(health_encoded, health_encoded_key)
        self.max_health     = read('float', health_component + 0x18)
