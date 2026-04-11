#!/usr/bin/python3

from pwn import *
import os

os.system("mkdir -p Data")
env = os.environ.copy()
env['LD_LIBRARY_PATH'] = './runner/external/'

pid = process(['./runner/run.sh'], env=env)
pid.recv(numb=100, timeout=1.0)
pid.sendline(b'turbine_remote_access')

pid.recv(timeout=1.0)

os.system("find ./Data/ -type f -exec cat {} \\;")
print()
os.system("rm -rf Data")