from threading import Thread
import time
import serial
import numpy as np

last_received = ''

COMport = 'com5'

def receiving(serial_port):
    global last_received
    buffer = ''
    while True:
        buffer += serial_port.read_all()
        if '\n' in buffer:
            lines = buffer.split('\n')  # Guaranteed to have at least 2 entries
            last_received = lines[-2]
            # If the Arduino sends lots of empty lines, you'll lose the last
            # filled line, so you could make the above statement conditional
            # like so: if lines[-2]: last_received = lines[-2]
            buffer = lines[-1]
            print last_received


class SerialData(object):
    def __init__(self):
        try:
            self.serial_port = serial.Serial(COMport,115200)
        except serial.serialutil.SerialException:
            # no serial connection
            self.serial_port = None
        else:
            Thread(target=receiving, args=(self.serial_port,)).start()

    def send(self, data):
        self.serial_port.write(data + ",")

    def __del__(self):
        if self.serial_port is not None:
            self.serial_port.close()

if __name__ == '__main__':
    s = SerialData()
    while True:
        a = 1000
        while a < 2000:
            a += 1
            s.send(str(a))
            time.sleep(0.01)
        while a > 1000:
            a -= 1
            s.send(str(a))
            time.sleep(0.01)