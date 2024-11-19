import os
import serial

# 配置 USB 串行端口
USB_PORT = "/dev/cu.usbmodem11101"  # 修改为实际设备路径
BAUD_RATE = 115200

def main():
    with serial.Serial(USB_PORT, BAUD_RATE, timeout=2) as ser:
        print("Connecting to hardware wallet...")

        # 生成挑战字符串（随机 32 字节）
        challenge = os.urandom(32)
        print("Challenge sent:", challenge.hex())
        ser.write(challenge)

        # 接收签名
        signature = ser.read(32)
        print("Raw signature received:", signature.hex())
        if len(signature) != 32:
            print("Error: Invalid signature length")
            return

        print("Signature received:", signature.hex())

main()