PRIVATE_KEY = b'71652312b666c5a8ae185effacb354ecb4cc920fbde35495b348350c76fcada8a1183d3f8217c0cbc611b6a40de384b4d48cdfc1477b7d6c0ef367c77d7e6a77'
import sys
import time
import ssd1306
from machine import Pin, I2C



def sign_challenge(challenge):
    ''' perform a XOR between private key and challenge value, then return that XOR value'''
    signature = bytes((b ^ PRIVATE_KEY[i % len(PRIVATE_KEY)]) for i, b in enumerate(challenge))
    return signature

def display_init():
    i2c = I2C(1, sda=Pin(26), scl=Pin(27))
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    return display

def main():
    display = display_init()
    display.poweron()
    usb = sys.stdin.buffer
    usb_out = sys.stdout.buffer


    maxtry:int = 3
    while maxtry > 0:
        display.text("reading rand",5,5,1)
        display.show()
        challenge = usb.read(len(PRIVATE_KEY))

        if challenge and len(challenge) == len(PRIVATE_KEY):
            signature = sign_challenge(challenge)
            usb_out.write(signature)  
            display.text("verifying",5,18,1)
            break
        else:
            display.text("invalid",5,18,1)
            pass
        display.show()

        time.sleep(0.1)
        maxtry -= 1
        display.text("try again",5,30,1)
        display.show()

    display.text("success", 5, 45, 1)
    display.show()

    while True:
        display.rect(100, 45, 120, 65, 1)
        display.show()
        time.sleep(0.75)

main()
