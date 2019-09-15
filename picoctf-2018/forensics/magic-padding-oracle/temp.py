#!/usr/bin/env python
from __future__ import division
import base64, sys, io, time, webbrowser, urllib
import requests
from bs4 import BeautifulSoup
from PIL import Image
import cv2
import numpy as np
import argparse

import pwn

import asyncio

SB_LENGTH = 16
DEFAULT_PADDING_CHAR = "+"

'''
    Print cipher using colors and index
'''
def print_colored( cipher, idx ):
    print " ".join([
            red(cipher[:idx*2]), # c' block which we haven't touched yet
            blue(cipher[idx*2:idx*2+2]), # current bytes being modified
            green(cipher[idx*2+2:])]) # bytes we already found

'''
    Return blue text from provided string
'''
def blue( s ):
    return "\033[00;34m{}\033[00m".format(s)

'''
    Return green text from provided string
'''
def green( s ):
    return "\033[01;32m{}\033[00m".format(s)

'''
    Return red text from provided string
'''
def red( s ):
    return "\033[01;31m{}\033[00m".format(s)

'''
    Take in base64 string and return PIL image
'''
def stringToImage( base64_string ):
    return Image.open(io.BytesIO(base64.b64decode(base64_string)))

'''
    Convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv
'''
def toRGB( image ):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

'''
    Split cipher into blocks of specified length
'''
def split_len( cipher, length=SB_LENGTH ):
    return [cipher[i:i+length] for i in range(0, len(cipher), length)]

'''
    Check if our ciphertext is valid by send it at to specifiec url
    And checking the returned value doesn't contain the words specified
    in verification
'''
async def is_valid_cipher( cipher ):
    c = pwn.connect("2018shell1.picoctf.com", 24933)
    c.sendlineafter("cookie?", cipher.encode("hex"))
    resp = c.recvrepeat(3)
    c.close()
    if "invalid padding" not in resp.lower():
        print "invalid cipher not in response:", resp
        return True
    else:
        return False
    #return "invalid padding" not in resp.lower()

'''
    Convert plain list of ints to chars
    And convert pad to '+' or specified char
'''
def compute_word( plain, padding=DEFAULT_PADDING_CHAR ):
    return "".join([chr(c) if (c > 0x08) else padding for c in plain])

'''
    Run padding oracle attack
'''
def attack( cipher, block_length=SB_LENGTH ):
    cipher_block = split_len( cipher, length=block_length )

    results = []

    for i in range(0, len(cipher_block)):
        if i + 1 == len(cipher_block):
            break
        a = len(cipher_block) - 1
        prevblock = cipher_block[a-i-1]
        block = cipher_block[a-i]

        ivals = []
        plain = []
        cprime = chr(0)*SB_LENGTH

        for cprime_idx in range( SB_LENGTH - 1, -1, -1 ):
            # Create a PKCS#7 padding index [0x01, 0x08]
            padding_idx = SB_LENGTH - cprime_idx

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

                guesses

                # If the oracle correctly decrypts the ciphertext
                if is_valid_cipher( ciphertext ):
                    # Calculate the intermediate value
                    intermediate = guess^padding_idx
                    # Save the intermediate value
                    ivals.insert(0, intermediate)
                    # Crack the plain text character
                    plain.insert(0, intermediate^ord(prevblock[cprime_idx]))

                    # We found it, bail out
                    if cprime_idx:
                        print "".join(map(chr, plain))
                        print

                    break

        print "  " + green(ciphertext.encode("hex")) # print final decoded cipher

        print "\nIntermediate values = {}\n".format(ivals)

        plainstr = compute_word(plain)
        results.append(plainstr)

    return results

def main():
    pwn.context.log_level = 'error'
    cookie = "5468697320697320616e204956343536d6ca0a2883280762915414c54e97df1b40871b72f45ec7f9510a080095436d514129e137aaac86a0f7fa8bd3d250b9d1df35b668fcb93f00bb06692560a3fed8a3b523d385f1477b6daac14ff2416c67"
    cookie = [cookie[i:i+2] for i in range(0,len(cookie),2)]
    cookie = map(lambda x: int(x,16), cookie)
    cookie = "".join(map(chr,cookie))
    print "cipher len:", len(cookie)
    print
    word = attack( cookie )

    print "Captcha word is : {} ('+' represents padding)".format("".join(reversed(word)))

    print green("[Done]")


if __name__ == '__main__':
    main()
