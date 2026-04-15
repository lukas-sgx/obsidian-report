#!/usr/bin/python3

from pwn import *
import os
import warnings

def main():
    warnings.filterwarnings("ignore", category=BytesWarning)
    context.log_level = 'error'

    env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = './runner/external/'

    os.system("mkdir Data")

    pid = process(['./runner/run.sh'], env=env)
    pid.recv(numb=100, timeout=1.0)
    pid.sendline(b'send_status_report')

    pid.recv(timeout=2.0)

    print(text.red("[+]") + " Vuln Weak Encryption - send_status_report:")
    os.system("./send_status_report/decrypt.sh")
    print()

    os.system("rm -rf Data")

if __name__ == "__main__":
    main()