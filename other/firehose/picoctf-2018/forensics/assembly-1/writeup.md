> assembly-1 - Points: 200 - (Solves: 423)
> What does asm1(0x15e) return? Submit the flag as a hexadecimal value (starting with '0x'). NOTE: Your submission for this question will NOT be in the normal flag format. Source located in the directory at /problems/assembly-1_3_cfc4373d0e723e491f368e7bcc26920a.

Following the different jumps based on the value of ebp+8 takes us to part c where we add 0x3 to [ebp+0x8] which is argument 1.

Calculating the sum we get the value returned:
```python
print hex(0x15e + 0x3) # 0x161
```

Flag: `0x161`
