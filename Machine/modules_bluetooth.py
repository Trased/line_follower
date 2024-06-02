from machine import UART, Pin, ADC
import modules_shared

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
        key = received_message[10]
        message_size = received_message[11]
        message_offset = 12 + message_size
        message = received_message[12:message_offset]
        return {chr(key): message.decode('ascii')}
    except Exception as e:
        print(f"Error decoding message: {e}")
        return None

class ATUART(UART):
    source_type = 'R'.encode()
    source_id = 0x32
    destination_id = 0x44
    message_counter = 0

    def req(self, echo=True):
        self.responses = []
        ln = self.readline()
        if ln:
            self.responses.append(ln)
            try:
                self.responses[-1] = self.responses[-1].decode('ascii').strip()
            except UnicodeError:
                pass
            if echo:
                decoded_data = decode_message(ln)       
                key, value = list(decoded_data.items())[0]
                if key == '1':
                    with modules_shared.variable_lock:
                        modules_shared.action = value
                if key == '2':
                    if value == 'slow':
                        with modules_shared.variable_lock:
                            if modules_shared.speed > 0.003:
                                modules_shared.speed = modules_shared.speed - 0.001
                    elif value == 'fast':
                        with modules_shared.variable_lock:
                            if modules_shared.speed < 0.01:
                                modules_shared.speed = modules_shared.speed + 0.001
        return ln
    
    def res(self):
        """Send a message over the UART connection."""
        try:
            speed_message = format_message(f"2:{modules_shared.speed}", self.message_counter, self.source_type, self.source_id, self.destination_id)
            self.write(speed_message)
            self.message_counter = (self.message_counter + 1) % 256
            action_message = format_message(f"2:{modules_shared.action}", self.message_counter, self.source_type, self.source_id, self.destination_id)
            self.write(action_message)
            self.message_counter = (self.message_counter + 1) % 256

        except Exception as e:
            print(f"Error sending message: {e}")
    
    def shell(self): # deschide un terminal interactiv de comunicare prin conexiunea UART asociata instantei
        self.req()
        self.res()
        time.sleep(1)



