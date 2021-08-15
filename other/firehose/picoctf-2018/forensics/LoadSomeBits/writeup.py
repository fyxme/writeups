
fp = "pico2018-special-logo.bmp"
check_word = "pico"

with open(fp) as f:
   data = f.read()

# convert ascii string to binary array
bins = map(lambda x: bin(ord(x)), data) 

# extract the Least Significant Bit from each binary value
lsb = [i[-1] for i in bins] 

for i in range(len(lsb)): 
    # Next line is the crucial line. 
    # Every time 'i' is incremented, 
    # this line will take the LSB starting from that index up to the end of the array
    # What ends up happening is that it basically ignores the first 0 to i bytes
    tmp = lsb[i:]

    # convert the tmp array to chunks of 8 bits so we can then convert those bits to bytes
    chunks = [tmp[i:i+8] for i in range(0, len(lsb), 8)]

    # Remove the last chunk if it's not of length 8
    if len(chunks[-1]) != 8:
        chunks = chunks[:-1] 

    # convert each chunks to a binary string 
    # which then gets converted to 
    # it's equivalent base 10 integer value 
    # and finally the int value gets converted into a char
    chunks = map(lambda x: chr(int("".join(x),2)), chunks) 
    word = "".join(chunks) # join the char array to get a string

    #check if our flag is in the final string
    if check_word in word: 
        print word
        exit()