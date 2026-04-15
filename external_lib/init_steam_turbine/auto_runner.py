#!/usr/bin/python3

from pwn import *
import os
import warnings

warnings.filterwarnings("ignore", category=BytesWarning)
context.log_level = 'error'

env = os.environ.copy()
env['LD_LIBRARY_PATH'] = './runner/external/'

os.system("clang ./external_lib/init_steam_turbine/decompiler/main.c -o ./external_lib/init_steam_turbine/decompiler/main")
os.system("clang ./external_lib/init_steam_turbine/decompiler/rand.c -o ./external_lib/init_steam_turbine/decompiler/rand")
pid = process(['./external_lib/init_steam_turbine/decompiler/main'], env=env)
line = pid.recvline_startswith(b'magix - decompil:')

print(text.red("[+]") + " Vuln Insecure Randomness - init_steam_turbine:")
print(line.decode(errors='ignore'))
os.system("./external_lib/init_steam_turbine/decompiler/rand")
print()