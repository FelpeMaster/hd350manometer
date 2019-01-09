import serial
import time
import struct
import time
import json
import os
import csv

#mPress = bytearray([0xaa, 0xbb, 0x11])# 0xaa, 0xbb, 0x0c]
#mSpeed = bytearray([0xaa, 0xbb, 0x11])# 0xaa, 0xbb, 0x0c]
#mFlow = bytearray([0xaa, 0xbb, 0x11])# 0xaa, 0xbb, 0x0c]ss

'''
Pressure in Pascals,
Temperature in Celsius degrees
wind speed in meters per second
flow in CMM
'''

class hd350:
    def __init__(self):
        with open('/home/pi/Documentos/hd350manometer/configuration.json','r') as file:
            self.deviceConf = json.load(file)
        self.port = self.deviceConf['port']
        self.createDatabaseDirectory()
        self.connectToHD350()
        self.createCsvfile()
        mHandMessage = bytearray([0xaa, 0xbb, 0x0c])
        mHandConnectMetter = bytearray([0xaa, 0xbb, 0x01])
        while True:
            m = mHandMessage
            self.s.write(m)
            m = mHandConnectMetter
            self.s.write(m)
            for i in range(5):
                d = self.s.read(46)
                data = self.decodeData(d)
                if data:
                    self.addData(data)
                    print (data)
            self.s.flushInput()

    def createDatabaseDirectory(self):
        path = self.deviceConf['databasePath']
        os.makedirs(path, exist_ok=True)
        os.chdir(path)

    def createCsvfile(self):
        self.createDatabaseDirectory()
        self.csvfile = self.deviceConf['databasefile']
        if not os.path.isfile(self.csvfile):
            variables = self.deviceConf['variables']
            arrayOfVariableNames = ['timestamp']
            for v, value in variables.items():
                arrayOfVariableNames.append(value)
            with open(self.csvfile, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=arrayOfVariableNames)
                writer.writeheader()

    def addData(self, measurementsArray):
        with open(self.csvfile, 'a') as f:
            w = csv.writer(f)
            w.writerow(measurementsArray)

    def connectToHD350(self):
        self.s = serial.Serial(self.port, baudrate = 9600, xonxoff=False, bytesize = 8, parity='N', stopbits=1)

    def decodeData(self, m):
        if len(m) != 46:
            return None
        else:
            rawPress  = m[8:12]
            rawWind  = m[12:16]
            rawFlow = m[16:20]
            rawTemp = m[20:22]
            press = struct.unpack('f', rawPress)[0]
            wind = struct.unpack('f', rawWind)[0]
            flow = struct.unpack('f', rawFlow)[0]
            temp = float(struct.unpack('h', rawTemp)[0]/10.)
            timestamp = int(time.time())
            #dict = {'timestamp':timestamp,
            #        'pressure': press,
            #        'flow':flow,
            #        'windspeed': wind,
            #        'temperature': temp}
            measurementsArray = [timestamp, temperature, flow, wind, press]
            return measurementsArray

if __name__ == "__main__":
    hd350 = hd350()
