import serial
import time
import struct
import time

'''
Pressure in Pascals,
Temperature in Celsius degrees
wind speed in meters per second
flow in CMM
'''

class hd350:
    def __init__(self):
        self.device = 'COM4'
        self.createDatabaseDirectory()

        with open('/home/pi/Documentos/HD350Manometer/configuration.json','r') as file:
            self.deviceConf = json.load(file)

        self.connectToHD350()
        mHandMessage = bytearray([0xaa, 0xbb, 0x0c])
        mHandConnectMetter = bytearray([0xaa, 0xbb, 0x01])

        while True:
            m = mHandMessage
            s.write(m)
            m = mHandConnectMetter
            s.write(m)
            for i in range(5):
                d = s.read(46)
                data = decodeData(d)
                if data:
                    time.sleep(10)


    def createDatabaseDirectory(self):
        path = self.deviceConf['databasePath']
        os.makedirs(path, exist_ok=True)
        os.chdir(path)

    def createCsvfile(self):
        self.createDatabaseDirectory()
        csvfile = self.deviceConf['databasefile']
        if not os.path.isfile(csvfile):
            variables = self.deviceConf['variables']
            arrayOfVariableNames = ['time']
            for v, value in variables.items():
                arrayOfVariableNames.append(value)
            with open(csvfile, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=arrayOfVariableNames)
                writer.writeheader()


    def connectToHD350(self):
        self.s = serial.Serial(self.device, baudrate = 9600, xonxoff=False, bytesize = 8, parity='N', stopbits=1, timeout=1)

    def decodeData(self, m):

        if len(m) != 46:
            return None
        else:
            rawPress  = m[8:12]
            rawWind  = m[12:16]
            rawFlow = m[16:20]
            rawTemp = m[20:22]
            data1 = struct.unpack('f', rawData1)[0]
            press = struct.unpack('f', rawPress)[0]
            wind = struct.unpack('f', rawWind)[0]
            flow = struct.unpack('f', rawFlow)[0]
            temp = float(struct.unpack('h', rawTemp)[0]/10.)
            timestamp = int(time.time())
            dict = {'timestamp':timestamp,
                    'press': press,
                    'flow':flow,
                    'wind': wind,
                    'temp': temp}
            return dict




#for j in baudrate_array:
#s = serial.Serial('COM4', baudrate = j, xonxoff=False, bytesize = 8, parity='N', stopbits=1, timeout = 120)

s = serial.Serial('COM4', baudrate = 9600, xonxoff=False, bytesize = 8, parity='N', stopbits=1, timeout=1)
#VEL, TEMP, FLOW
#s.write(b'press\n')
#m = bytearray(b'\xaa\xbb\x0c\xaa\xbb\x01\xaa\xbb\x0c')
s.flushInput()

mPress = bytearray([0xaa, 0xbb, 0x11])# 0xaa, 0xbb, 0x0c]
mSpeed = bytearray([0xaa, 0xbb, 0x11])# 0xaa, 0xbb, 0x0c]
mFlow = bytearray([0xaa, 0xbb, 0x11])# 0xaa, 0xbb, 0x0c]ss



while True:


    print("-----------------------------------------------------------------------------------------------------------------------------------------------")
    for i in range(5):
        #shutdown = bytearray([0xaa, 0xbb, 0x0d])# 0xaa, 0xbb, 0x0c]
        #print ("Comunicacion 1:\n",s.readline())#.decode())
        #print ("m =",s.readline())#.decode())
        d = s.read(46)
        data = decodeData(d)
        if data:
            imp = "Temperatura: %.2f, presion: %.2f, flujo: %.2f, viento: %.2f"  %(data['temp'], data['press'], data['flow'], data['wind'] )
            print (imp)


    print("-----------------------------------------------------------------------------------------------------------------------------------------------")
    #s.write(m)
    #if m:#
    #    print(m)
    #s.close()
