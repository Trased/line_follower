from modules_bluetooth import ATUART

ser = ATUART(0, 9600, timeout=100, timeout_char=1)  # tx=6, rx=7 GND=8
print('Automatic message sending over UART started! (use Ctrl+C to terminate!)')
try:
    while True:
        ser.shell()
except KeyboardInterrupt:
    print('Shell terminated!')
