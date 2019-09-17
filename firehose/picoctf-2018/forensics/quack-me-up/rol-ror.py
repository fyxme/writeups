###########################################################################
# Rotating bits (tested with Python 2.7)

from __future__ import print_function   # PEP 3105

# max bits > 0 == width of the value in bits (e.g., int_16 -> 16)

# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

max_bits = 16  # For fun, try 2, 17 or other arbitrary (positive!) values

c ="11 80 20 E0 22 53 72 A1 01 41 55 20 A0 C0 25 E3 35 40 55 30 85 55 70 20 C1"

c = c.split(" ")
c = map(lambda x: int(x,16),c)
c = map(lambda x: rol(x, 8,8), c)
c = map(lambda x: x ^ 22, c)
c = map(lambda x: ror(x, 4,8), c)

c = map(chr, c)

print("".join(c))
