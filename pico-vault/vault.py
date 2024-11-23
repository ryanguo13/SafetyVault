import os
import time
import serial

'''this is the vault simulation, these code will burn into the vault micro-controller'''
USB_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200
PRIVATE_KEY = b'71652312b666c5a8ae185effacb354ecb4cc920fbde35495b348350c76fcada8a1183d3f8217c0cbc611b6a40de384b4d48cdfc1477b7d6c0ef367c77d7e6a77'

def verify_signature(challenge, signature, private_key):
    ''' perform a XOR between private key and challenge value, then return that XOR value'''
    expected_signature = bytes((b ^ private_key[i % len(private_key)]) for i, b in enumerate(challenge))
    return expected_signature == signature

def main():
    print("Connecting to hardware wallet...")
    with serial.Serial(USB_PORT, BAUD_RATE) as ser:
        challenge = os.urandom(len(PRIVATE_KEY))

        maxtry = 3
        while maxtry > 0:
            
            print(f"Challenge sent")
            ser.write(challenge)
            
# ok not ok ok not 

#  同步异步 3次没用 
#  gui
#  图纸
#  display i2c  (wait line)
#  vault 软件编写

            print("wait end, read start")
            raw_signature = ser.read(len(PRIVATE_KEY))
            # this is sync block, so it will wait until receive input
            print(f"Raw signature received ")

            if len(raw_signature) == len(PRIVATE_KEY) and verify_signature(challenge, raw_signature, PRIVATE_KEY):
                print("Verification successful: Access granted")
                exit(0)
                #here UNLOCK VAULT!!!
            else:
                print("Verification failed: Access denied")
            
            maxtry -= 1
            time.sleep(1)
            print("try again\n")

        exit(1)#it means three try fail, systemd should record this.
        

if __name__ == "__main__":
    main()