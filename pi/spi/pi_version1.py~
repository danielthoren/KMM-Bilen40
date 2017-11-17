import wiringpi

'''''''''''''''''
Setup

'''''''''''''''''

INPUT = 0
OUTPUT = 1
LOW = 0
HIGH = 1
MOSI = 10
MISO = 9
SCLK = 11
SS = 22

if (wiringpi.wiringPiSPISetup(0,5000) == -1):
    print("error in wiringpi setup. Initialization failed!")

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(SS, OUTPUT)
wiringpi.digitalWrite(SS, HIGH)
print('Starting')
wiringpi.delay(2000)

'''''''''''''''''
End Setup

'''''''''''''''''

#Receives data from sensor and returns it in a list
def sensorTransceiver():
    wiringpi.digitalWrite(SS, LOW)
    
    buff = bytes([0, 0, 0, 0, 0])
    retlen, retdata = wiringpi.wiringPiSPIDataRW(0, buff)

    indata_list = [retdata[0], retdata[1], retdata[2], retdata[3], retdata[4]]

    print(indata_list)

    wiringpi.delay(1000)
    
    wiringpi.digitalWrite(SS, HIGH)
    
    return indata_list

'''
#Probably not going to be needed
def sensorSendData(int_data):
    wiringpi.digitalWrite(SS, LOW)

    buff = bytes(int_data)
    print(buff)
    retlen, retdata = wiringpi.wiringPiSPIDataRW(0, buff)

    wiringpi.digitalWrite(SS, HIGH)
    
    return
'''

#Transceives data with motor, receives one value(rotations per minute, rpm) and
#sends two values(speed and angle).
def motorTransceiver(data):
    wiringpi.digitalWrite(SS, LOW)

    buff = bytes(data)
    retlen, retdata = wiringpi.wiringPiSPIDataRW(0, buff)

    motor_data = retdata[2]

    print(motor_data)

    wiringpi.digitalWrite(SS, HIGH)

    return motor_data


'''''''''''''''''
The Testchamber

'''''''''''''''''

sensorTransceiver()

wiringpi.delay(1000)

sensorTransceiver()

speed = 5

angle = 30

motor_list = [0, speed, angle]

#motorTransceiver(motor_list)



