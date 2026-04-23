#!/usr/bin/python3

from pwn import text

def main():
    var_17h = (0x61505f6f62614c7b).to_bytes(8, byteorder="little").decode()
    var_f= 0x6f777373.to_bytes(4, byteorder="little").decode()
    var_fg = 0x6472.to_bytes(2, byteorder="little").decode()
    var_fi = 0x7d.to_bytes(byteorder="little").decode()



    print(text.red("[+]") + " Vuln Hardcoded Credentials - alchemy:")
    print(f"{var_17h}{var_f}{var_fg}{var_fi}")
    print()

if __name__ == "__main__":
    main()