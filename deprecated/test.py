import os
import serial

USB_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200
PRIVATE_KEY = b"abcdefghijklmnopqrstuvwx12345678"

def verify_signature(challenge, signature, private_key):
    expected_signature = bytes((b ^ private_key[i % len(private_key)]) for i, b in enumerate(challenge))
    return expected_signature == signature

def main():
    print("Connecting to hardware wallet...")
    with serial.Serial(USB_PORT, BAUD_RATE, timeout=2) as ser:
        challenge = os.urandom(32)
        print(f"Challenge sent: {challenge.hex()}")
        ser.write(challenge)

        raw_signature = ser.read(32)
        print(f"Raw signature received: {raw_signature.hex()}")

        if len(raw_signature) == 32 and verify_signature(challenge, raw_signature, PRIVATE_KEY):
            print("Verification successful: Access granted")
        else:
            print("Verification failed: Access denied")

if __name__ == "__main__":
    main()