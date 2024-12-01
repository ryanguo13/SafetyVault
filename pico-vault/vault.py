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

def generate_safe_random(length, min_val=33, max_val=126):
    """
    Generate random bytes within a specified ASCII range.

    Args:
        length (int): Number of bytes to generate.
        min_val (int): Minimum ASCII value (inclusive).
        max_val (int): Maximum ASCII value (inclusive).

    Returns:
        bytes: Random bytes within the specified range.
    """
    range_size = max_val - min_val + 1
    random_bytes = os.urandom(length)
    # Map each byte to the range [min_val, max_val]
    return bytes(min_val + (byte % range_size) for byte in random_bytes)

def main():

    '''debug session'''
    logfile = open("./pico_output_log", "ab") 

        
    
    
    
    
    

    print("Connecting to hardware wallet...")
    with serial.Serial(USB_PORT, BAUD_RATE) as ser:

        """
        I spend fucking 6 hours debugging for below line of code, only because of 
        historical terminal escape sequence reasons. I won't for give REPL and the 
        AI who generate this code. I will kill you all!😠😡
        """
        #challenge = os.urandom(len(PRIVATE_KEY))
        challenge = generate_safe_random(len(PRIVATE_KEY), 33, 126)


        maxtry = 3
        while maxtry > 0:
            time.sleep(0.5)
            
            print(f"Challenge sent")
            ser.write(challenge)

            '''debug session'''
            logfile.write(b'writed content from vault\n')
            logfile.write(challenge.hex().encode('utf-8'))
            logfile.write(b'\n')
# ok not ok ok not 

#  同步异步 3次没用 
#  gui
#  图纸
#  display i2c  (wait line)
#  vault 软件编写

            print("wait end, read start")
            raw_signature = ser.read(len(PRIVATE_KEY))

            '''debug session'''
            logfile.write(b'readed content from pico\n')
            logfile.write(raw_signature.hex().encode('utf-8'))
            logfile.write(b'\n')

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

        logfile.write(b'one test terminated\n\n')
        logfile.close()
        exit(1)#it means three try fail, systemd should record this.
        

if __name__ == "__main__":
    main()