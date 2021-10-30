from pwn import *
import sys

s = remote(sys.argv[1], int(sys.argv[2]))
s.interactive()
