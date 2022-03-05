## alias python='python3.7'
## sudo pip3 install adafruit-circuitpython-servokit

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
import time

while True:
        for i in range(0, 180, 1):
            kit.servo[0].angle = i
            kit.servo[1].angle = i
            time.sleep(.01)

        for i in range(180, 0, -1):
            kit.servo[0].angle = i
            kit.servo[1].angle = i
            time.sleep(.01)
