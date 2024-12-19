PRIVATE_KEY = b'xxxx2312b666c5a8ae185effacb354ecb4cc920fbde35495b348350c76fcada8a1183d3f8217c0cbc611b6a40de384b4d48cdfc1477b7d6c0ef367c77d7e6a77'
#i change the first four digits from ???? to xxxx, this is our "attacker"
import os
import sys
import time
from machine import Pin, I2C



def sign_challenge(challenge):
    ''' perform a XOR between private key and challenge value, then return that XOR value'''
    signature = bytes((b ^ PRIVATE_KEY[i % len(PRIVATE_KEY)]) for i, b in enumerate(challenge))
    return signature

def main():
    usb = sys.stdin.buffer
    usb_out = sys.stdout.buffer


    maxtry:int = 3
    while maxtry > 0:
        challenge = usb.read(len(PRIVATE_KEY))

        if challenge and len(challenge) == len(PRIVATE_KEY):
            signature = sign_challenge(challenge)
            usb_out.write(signature)  
            break
        else:
            pass

        time.sleep(0.1)
        maxtry -= 1


main()

