#!/usr/bin/env python2
# -*- coding:utf-8 -*-
#
# VincCTF 2018 - TokenVault v1
import socket
import sys
from thread import *
from Crypto.Cipher import AES
from Crypto import Random
from hashlib import sha256
from base64 import b64encode, b64decode

HOST = ''
PORT = 33333

pad = lambda data: data + chr((16 - len(data) % 16)) * (16 - len(data) % 16)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

FLAG = 'VINCCTF{XXXXXXXXXXXXXXXXXXXXXXXXX}'
KEY = sha256('XXXXXXXXXXXXXXXXXXXXXXXXXXX').hexdigest()[0:32]


def verify_token(token):
    decoded = b64decode(token)
    data = unpad(AES.new(KEY, AES.MODE_CBC, decoded[0:16]).decrypt(decoded[16:]))
    print data
    return data == 'flag: 1'


def generate_token(authorized):
    iv = Random.new().read(16)
    return b64encode(iv + AES.new(KEY, AES.MODE_CBC, iv).encrypt(pad('flag: ' + str(authorized))))


def connection_handler(conn):
    conn.send(
        'Welcome to TokenVault, where your flags are secured by tokens encrytped using millitary grade encryption.\n')
    conn.send('Token example: ' + generate_token(0) + '\n')
    conn.send('Please send an authorized token: \n')
    data = conn.recv(1024).strip()
    if verify_token(data):
        conn.send('Here is your flag: ' + FLAG + '\n')
    else:
        conn.send('Unauthorized token, no flag for you.\n')
    conn.close()


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    print 'Socket bind complete'
    s.listen(10)
    print 'Socket now listening'
    try:
        while 1:
            conn, addr = s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            start_new_thread(connection_handler, (conn,))
    except KeyboardInterrupt:
        pass

    s.close()
    print 'Socket closed'


if __name__ == '__main__':
    start_server()
