import RPi.GPIO as GPIO
from time import sleep

def deinit() :
    __cleanup_gpio()
    
def stop() :
    __set_duty_cycle_for_pins(0, 0, 0, 0)

def turn_left(duty_cycle):
    __set_duty_cycle_for_pins(0, duty_cycle, duty_cycle, 0)

def turn_right(duty_cycle):
    __set_duty_cycle_for_pins(duty_cycle, 0, 0, duty_cycle)
    
def move_forward(duty_cycle):
    __set_duty_cycle_for_pins(duty_cycle, 0, duty_cycle, 0)

##def move_backward(duty_cycle):
##    __set_duty_cycle_for_pins(0, duty_cycle, 0, duty_cycle)

def __set_duty_cycle(pin_id, dc) :
    pwm_pins[pin_id].ChangeDutyCycle(dc)

def __set_duty_cycle_for_pins(a,b,c,d) :
    __set_duty_cycle(pin_left_a,a)
    __set_duty_cycle(pin_left_b,b)
    __set_duty_cycle(pin_right_a,c)
    __set_duty_cycle(pin_right_b,d)
    
def __cleanup_gpio() :
    GPIO.cleanup()

def __init_pwm_pin(pin_id) :
    pwm_pins[pin_id] = GPIO.PWM(pin_id, pwm_frequency)
    pwm_pins[pin_id].start(0)

def __init_output_pin(pin_id) :
    GPIO.setup(pin_id, GPIO.OUT)
    
def __init_gpio_pins() :
    GPIO.setmode(GPIO.BOARD)

    __init_output_pin(pin_left_a)
    __init_output_pin(pin_left_b)
    __init_output_pin(pin_right_a)
    __init_output_pin(pin_right_b)

    __init_pwm_pin(pin_left_a)
    __init_pwm_pin(pin_left_b)
    __init_pwm_pin(pin_right_a)
    __init_pwm_pin(pin_right_b)

class ControlValues :
    def  __init__(self) :
        self.direction = 'none'
        self.duty_cycle = 50
        self.distance = None

    def set_distance(self, distance) :
        self.distance = distance

    def set_direction(self, direction) :
        self.direction = direction

    def set_duty_cycle(self, duty_cycle) :
        self.duty_cycle = duty_cycle
        self.duty_cycle = 100 if self.duty_cycle > 100 else self.duty_cycle
        self.duty_cycle = 0 if self.duty_cycle < 0 else self.duty_cycle

    def increase_duty_cycle(self) :
        self.set_duty_cycle(self.duty_cycle+1)

    def decrease_duty_cycle(self) :
        self.set_duty_cycle(self.duty_cycle-1)

    def get_duty_cycle(self) :
        return self.duty_cycle

    def get_direction(self) :
        return self.direction

    def get_distance(self) :
        return self.distance

## initialize ####
pwm_frequency = 50
pwm_pins = dict()

pin_left_a = 13
pin_left_b = 15
pin_right_a = 7
pin_right_b = 11

__init_gpio_pins()
