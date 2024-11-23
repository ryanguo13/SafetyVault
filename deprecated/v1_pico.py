import os
import time
from machine import Pin

# 私钥 (测试用)
PRIVATE_KEY = b"abcdefghijklmnopqrstuvwx12345678"

# 模拟签名函数
def sign_challenge(challenge):
    return os.urandom(32)  # 固定返回 32 字节伪签名

# 设置 LED
led = Pin(25, Pin.OUT)
led.value(0)

def main():
    print("Main Program is starting!")
    import sys
    usb = sys.stdin.buffer  # 使用标准输入作为 USB 通信
    usb_out = sys.stdout.buffer  # 使用标准输出作为 USB 通信

    while True:
        led.value(1)
        print("Program started") # 点亮 LED，表示程序运行中
        challenge = usb.read(32)  # 读取挑战字符串
        if challenge:
            print("Received challenge:", challenge)
            if len(challenge) == 32:
                signature = sign_challenge(challenge)
                usb_out.write(signature)  # 发送签名
            else:
                usb_out.write(b"ERR")  # 数据长度错误
                print("Invalid challenge length")
        led.value(0)  # 关闭 LED
        time.sleep(0.1)

main()
