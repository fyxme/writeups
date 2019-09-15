#!/usr/bin/env python2.7
from __future__ import division
import base64, sys, io, time, webbrowser, urllib
import requests
from bs4 import BeautifulSoup
from PIL import Image
import cv2
import numpy as np

import pwn
import time

from multiprocessing import Pool
#from multiprocessing.pool import ThreadPool as Pool

SB_LENGTH = 16
DEFAULT_PADDING_CHAR = "+"
NUM_POOLS = 40

def print_colored( cipher, idx ):
    print " ".join([
            red(cipher[:idx*2]), # c' block which we haven't touched yet
            blue(cipher[idx*2:idx*2+2]), # current bytes being modified
            green(cipher[idx*2+2:])]) # bytes we already found

def blue( s ):
    return "\033[00;34m{}\033[00m".format(s)

def green( s ):
    return "\033[01;32m{}\033[00m".format(s)

def red( s ):
    return "\033[01;31m{}\033[00m".format(s)

def split_len( cipher, length=SB_LENGTH ):
    return [cipher[i:i+length] for i in range(0, len(cipher), length)]

def is_valid_cipher( input ):
    (i,cipher) = input
    # print "trying:", i
    c = pwn.connect("2018shell1.picoctf.com", 24933)
    c.sendlineafter("cookie?", cipher.encode("hex"))
    resp = c.recvrepeat(2.2)
    c.close()
    if "The flag is" in resp:
        print resp
        exit()

    if "invalid padding" not in resp.lower():
        print i, resp
        return i, True
    else:
        return i, False
    #return "invalid padding" not in resp.lower()

def compute_word( plain, padding=DEFAULT_PADDING_CHAR ):
    return "".join([chr(c) if (c > 0x08) else padding for c in plain])

def attack( cipher, block_length=SB_LENGTH ):
    p = Pool(NUM_POOLS) # not sure what to set this to...

    # separate the cipher into blocs of 16
    cipher_block = split_len( cipher, length=block_length )

    results = []
    istates = []

    for i in range(len(cipher_block)):
        if i + 1 == len(cipher_block):
            break

        idx = len(cipher_block) - 1
        prevblock = cipher_block[idx-i-1]
        block = cipher_block[idx-i]

        ivals = []
        plain = []
        cprime = chr(0x00)*SB_LENGTH

        for cprime_idx in range( SB_LENGTH - 1, -1, -1 ):

            # Create a PKCS#7 padding index [0x01, SB_LENGTH]
            padding_idx = SB_LENGTH - cprime_idx

            guesses = dict()

            for guess in range(256):
                # Create new ciphertext with the guess
                if cprime_idx > 0:
                    ciphertext = cprime[:cprime_idx]
                    ciphertext += chr(guess)
                else:
                    ciphertext = chr(guess)

                # Insert the previous intermediate values
                for intr in ivals:
                    # Adjust them for this padding index
                    ciphertext += chr(intr^padding_idx)

                # Append the block we're cracking
                ciphertext += block

                sys.stdout.write("\033[F") # Cursor up one line
                print_colored(ciphertext.encode("hex"), cprime_idx)

                guesses[guess] = ciphertext

            while(1):
                try:
                    back = p.map(is_valid_cipher, guesses.items())
                    guesses = back
                    break
                except:
                    time.sleep(1)
                    print "Something went wrong.. Retrying..."
                    pass

            for guess, valid in guesses:
                # if valid:
                    # print i, valid
                # # If the oracle correctly decrypts the ciphertext
                if valid:
                    # Calculate the intermediate value
                    intermediate = guess^padding_idx
                    # Save the intermediate value
                    ivals.insert(0, intermediate)
                    # Crack the plain text character
                    plain.insert(0, intermediate^ord(prevblock[cprime_idx]))
                    print "".join(map(chr, plain))
                    # We found it, bail out
                    if cprime_idx:
                        print
                    break

        print "  " + green(ciphertext.encode("hex")) # print final decoded cipher

        print "\nIntermediate values = {}\n".format(ivals)

        plainstr = compute_word(plain)
        results.append(plainstr)
        istates.append(ivals)

    return results, istates

def encrypt(message):
    # generate a 16 bytes iv (random or not, it doesn't matter)
    iv = "A" * 16
    current = "A" * 16

    # TODO: add padding if necessary
    assert(len(message) % SB_LENGTH == 0)


    message = map(ord, message)
    message = [message[i:i+SB_LENGTH] for i in range(0, len(message), SB_LENGTH)]

    e_msg = current
    #print message
    # we start from the last block
    message = message[::-1]
    for i, block in enumerate(message):
        print "encrypting:", block
        cookie = iv + current
        #cookie = iv + e_msg

        print cookie.encode("hex")

        word, istates = attack(cookie)
        print "Encrypted word was : {} ('+' represents padding)".format("".join(reversed(word)))
        word = "".join(reversed(word))
        print "Word ordinal values: {}".format(map(ord, word))
        print "Intermediate values: {}".format(list(reversed(istates)))

        istates = list(reversed(istates))

        # xor intermediate value with wanted block to get previous cipherblock
        istate = istates[0]
        xored = [a^b for a,b in zip(istate,block)]
        #xored = [a^ord(b) for a,b in zip(xored, iv)]
        x_value = "".join(map(chr, xored))

        current = x_value
        e_msg = current + e_msg

    return e_msg.encode('hex')

def main():
    pwn.context.log_level = 'error'
    pwn.context.log_console=open('/dev/null', 'w')

    cookie = "5468697320697320616e204956343536d6ca0a2883280762915414c54e97df1b40871b72f45ec7f9510a080095436d514129e137aaac86a0f7fa8bd3d250b9d1df35b668fcb93f00bb06692560a3fed8a3b523d385f1477b6daac14ff2416c67"

    cookie = "0405004a625e271a66013210a5299473d9a5581b7cb35f961c31900ba34ac6a2e7e0d2881176bb7783134ffb7e131a8e8e8528e88802ae308459dbcb4421982741414141414141414141414141414141"

    # cookie = [cookie[i:i+2] for i in range(0,len(cookie),2)]
    # cookie = map(lambda x: int(x,16), cookie)
    # cookie = "".join(map(chr,cookie))
    cookie = cookie.decode('hex')

    print "cipher len:", len(cookie)
    print
    msg = '{"username": "a", "expires": "2100-01-07", "is_admin": "true"}' + '\x02'*2
    print "msg len:", len(msg)
    print
    print encrypt(msg)
    exit()

    word, istates = attack( cookie )

    print "Encrypted word was : {} ('+' represents padding)".format("".join(reversed(word)))
    word = "".join(reversed(word))
    print "Word values: {}".format(map(ord, word))
    print "Intermediate values: {}".format(list(reversed(istates)))

if __name__ == '__main__':
    main()
