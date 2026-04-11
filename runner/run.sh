#!/run/current-system/sw/bin/bash

export LD_LIBRARY_PATH=./runner:./runner/external
./runner/ld-linux-x86-64.so.2 --library-path ./runner/ ./runner/obsidian