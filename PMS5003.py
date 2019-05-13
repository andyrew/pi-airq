
import serial
import struct
import sys

class PMS5003:
    def __init__(self, serial_terminal="/dev/serial0"):
        self.serial_terminal = serial_terminal
        self.baud_rate = 9600
        self.read()

    def read(self):
        try:
            self.serial_connection = serial.Serial(self.serial_terminal, baud_rate=self.baud_rate)

            # The following block of code is largely taken from Adafruit Learning System Guides
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
                raise overrun

            if len(buffer) < 32:
                raise not_enough

            if buffer[1] != 0x4d:
                buffer.pop(0)
                raise wrong_data

            frame_len = struct.unpack(">H", bytes(buffer[2:4]))[0]
            if frame_len != 28:
                buffer = []
                raise incorrect_data

            frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(buffer[4:]))

            pm10_standard, pm25_standard, pm100_standard, pm10_env, \
                pm25_env, pm100_env, particles_03um, particles_05um, particles_10um, \
                particles_25um, particles_50um, particles_100um, skip, checksum = frame

            check = sum(buffer[0:30])

            if check != checksum:
                buffer = []
                raise bad_checksum

            # End Adafruit Code
            # Thanks Adafruit!

            self.pm10_standard = pm10_standard
            self.pm25_standard = pm25_standard
            self.pm100_standard = pm100_standard
            self.pm10_env = pm10_env
            self.pm25_env = pm25_env
            self.pm100_env = pm100_env
            self.particles_03um = particles_03um 
            self.particles_05um = particles_05um
            self.particles_10um = particles_10um
            self.particles_25um = particles_25um
            self.particles_50um = particles_50um
            self.particles_100um = particles_100um

        except overrun:
            sys.stderr.write("potential overrun avoided - PMS5003 read")
        except not_enough:
            sys.stderr.write("not enough bytes received - PMS5003 read")
        except wrong_data:
            sys.stderr.write("data received doesn't start correctly - PMS5003 read")
        except incorrect_data
            sys.stderr.write("not enough good bytes received - PMS5003 read")
        except bad_checksum:
            sys.stderr.write("checksum doesn't match - PMS5003 read")
        except:
            sys.stderr.write('problem with PMS5003 read')



