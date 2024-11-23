import os
import serial

# 配置 USB 串行端口
USB_PORT = "/dev/cu.usbmodem11101"  # 根据实际设备修改
BAUD_RATE = 115200

# 测试用共享密钥（与 Pico 的 PRIVATE_KEY 对应）
SHARED_KEY = b"abcdefghijklmnopqrstuvwx12345678"

# 签名验证函数
def verify_signature(challenge, signature):
    expected_signature = bytes(
        (b ^ SHARED_KEY[i % len(SHARED_KEY)]) for i, b in enumerate(challenge)
    )
    return signature == expected_signature

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

        # 验证签名
        if verify_signature(challenge, signature):
            print("Signature verified: Access granted")
        else:
            print("Verification failed: Access denied")

main()