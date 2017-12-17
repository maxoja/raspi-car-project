import interface_module as interface
import camera_module as cam
from custom_thread import InputThread, CarThread, SonarSensorThread, CamThread
import car_module as car

from time import sleep
import os

def deinit_modules() :
    car.deinit()
    interface.deinit()
    cam.deinit()

def dance() :
    os.popen("./dance")
    sleep(2)

def main() :
    
    dance()
    
    car.init_gpio_pins()
    
    control_values  = car.ControlValues()

    input_thread    = InputThread       (control_values)
    car_thread      = CarThread         (control_values)
    sensor_thread   = SonarSensorThread (control_values)
    camera_thread   = CamThread         (control_values)

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

