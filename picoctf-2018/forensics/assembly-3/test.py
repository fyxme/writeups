from __future__ import print_function
from unicorn import *
from unicorn.x86_const import *
from pwn import *

X86_CODE32 = asm("""
mov    eax,0x27
xor    al,al
mov    ah,BYTE PTR [ebp+0xb]
sal    ax,0x10
sub    al,BYTE PTR [ebp+0xc]
add    ah,BYTE PTR [ebp+0xf]
xor    ax,WORD PTR [ebp+0x12]
""", arch = 'i386', os = 'linux')

ADDRESS = 0x1000000
STACK = 0x2000000
print("Emulate i386 code")
try:
  mu = Uc(UC_ARCH_X86, UC_MODE_32)

  mu.mem_map(ADDRESS, 2 * 1024 * 1024)
  mu.mem_map(STACK, 2 * 1024 * 1024)

  mu.mem_write(ADDRESS, X86_CODE32)
  mu.mem_write(STACK, '\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a'+p32(0xfac0f685)+p32(0xe0911505)+p32(0xaee1f319))

  mu.reg_write(UC_X86_REG_EBP, STACK)

  mu.emu_start(ADDRESS, ADDRESS + len(X86_CODE32))

  print("Emulation done. Below is the CPU context")

  r_eax = mu.reg_read(UC_X86_REG_EAX)
  r_ebx = mu.reg_read(UC_X86_REG_EBX)
  print(">>> EAX = 0x%x" % r_eax) # 0x7771
except UcError as e:
  print("ERROR: %s" % e)
