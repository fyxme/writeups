We open the assembly file in sublime

The `push`/`pushl` instructions pushes values onto the stack therefore we can start by counting the numb of `push` instructions.

There are 4 which means we push `0x4 * 4` onto the stack therefore `0x10`

The instruction `sub $0xf8, %esp` subs `0xf8` to the $esp therefore it grows the stack by 0xf8

Calculating `0xf8 + 0x10` we get `0x108` which is the flag.

Flag: `0x108`
