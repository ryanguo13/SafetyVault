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

def first_key_verify():

    print("Connecting to hardware wallet...")
    with serial.Serial(USB_PORT, BAUD_RATE) as ser:

        """
        dead
        """
        #challenge = os.urandom(len(PRIVATE_KEY))
        challenge = generate_safe_random(len(PRIVATE_KEY), 33, 126)


        maxtry = 3
        while maxtry > 0:
            time.sleep(0.5)
            
            print(f"Challenge sent")
            ser.write(challenge)
            print("wait end, read start")
            raw_signature = ser.read(len(PRIVATE_KEY))

            # this is sync block, so it will wait until receive input
            print(f"Raw signature received ")

            if len(raw_signature) == len(PRIVATE_KEY) and verify_signature(challenge, raw_signature, PRIVATE_KEY):
                print("Verification successful: Access granted")
                return True
                #here UNLOCK VAULT!!!
            else:
                print("Verification failed: Access denied")
            
            maxtry -= 1
            time.sleep(1)
            print("try again\n")
        exit(1)#it means three try fail, systemd should record this.
        

def second_key_verify():
    """deprecated"""
    pass


#import RPi.GPIO as GPIO
import time

def set_servo_angle(pwm, angle):
    """
    adjust pwm to adjust sg90 angle
    :param pwm: a PWN micropython object, such as PWM(PIN(0))
    :param angle: the valid para is ranging from 90 to 210，
    90 is unlock, 210 is lock.
    """
    #transform the angle to PWM duty(功率）
    angle = int(angle)
    if ((angle < 90) or (angle > 210)):
        return
    #above code prevent you from breaking the machine structure
    #机械结构是焊死的，超过这个角度，电机和保险柜必有一尸
    if((angle!=90) and (angle != 210)):
        return
    # for convenience, only "lock" and "unlock" state is allowed
    #this save me from judging the state of lock.
    duty = 2500 + int((angle / 180) * 5000)  # 0度对应 2.5%，180度对应 7.5%
    pwm.duty_u16(duty)





if __name__ == "__main__":
    time.sleep(2)
    #just set a timer waiting for private key ready. increase success rate
    checkresult = False
    checkresult = first_key_verify()
    #second_key_verify()
    
    if checkresult == True:

        servo_pin = 12  
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)

        servo = GPIO.PWM(servo_pin, 50)  

        try:
            servo.start(12.5)
            time.sleep(7)

            servo.ChangeDutyCycle(7.5)
            time.sleep(2)
        finally:
            servo.stop()
            GPIO.cleanup()
