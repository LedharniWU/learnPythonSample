import serial
import struct

use_port = 'COM3'

_serial = serial.Serial(use_port)
_serial.baudrate = 921600
_serial.parity = serial.PARITY_NONE
_serial.bytesize = serial.EIGHTBITS
_serial.stopbits = serial.STOPBITS_ONE
_serial.timeout = 5 #sec

commands = [ 0xAA, 0x81, 0x02, 0x01 ]

for cmd in commands:
    data = struct.pack("B", cmd)
    print("tx: ", data)
    _serial.write(data)

_serial.flush()

rx = _serial.readline()

print("rx: ", rx)

print("アンパック", struct.unpack("B",rx))

_serial.close()