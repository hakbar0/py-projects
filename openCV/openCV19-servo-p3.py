import Adafruit_PCA9685
import time

## init the pca9685 using desired address/or bus
pwm = Adafruit_PCA9685.PCA9685(address = 0x40, busnum = 1)

## Number of servo
servo_num = 2

servo_min = 150 # min pulse length
servo_max = 600 # max pulse length
servo_offset = 50

## set frequency
pwm.set_pwm_freq(60)

pwm.set_pwm(0,0,600)
time.sleep(2)
pwm.set_pwm(0,0,150)
time.sleep(2)

pwm.set_pwm(0,0,150)
time.sleep(2)
pwm.set_pwm(0,0,600)
time.sleep(2)

pwm.set_pwm(1,0,600)
time.sleep(2)
pwm.set_pwm(1,0,150)
time.sleep(2)

pwm.set_pwm(1,0,150)
time.sleep(2)
pwm.set_pwm(1,0,600)
time.sleep(2)




# while True:
## move servp pm each channel
    # for i in range(servo_num):
    #     pwm.set_pwm(i, 0, servo_max - servo_offset)
    #     time.sleep(0.4)
    
    

