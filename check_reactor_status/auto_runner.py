#!/usr/bin/python3

from pwn import *
import os
import warnings

def cipher(encoded, gap):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    decoded = list(encoded)

    for i, char in enumerate(decoded):
        if char in alphabet:
            new_gap = (alphabet.index(char) - gap) % len(alphabet)
            decoded[i] = alphabet[new_gap]

    return "".join(decoded)

def main():
    warnings.filterwarnings("ignore", category=BytesWarning)
    context.log_level = 'error'

    env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = './runner/external/'

    pid = process(['./runner/run.sh'], env=env)
    pid.recv(numb=100, timeout=1.0)
    pid.sendline(b'check_reactor_status')

    line = pid.recvline_startswith(b'Encrypted message:')

    print(text.red("[+]") + " Vuln Weak Encryption - check_reactor_status:")
    print(cipher(line.decode().split()[2], 3))
    print()

if __name__ == "__main__":
    main()