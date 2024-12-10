
import RPi.GPIO as GPIO
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



servo_pin = 12  # BCM 引脚号（物理引脚 32）????what am i writing
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

servo = GPIO.PWM(servo_pin, 50)  

try:
    #now lock the vault
    set_servo_angle(servo, 210)
    time.sleep(2)
    #now unlock the vault
    set_servo_angle(servo, 90)
    time.sleep(2)

finally:
    servo.stop()
    GPIO.cleanup()
