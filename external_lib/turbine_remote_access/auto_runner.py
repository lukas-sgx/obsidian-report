#!/usr/bin/python3

from pwn import *
import os
import warnings

warnings.filterwarnings("ignore", category=BytesWarning)
context.log_level = 'error'

os.system("mkdir -p Data")
env = os.environ.copy()
env['LD_LIBRARY_PATH'] = './runner/external/'

pid = process(['./runner/run.sh'], env=env)
pid.recv(numb=100, timeout=1.0)
pid.sendline(b'turbine_remote_access')

pid.recv(timeout=1.0)

print(text.red("[+]") + " FLAG turbine_remote_access:")
os.system("find ./Data/ -type f -exec cat {} \\;")
print()
os.system("rm -rf Data")