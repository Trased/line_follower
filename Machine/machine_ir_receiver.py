from modules_ir_receiver import NEC_8, callback
from machine import Pin

pin_ir = Pin(5, Pin.IN)
ir = NEC_8(pin_ir, callback)

"""
22 == go
13 == stop
24 == speed_up
82 == slow_down
"""