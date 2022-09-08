import os
import ctypes


from lib.process import mhr_pid_lookup


pid  = mhr_pid_lookup()
libc = ctypes.CDLL('libc.so.6')
file_descriptor = os.open(f'/proc/{pid}/mem', os.O_RDWR)

buffers = {
    # 'int8'   : ctypes.c_int8(),
    # 'int16'  : ctypes.c_int16(),
    # 'double' : ctypes.c_double(),

    'int32' : ctypes.c_int32(),
    'int64' : ctypes.c_int64(),
    'float' : ctypes.c_float(),
}

def read(ctype, address):
    libc.pread(
        file_descriptor,
        ctypes.pointer(buffers[ctype]),
        ctypes.sizeof(buffers[ctype]),
        ctypes.c_long(address)
    )

    return buffers[ctype].value

def read_ptr(address, offsets = []):
    for offset in offsets:
        address = read('int64', address + offset)

    return address
