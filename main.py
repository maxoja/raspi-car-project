import car_module as car
import interface_module as interface
import sonar_sensor_module as sensor

import curses
from custom_thread import WhileTrueThread

from time import sleep

def deinit_modules() :
    car.deinit()
    interface.deinit()

class InputThread (WhileTrueThread) :
    def __init__(self, control_values) :
        WhileTrueThread.__init__(self, 0.1)
        self.__control_values = control_values

    def _loop(self) :
        key = interface.get_key_pressed()
    
        if key == 'up' :        self.__control_values.set_direction('forward')  #car.move_forward(duty_cycle)
##        elif key == 'down' :    self.__control_values.set_direction('backward') #car.move_backward(duty_cycle)
        elif key == 'left' :    self.__control_values.set_direction('left')     #car.turn_left(duty_cycle)
        elif key == 'right' :   self.__control_values.set_direction('right')    #car.turn_right(duty_cycle)
        elif key == 'space' :   self.__control_values.set_direction('none')         #car.stop()
        elif key == '1' :       self.__control_values.decrease_duty_cycle()     #duty_cycle -= 1
        elif key == '2' :       self.__control_values.increase_duty_cycle()     #duty_cycle += 1
        elif key == 'q' :       self.stop()
        else :                  pass #unknown key detected

class CarThread (WhileTrueThread) :
    def __init__(self, control_values) :
        WhileTrueThread.__init__(self, 0.1)
        self.__control_values = control_values

    def _loop(self) :
        direction = self.__control_values.get_direction()
        duty_cycle = self.__control_values.get_duty_cycle()

        if direction == 'forward' :
            if self.__control_values.get_distance() <= 6 :
                car.turn_left(duty_cycle)
            else :
                car.move_forward(duty_cycle)
##        elif direction == 'backward' :
##            car.move_backward(duty_cycle)
        elif direction == 'left' :
            car.turn_left(duty_cycle)
        elif direction == 'right' :
            car.turn_right(duty_cycle)
        elif direction == 'none' :
            car.stop()
        else :
            pass # unknown direction

    

class SonarSensorThread(WhileTrueThread):
        def __init__(self, control_values) :
            WhileTrueThread.__init__(self, 0.1)
            self.__control_values = control_values
            
        def _loop(self):
            front_distance = sensor.check_distance()
            interface.set_line(7,'distance',front_distance)
            self.__control_values.set_distance(front_distance)
                    
if __name__ == '__main__' :
    control_values  = car.ControlValues()

    input_thread    = InputThread       (control_values)
    car_thread      = CarThread         (control_values)
    sensor_thread   = SonarSensorThread (control_values)

    input_thread.start()
    car_thread.start()
    sensor_thread.start()

    input_thread.join()
    car_thread.stop()
    sensor_thread.stop()
    
    sleep(1)

    deinit_modules()
