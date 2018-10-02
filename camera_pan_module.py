import RPi.GPIO as GPIO
from time import sleep



#It is expected to have 2 servos where both works simultaneously

#One for horizontal direction
#Two for vertical direction

class Servo:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BOARD)
        self.__servo_pin = pin       #Selected Pin
        self.degree = 0
        GPIO.setup(pin, GPIO.OUT)    #Set a pin as a GPIO OutputPin
        self.pwm = GPIO.PWM(pin, 50) # The frequency is fixed at 50Hz to match with the equation in SetAngle Method
        self.pwm.start(0)            # Start PWM


    def setAngle(self, angle):
        self.angle = angle
        duty = angle / 18 + 2
        GPIO.output(self.__servo_pin, True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(self.__servo_pin, False)
        self.pwm.ChangeDutyCycle(0)


    def setDefaultAngle(self):
        self.degree = 90
        self.setAngle(self.degree)

    def increaseAngle(self):
        if (self.degree <= 0):
            self.degree = (360 - self.degree) % 360
        if(self.degree > 360):
            self.degree = (self.degree) % 360
        self.degree += 1

    def decreaseAngle(self):
        if(self.degree <= 0):
            self.degree = (360 - self.degree) % 360
        self.degree -= 1

    def clear(self):
        self.pwm.stop()
        GPIO.cleanup()

