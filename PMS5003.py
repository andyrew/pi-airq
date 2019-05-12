
import serial
import struct

class PMS5003:
    def __init__(self, serial_terminal="/dev/serial0"):
        self.serial_terminal = serial_terminal
        self.baud_rate = 9600
        self.read()

    def read(self):
        self.serial_connection = serial.Serial(self.serial_terminal, baud_rate=self.baud_rate)

        # The following block of code is from Adafruit Learning System Guides
        #
        # github.com/adafruit/Adafruit_Learning_System_Guides/PMS5003_Air_Quality_Sensor/PMS5003_CircuitPython/main.py
        # Copyright (c) 2018 Adafruit Industries
        #
        # Permission is hereby granted, free of charge, to any person obtaining a copy
        # of this software and associated documentation files (the "Software"), to deal
        # in the Software without restriction, including without limitation the rights
        # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        # copies of the Software, and to permit persons to whom the Software is
        # furnished to do so, subject to the following conditions:
        #
        # The above copyright notice and this permission notice shall be included in all
        # copies or substantial portions of the Software.
        buffer = []
        data = self.serial_connection.read(32)   # read up to 32 bytes
        buffer += list(data)

        while buffer and buffer[0] != 0x42:
            buffer.pop(0)

        if len(buffer) > 200:
            buffer = []  # avoid an overrun if all bad data
        if len(buffer) < 32:
            continue

        if buffer[1] != 0x4d:
            buffer.pop(0)
            continue

        frame_len = struct.unpack(">H", bytes(buffer[2:4]))[0]
        if frame_len != 28:
            buffer = []
            continue

        frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(buffer[4:]))

        self.pm10_standard, self.pm25_standard, self.pm100_standard, self.pm10_env, \
            self.pm25_env, self.pm100_env, self.particles_03um, self.particles_05um, self.particles_10um, \
            self.particles_25um, self.particles_50um, self.particles_100um, skip, checksum = frame

        check = sum(buffer[0:30])

        if check != checksum:
            buffer = []
            continue

        # End Adafruit Code
        # Thanks Adafruit!



