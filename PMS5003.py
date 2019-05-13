
import serial
import struct
import sys
import bisect

aqi_breakpoints =       [ 0,   50,  100,  150,   200,   300,   400,   500 ]
aqi_pm25_breakpoints =  [ 0, 12.1, 35.5, 55.5, 150.5, 250.5, 350.5, 500.5 ]

class PMS5003:
    def __init__(self, serial_terminal="/dev/serial0"):
        self.serial_terminal = serial_terminal
        self.baudrate = 9600
        self.read()

    def read(self):
        try:
            self.serial_connection = serial.Serial(self.serial_terminal, baudrate=self.baudrate)

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
                raise RuntimeError("potential overrun avoided - PMS5003 read")

            if len(buffer) < 32:
                raise RuntimeError("not enough bytes received - PMS5003 read")

            if buffer[1] != 0x4d:
                buffer.pop(0)
                raise RuntimeError("data received doesn't start correctly - PMS5003 read")

            frame_len = struct.unpack(">H", bytes(buffer[2:4]))[0]
            if frame_len != 28:
                buffer = []
                raise RuntimeError("not enough good bytes received - PMS5003 read")

            frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(buffer[4:]))

            pm10_standard, pm25_standard, pm100_standard, pm10_env, \
                pm25_env, pm100_env, particles_03um, particles_05um, particles_10um, \
                particles_25um, particles_50um, particles_100um, skip, checksum = frame

            check = sum(buffer[0:30])

            if check != checksum:
                buffer = []
                raise RuntimeError("checksum doesn't match - PMS5003 read")

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

        except:
            sys.stderr.write('problem with PMS5003 read')

        self.calc_aq_index()


    def calc_aq_index(self):
        # find breakpoints
        idx_pm25 = bisect.bisect_left(aqi_pm25_breakpoints, self.pm10_standard)
        self.aqi_pm25 = int (( aqi_breakpoints[idx_pm25] - aqi_breakpoints[idx_pm25-1] ) / (aqi_pm25_breakpoints[idx_pm25] - aqi_pm25_breakpoints[idx_pm25-1]) * \
                        ( self.pm25_standard - aqi_pm25_breakpoints[idx_pm25-1] ) + aqi_breakpoints[idx_pm25-1] )




