from hcsr04sensor import sensor

#distances are in inch unit
#temperature in F
#20 C = 68 F
#25 C = 77 F
#30 C = 86 F

trigger_pin     = 23
echo_pin        = 24

def check_distance() :

    try :
        
        value = sensor.Measurement(
            trigger_pin,
            echo_pin,
            temperature     = 68,
            unit            = 'imperial',
            round_to        = 2
        )

        raw_measurement = value.raw_distance(
            sample_size = 3,
            sample_wait = 0.04
        )

        # Calculate the distance in inches
        inch_distance = value.distance_imperial(raw_measurement)
        
    except :
        
        inch_distance = None

    return inch_distance

#### unit test #####
if __name__ == '__main__' :
    import threading
    
    class SonarSensorThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            
        def run(self):
            while True:
                print(check_distance())

    def test():
        distance = SonarSensorThread()
        distance.start()
        distance.join()
        
    if __name__ == "__main__":
        test()
