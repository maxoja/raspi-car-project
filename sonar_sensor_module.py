from hcsr04sensor import sensor

#distances are in inch unit
#temperature in F
#20 C = 68 F
#25 C = 77 F
#30 C = 86 F

trigger_pin     = 16
echo_pin        = 18

sample_size = 1
sample_interval = 0.05

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
            sample_size = sample_size,
            sample_wait = sample_interval
        )

        # Calculate the distance in inches
        inch_distance = value.distance_imperial(raw_measurement)
        
    except Exception as e:
##        print(e)
        inch_distance = None

    return inch_distance

#### test #########
if __name__ == '__main__' :
    while True :
        print(check_distance())
