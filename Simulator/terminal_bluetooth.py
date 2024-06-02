import time
import select
import sys
from modules_bluetooth import connect_bluetooth, send_message, receive_message

def main():
    # Replace '/dev/rfcomm0' with your actual device file
    device_file = '/dev/rfcomm0'

    bt_serial = connect_bluetooth(device_file)

    if not bt_serial:
        return

    try:
        message_counter = 0
        while True:
                # format key1:value1
            ready_to_send, _, _ = select.select([sys.stdin], [], [], 0)
            if ready_to_send and sys.stdin.read(1) != '':
                message = input()
                send_message(bt_serial, message, message_counter,'M'.encode(), 0x44, 0x32)
                message_counter = (message_counter + 1) % 256
                time.sleep(1)
            
            received_message = receive_message(bt_serial)
            if received_message:
                print(f"Message from HC-05: {received_message}")
    except KeyboardInterrupt:
        print("Exiting program.")

    bt_serial.close()
    print("Disconnected from HC-05.")

if __name__ == "__main__":
    main()
