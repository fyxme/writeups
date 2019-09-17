c = "vuqxyugfyzfjgoccjkxlqvguczymjhpmjkyzoilsxlwtmccclwizqbetwthkkvilkruufwuu"


c = [c[i:i+2] for i in range(0, len(c), 2)]


print c


# z = (x*key[0][0] + y*key[0][1])%26 + 97
# w = (x*key[1][0] + y*key[1][1])%26 + 97
z = c[i]
w = c[i+1]


# z = (x*key[0][0] + y*key[0][1])%26
# w = (x*key[1][0] + y*key[1][1])%26
z -= 97
w -= 97

# z = (x*(key[0][0])%26 + y*(key[0][1])%26)%26 %x
# w = (x*(key[1][0])%26 + y*(key[1][1])%26)%26
x = 97 - ord('p') # 'p' or 'c'
y = 97 - ord('c') # 'c' or 't'

# z = (x*(key[0][0])%26 + y*(key[0][1])%26)%26 %x
# z =
z_tmp = z % x
