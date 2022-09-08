import re
import os
import ctypes


quest_address = 0xee59bc8
quest_status_offsets = 0x110


class MHRMemory:
    def __init__(self, pid):
        self.pid = pid
        self.libc = ctypes.CDLL('libc.so.6')
        self.file_descriptor = os.open(f'/proc/{self.pid}/mem', os.O_RDWR)

        self.buffers = {
            # 'int8'   : ctypes.c_int8(),
            # 'int16'  : ctypes.c_int16(),
            # 'double' : ctypes.c_double(),

            'int32' : ctypes.c_int32(),
            'int64' : ctypes.c_int64(),
            'float' : ctypes.c_float(),
        }

        self.ptr_quest = self.read('int64', self.get_base_address() + quest_address)


    def get_base_address(self):
        with open(f'/proc/{self.pid}/maps', 'r') as f:

            for line in f.readlines():
                match = re.match('([0-9a-f]+)-([0-9a-f]+)(.*MonsterHunterRise.exe.*)', line)

                if match != None:
                    return int(match.group(1), base = 16)

    def read(self, ctype, address):
        self.libc.pread(
            self.file_descriptor,
            ctypes.pointer(self.buffers[ctype]),
            ctypes.sizeof(self.buffers[ctype]),
            ctypes.c_long(address)
        )

        return self.buffers[ctype].value

    def read_ptr(self, ctype, address, offsets = []):
        last_offset = offsets.pop()

        for offset in offsets:
            address = self.read('int64', address + offset)

        return self.read(ctype, address + last_offset)


    def update(self):
        game = {
            'quest_status' : self.read('int32', self.ptr_quest + quest_status_offsets)
        }

        if game['quest_status'] == 2:
            pass

        return game
