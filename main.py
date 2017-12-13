import car_module as car
import interface_module as interface
import sonar_sensor_module as sensor
import camera_module as cam
from custom_thread import WhileTrueThread

import cv2
from time import sleep
from time import time as current_time
import math

def deinit_modules() :
    car.deinit()
    interface.deinit()
    cam.deinit()

class InputThread (WhileTrueThread) :
    
    def __init__(self, control_values) :
        WhileTrueThread.__init__(self, 0.1)
        self.__control_values = control_values

    def _loop(self) :
        key = interface.get_key_pressed()
    
        if key == 'i' :        self.__control_values.set_direction('forward')  #car.move_forward(duty_cycle)
        elif key == 'k' :    self.__control_values.set_direction('backward') #car.move_backward(duty_cycle)
        elif key == 'j' :    self.__control_values.set_direction('left')     #car.turn_left(duty_cycle)
        elif key == 'l' :   self.__control_values.set_direction('right')    #car.turn_right(duty_cycle)
        elif key == 'space' :   self.__control_values.set_direction('none')     #car.stop()
        elif key == '1' :       self.__control_values.decrease_duty_cycle()     #duty_cycle -= 1
        elif key == '2' :       self.__control_values.increase_duty_cycle()     #duty_cycle += 1
        elif key == 's' :       self.__control_values.set_swaying(not self.__control_values.is_swaying())
        elif key == 'a' :       self.__control_values.set_auto(not self.__control_values.is_auto())
        elif key == 'q' :       self.stop()
        else :                  pass #unknown key detected

        interface.set_info('direction', self.__control_values.get_direction())
        interface.set_info('duty cycle', self.__control_values.get_duty_cycle())
        interface.set_info('sway move', self.__control_values.is_swaying())
        interface.set_info('auto', self.__control_values.is_auto())

class CarThread (WhileTrueThread) :
    
    def __init__(self, control_values) :
        WhileTrueThread.__init__(self, 0.1)
        self.__control_values = control_values
        self.__sway_counter = 0
        self.__prev_time = current_time()
        self.__sway_freq = 1.6
        self.__sway_amp = 0.8
        self.__safe_distance = 8
        self.__prev_direction = 'none'

    def _loop(self) :
        direction = self.__control_values.get_direction()
        duty_cycle = self.__control_values.get_duty_cycle()
        is_auto = self.__control_values.is_auto()

        if is_auto :
            if self.__control_values.get_distance() <= self.__safe_distance :
                car.turn_left(duty_cycle)
            else :
                if not self.__control_values.is_swaying() :
                    car.move_forward(duty_cycle)
                else :
                    self.__sway_counter += (current_time() - self.__prev_time)*math.pi*self.__sway_freq
                    self.__prev_time = current_time()
                    turn_ratio = math.sin(self.__sway_counter)/2*self.__sway_amp + 0.5
                    car.move_forward(duty_cycle, turn_ratio)
        else :
            if direction == 'forward' :
                if not self.__control_values.is_swaying() :
                    car.move_forward(duty_cycle)
                else : 
                    if self.__prev_direction != 'forward' :
                        self.__sway_counter = 0

                    self.__sway_counter += (current_time() - self.__prev_time)*math.pi*self.__sway_freq
                    self.__prev_time = current_time()
                    turn_ratio = math.sin(self.__sway_counter)/2*self.__sway_amp + 0.5
                    car.move_forward(duty_cycle, turn_ratio)
            elif direction == 'backward' :
                car.move_backward(duty_cycle)
            elif direction == 'left' :
                car.turn_left(duty_cycle)
            elif direction == 'right' :
                car.turn_right(duty_cycle)
            elif direction == 'none' :
                car.stop()
            else :
                pass # unknown direction
        
        self.__prev_direction = direction

    
class SonarSensorThread(WhileTrueThread):
    
    def __init__(self, control_values) :
        WhileTrueThread.__init__(self, 0)
        self.__control_values = control_values
        
    def _loop(self):
        front_distance = sensor.check_distance()
        interface.set_info('distance',front_distance)
        self.__control_values.set_distance(front_distance)
        interface.update_screen()

class CamThread(WhileTrueThread):
    
    def __init__(self):
        WhileTrueThread.__init__(self)

    def _prepare(self) :
        self.__frame_count = 0

    def _loop(self):
        raw_image = cam.capture()
        resized_image = cam.shrink_image(raw_image)
        flipped_image = cam.flip_up_down(resized_image)
        self.__frame_count += 1
##        cam.show_image(flipped_image)

##        interface.set_info('frame count', self.__frame_count)
        
        if cv2.waitKey(1) == 27 :
            self.stop()

def main() :
    
    control_values  = car.ControlValues()

    input_thread    = InputThread       (control_values)
    car_thread      = CarThread         (control_values)
    sensor_thread   = SonarSensorThread (control_values)
    camera_thread   = CamThread()

    input_thread.start()
    car_thread.start()
    sensor_thread.start()
    camera_thread.start()

    input_thread.join()
    camera_thread.stop()
    car_thread.stop()
    sensor_thread.stop()
    
    sleep(1)

    deinit_modules()
    
if __name__ == '__main__' :
    main()

