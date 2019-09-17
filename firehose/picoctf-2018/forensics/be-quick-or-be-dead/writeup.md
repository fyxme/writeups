>
>

We don't have time to do the computation before the required time but we can edit the binary so the key is already set once we load it.

To exploit:
- Open the binary in a text editor
- modify the `calculate_key` function value 0x75C3328B to 0xEB866516
- save the file and run the program


Flag: `picoCTF{why_bother_doing_unnecessary_computation_402ca676}`
