import utime
from machine import Pin, ADC
# Motor Pins
pinsLeft = [15, 14, 13, 12]
pinsRight = [19, 18, 17, 16]

phasesRight = [Pin(pin, Pin.OUT) for pin in pinsRight]
phasesLeft = [Pin(pin, Pin.OUT) for pin in pinsLeft]

wave_drive = [
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [1, 0, 0, 1]
]

def go_forward(phase):
    for pinL, pinR, value in zip(phasesLeft, phasesRight, phase):
        pinL.value(value)
        pinR.value(value)
        
def go_right(phase):
    for pinL, pinR, value in zip(phasesLeft, phasesRight, phase):
        pinL.value(value)
        pinR.value([0, 0, 0, 0])
        
def go_left(phase):
    for pinL, pinR, value in zip(phasesLeft, phasesRight, phase):
        pinL.value([0, 0, 0, 0])
        pinR.value(value)

# ADC with Pull-Up Class
class ADCwithPullUp(ADC):
    def __init__(self, gpio, adc_vref=3.3):
        self.gpio = gpio
        self.adc_vref = adc_vref
        adc_pin = Pin(gpio, mode=Pin.IN, pull=Pin.PULL_UP)
        super().__init__(adc_pin)
        adc_pin = Pin(gpio, mode=Pin.IN, pull=Pin.PULL_UP)
        
    def sample(self):
        self.adc_value = self.read_u16()
        # Convert the ADC value to voltage
        self.voltage = (self.adc_value / 65535) * self.adc_vref
        return self.voltage

# Setup sensors and LED
adcs = list(map(ADCwithPullUp, [28, 27, 26]))
LED_Ir = Pin(22, mode=Pin.OUT)
LED_Ir.off()

def read_sensors():
    LED_Ir.on()
    sensor_values = list([adc.sample() for adc in adcs])
    LED_Ir.off()
    return list([1 if value < 1.0 else 0 for value in sensor_values])

# Line Following Algorithm

def follow_line(speed):
    sensor_values = read_sensors()
    print(sensor_values)
    # Basic line following logic based on sensor readings  
    for phase in wave_drive:                
        if (sensor_values == [1, 1, 0]) or (sensor_values == [1, 0, 0]):
            go_right(phase)
        elif (sensor_values == [0, 1, 1]) or (sensor_values == [0, 0, 1]):
            go_left(phase)
        elif sensor_values == [0, 0, 0]:
            pass
        else:
            go_forward(phase)
        utime.sleep(speed) 
    


