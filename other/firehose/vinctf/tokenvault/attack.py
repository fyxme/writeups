from pwn import *
import base64

text = "3ysBaM6CoSHg3OORhjgAdWNXS/thJBGQGk+wEbKfv9M="
text = base64.b64decode(text)

print len(text)

for i in range(255):

    temp = list(text)
    temp[15] = chr(i)
    temp = ''.join(temp)
    c = connect('challenge1.ctf.vincbreaker.me',33333)

    print c.recvrepeat(1)
    c.sendline(text.encode('hex'))
    print c.recvrepeat(1)

    c.close()
