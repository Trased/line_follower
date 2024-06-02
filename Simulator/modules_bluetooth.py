import serial
import time

def crc8(data):
    """
    Compute CRC8 using the One-Wire CRC8 algorithm.
    """
    crc = 0x00
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if (crc & 0x01):
                crc = (crc >> 1) ^ 0x8C  # X8 + X5 + X4 + 1
            else:
                crc >>= 1
    return crc

def format_message(message, message_counter, source_type, source_id, destination_id):
    """
    Format the message according to the specified format.
    """
    preamble = [0x55, 0x55, 0x55, 0x33]

    # Convert the message into key-value pairs (example: "key1:value1;key2:value2")
    pairs = []
    for pair in message.split(';'):
        if ':' in pair:
            key, value = pair.split(':', 1)
            pairs.append(ord(key))  # Convert key to ASCII
            pairs.append(len(value))
            pairs.extend(value.encode())  # Append value

    # Calculate lengths
    content_length = len(pairs)
    length_negated = 0xFF - content_length

    # Construct the message
    msg = preamble + [content_length, length_negated] + list(source_type) + [source_id, destination_id, message_counter] + pairs

    # Calculate CRC8 and append
    crc = crc8(msg[4:])  # CRC8 calculation starts from the length field
    msg.append(crc)
    msg.extend(map(ord, '\r\n'))
    return bytes(msg)

def decode_message(received_message):
    """
    Decode the received message and extract key-value pairs.
    """
    try:
        print(received_message)
        key = received_message[10]
        message_size = received_message[11]
        message_offset = 12 + message_size
        message = received_message[12:message_offset]
        return {chr(key): message.decode('ascii')}
    except Exception as e:
        print(f"Error decoding message: {e}")
        return None
def connect_bluetooth(device_file, baud_rate=9600):
    """
    Connect to the HC-05 Bluetooth module.
    """
    try:
        bt_serial = serial.Serial(device_file, baud_rate)
        print(f"Connected to HC-05 on {device_file}")
        return bt_serial
    except serial.SerialException as e:
        print(f"Error connecting to {device_file}: {e}")
        return None

def send_message(bt_serial, message, message_counter, source_type, source_id, destination_id):
    """
    Send a message to the HC-05 Bluetooth module.
    """
    try:
        formatted_message = format_message(message, message_counter, source_type, source_id, destination_id)
        print(formatted_message)
        bt_serial.write(formatted_message)
        print(f"Sent: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")

def receive_message(bt_serial):
    """
    Receive a message from the HC-05 Bluetooth module.
    """
    try:
        bt_serial.timeout = 1
        if bt_serial.in_waiting > 0:
            message = bt_serial.readline()
            return message
    except Exception as e:
        print(f"Error receiving message: {e}")
    return None