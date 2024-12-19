import os
import sys
import time
import serial
import datetime
import vault_util.udevrunner.udevrunner as serialrecorder

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

def first_key_verify() -> list:
    """
    return a list in such format: [boolean: success_or_not, object:picokey_serial]
    one call this function always need to manually close the serial port
    """

    print("Connecting to hardware wallet...")
    ser =  serial.Serial(USB_PORT, BAUD_RATE)

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
            return [True, ser]
            #here UNLOCK VAULT!!!
        else:
            print("Verification failed: Access denied")
        
        maxtry -= 1
        time.sleep(1)
        print("try again\n")
    return [False, ser]#it means three try fail, systemd should record this.

def second_key_verify():
    """deprecated"""
    pass

#import RPi.GPIO as GPIO

"""Deprecated"""
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
    if((angle!=90) and (angle != 210)):
        return
    # for convenience, only "lock" and "unlock" state is allowed
    #this save me from judging the state of lock.
    duty = 2500 + int((angle / 180) * 5000)  # 0度对应 2.5%，180度对应 7.5%
    pwm.duty_u16(duty)

class recorder:
    log:None
    def __init__(self, path):
        self.log = open(path, "a")
        pass

    
    def printk(self,report:list):
        """
        Args:
            report (list): [0] should be the path of the device
            [1] should be the device serial number
        """
        #report time
        line_content = "Key-verify Fail. Time: "
        line_content += f"{datetime.datetime.now()}\n"
        self.log.write(line_content)

        #report attacker detailed
        line_content = "Attacker Device Detailed:\n"
        line_content += "Device Type: Respberry Pico\n"
        line_content += f"Device Serial Number: {report[1]}\n"
        self.log.write(line_content)
        self.log.write("\n")

        pass

    def close(self):
        self.log.close()
        pass
    

class Cust_interrupt:
    def __init__(self):
        pass

    def mastercallSerialJudge(self, slave:object, message:str):
        """
        master send message to slave, if no slave, master raise an soft Interrupt

        Args:
            message: message from master
        Raises:
            Exception: if no slave
        """
        while True:
            time.sleep(0.5)
            slave.write(message)

    def pyudevJudge(self, path):
        pass
        


    def pathexistJudge(self, path):
        """
        Interrupt based on path
        Args:
            path: path of the usb device under /dev
        Raises:
            Exception: if the path is not exist
        """
        while True:
            #keep program running until user unplug the key
            time.sleep(0.5)
            if not os.path.exists(path):
                print("key removed")
                raise Exception("key removed")#soft Interrupt
        

if __name__ == "__main__":
    time.sleep(1)
    #just set a timer waiting for private key ready. increase success rate
    checkresult = False
    try:
        if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
            loggertxt = sys.argv[1]
        else:
            loggertxt = "/home/phage/codev/SafetyVault/pico_vault/pico_eject_errlog"
        
        log_recorder = recorder(loggertxt)
        serial_recorder = serialrecorder.udevrunner()
        serial_recorder.connect("/dev/ttyACM0")


        key_return = first_key_verify()
        checkresult = key_return[0]
        #second_key_verify()



        
        if checkresult == True:
            print("opendoor")
            """
            servo_pin = 12  
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(servo_pin, GPIO.OUT)

            servo = GPIO.PWM(servo_pin, 50)  

            servo.start(12.5)#unlock
            time.sleep(2)
            """
            Cust_interrupt().mastercallSerialJudge(message=b"/dev/ttyACM0", slave=key_return[1])
            #Cust_interrupt().pathexistJudge("/dev/ttyACM0")
        else:
            attacker_serial_id = serial_recorder.query_connected_info()
            attacker_detail_list = ["/dev/ttyACM0", attacker_serial_id]
            log_recorder.printk(report=attacker_detail_list)

            
    except Exception as e:
        print(type(e))
        print(e)
    finally:
        print("close door")
        log_recorder.close()
        key_return[1].close()
        '''
        servo.ChangeDutyCycle(7.5)
        time.sleep(1)
        servo.stop()
        GPIO.cleanup()
        key_return[1].close()
        '''
