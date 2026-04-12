#!/usr/bin/python3

from pwn import *
import os

env = os.environ.copy()
env['LD_LIBRARY_PATH'] = './runner/external/'

pid = process(['./runner/run.sh'], env=env)
pid.recv(numb=100, timeout=1.0)

pid.sendline(b'run_turbine')
pid.recv(timeout=1.0)

pid.sendline(b'-1')
pid.recvline_endswith(b'17/-1')
line = pid.recvline()

print(line.decode(errors='ignore'))