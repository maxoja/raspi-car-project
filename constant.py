import Rpi.GPIO
import sys

#Put all the constants into a single python file
servoVertical =17
servoHorizontal = 18

## initialize ####
pwm_frequency = 50
pwm_pins = dict()

pin_left_a = 13
pin_left_b = 15
pin_right_a = 7
pin_right_b = 11

trigger_pin     = 16
echo_pin        = 18

sample_size = 1
sample_interval = 0.05