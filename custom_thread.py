import car_module as car
import interface_module as interface
import sonar_sensor_module as sensor
import camera_module as cam
import sign_detection_module as detection

import threading
from time import sleep
from time import time as current_time
import math
import cv2

class WhileTrueThread(threading.Thread) :
    def __init__(self, interval = 0) :
        threading.Thread.__init__(self)
        self.__interval = interval
        self.__stop = False

    def stop(self) :
        self.__stop = True
        
    def _prepare(self) :
        pass

    def _loop(self) :
        pass

    def _end(self) :
        pass

    def run(self) :
        
        self._prepare()
        
        while not self.__stop :
            self._loop()
            sleep(self.__interval)

        self._end()
            

class InputThread (WhileTrueThread) :
    
    def __init__(self, control_values) :
        WhileTrueThread.__init__(self, 0.1)
        self.__control_values = control_values

    def _loop(self) :
        key = interface.get_key_pressed()
        current_mode = self.__control_values.get_mode()

        if current_mode == 'drive' :
            #keys that available on drive mode only
            if key == 'i' :         self.__control_values.set_direction('forward')  #car.move_forward(duty_cycle)
            elif key == 'k' :       self.__control_values.set_direction('backward') #car.move_backward(duty_cycle)
            elif key == 'j' :       self.__control_values.set_direction('left')     #car.turn_left(duty_cycle)
            elif key == 'l' :       self.__control_values.set_direction('right')    #car.turn_right(duty_cycle)
            elif key == 'space' :   self.__control_values.set_direction('none')     #car.stop()

        if key == '1' :         self.__control_values.decrease_duty_cycle()     #duty_cycle -= 1
        elif key == '2' :       self.__control_values.increase_duty_cycle()     #duty_cycle += 1
        elif key == 's' :       self.__control_values.toggle_swaying() 
        elif key == 'q' :       self.stop()
        elif key == 'a' :
                                self.__control_values.toggle_mode()
                                self.__control_values.set_direction('none')
        else :                  pass #unknown key detected

        interface.set_info('direction', self.__control_values.get_direction())
        interface.set_info('duty cycle',self.__control_values.get_duty_cycle())
        interface.set_info('sway move', self.__control_values.is_swaying())
        interface.set_info('mode',      self.__control_values.get_mode())

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
        self.__outbound_distance = 1100

    def _loop(self) :
        control_values  = self.__control_values
        direction       = control_values.get_direction()
        duty_cycle      = control_values.get_duty_cycle()
        mode            = control_values.get_mode()
        is_swaying      = control_values.is_swaying()
        distance        = control_values.get_distance()

        too_close       = False
        outbound        = False
        
        if distance != None :
            too_close  = distance <= self.__safe_distance
            outbound   = distance >= self.__outbound_distance
        
        #auto drive mode
        if mode == 'auto' :
            if direction == 'forward' :
                if too_close or outbound : 
                    car.turn_left(duty_cycle)
                else :
                    if not is_swaying :
                        turn_ratio = 0.5
                    else :
                        if self.__prev_direction != 'forward' :
                            self.__sway_counter = 0
                            
                        self.__sway_counter += (current_time() - self.__prev_time)*math.pi*self.__sway_freq
                        self.__prev_time = current_time()
                        turn_ratio = math.sin(self.__sway_counter)/2*self.__sway_amp + 0.5

                    car.move_forward(duty_cycle, turn_ratio)
                    
            elif direction == 'left' :
                car.move_forward(duty_cycle, 0.25)
            elif direction == 'right' :
                car.move_forward(duty_cycle, 0.75)
            elif direction == 'backward' :
                car.move_backward(duty_cycle)
            elif direction == 'none' :
                car.stop()
            else :
                pass

        #control drive / sign recognition mode
        elif mode == 'drive' :
            if direction == 'forward' :
                if not is_swaying :
                    turn_ratio = 0.5
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
    
    def __init__(self, control_values):
        WhileTrueThread.__init__(self)
        self.__control_values = control_values

    def _prepare(self) :
        self.__frame_count = 0

    def _loop(self):
        if self.__control_values.get_mode() != 'auto' :
            return
        
        raw_image = cam.capture()
        self.__frame_count += 1
        interface.set_info('frame count', self.__frame_count)
        
        sign_direction = detection.findTrafficSign(raw_image)
        interface.set_info('detection', sign_direction)

        if sign_direction == None :
            pass
        else :
            self.__control_values.set_direction(sign_direction)

        interface.set_info('direction', self.__control_values.get_direction())
        
        if cv2.waitKey(1) == 27 :
            self.stop()
