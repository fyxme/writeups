from multiprocessing import Pool
from pwn import *
import string

SPLIT_KEY = "||"

def get_data_from_file():
    with open('combinations.txt') as f:
        data = f.read().strip().split('\n')

    data = filter(None, data)

    d = {}
    for line in data:
        line = line.split(SPLIT_KEY)
        question = line[0]
        answer = line[1]
        d[question] = answer
    return d

def save_data_to_file(d):
    with open('combinations.txt', 'w') as f:
        for k, v in d.items():
            f.write("{}{}{}\n".format(k, SPLIT_KEY, v))

def learn(_):
    global data

    try:
        c = connect("2018shell1.picoctf.com", 8672)

        while(1):
            resp = c.recvrepeat(0.5)

            if "picoctf" in resp.lower():
                with open('flag.txt') as f:
                    f.write(resp)
                exit()

            resp = resp.split('\n')
            question = resp[-3].strip()

            if question in data:
                c.sendline(data[question])
            else:
                c.sendline(')(')
                c.recvuntil("Expected => ")
                resp = c.recvline().strip()
                c.close()
                return question, resp
    except:
        return ()

context.log_level = 'error'

data = get_data_from_file()
p = Pool(30)

for _ in range(1):
    results = p.map(learn, range(1200))
    results = filter(None, results)
    for r in results:
        data[r[0]] = r[1]

    save_data_to_file(data)
    print results
    print len(results)
    # raw_input("continue?:")
