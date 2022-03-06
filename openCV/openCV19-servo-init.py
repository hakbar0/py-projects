import Adafruit_PCA9685
import time

## init the pca9685 using desired address/or bus
pwm = Adafruit_PCA9685.PCA9685(address = 0x40, busnum = 1)

down_min = 150 # min pulse length
down_max = 600 # max pulse length
down_mid = 300 # init pos of camera


up_min = 450 # min pulse length
up_max = 600 # max pulse length
up_mid = 500 # init pos of camera

## set frequency
pwm.set_pwm_freq(60)

pwm.set_pwm(1,0,up_mid)
pwm.set_pwm(0,0,down_mid)
