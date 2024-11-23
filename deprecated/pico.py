import os
import time
from machine import Pin

PRIVATE_KEY = b"abcdefghijklmnopqrstuvwx12345678"

def sign_challenge(challenge):
    signature = bytes((b ^ PRIVATE_KEY[i % len(PRIVATE_KEY)]) for i, b in enumerate(challenge))
    return signature

led = Pin(25, Pin.OUT)
led.value(0)

def main():
    import sys
    usb = sys.stdin.buffer
    usb_out = sys.stdout.buffer

    print("Pico hardware wallet is ready.")
    try:
        while True:
            led.value(0)
            challenge = usb.read(32)
            if challenge and len(challenge) == 32:
                led.value(1)
                signature = sign_challenge(challenge)
                usb_out.write(signature)  # 发送签名
                led.value(0)
            else:
                usb_out.write(b"ERR")  # 返回错误
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting program...")
        led.value(0)

main()
