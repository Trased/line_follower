from modules_bluetooth import ATUART
from modules_ir_receiver import NEC_8, callback
from machine import Pin
import modules_shared

def run_receivers():
    pin_ir = Pin(5, Pin.IN)
    ir = NEC_8(pin_ir, callback)

    ser = ATUART(0, 9600, timeout=100, timeout_char=1)  # tx=6, rx=7 GND=8
    print('Automatic message sending over UART started! (use Ctrl+C to terminate!)')
    try:
        while not modules_shared.need_to_stop:
            ser.shell()
    except KeyboardInterrupt:
        print('Shell terminated!')


