#!/usr/bin/python3
import wiringpi
import time
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
SSS = 22
SSM = 27
NEWDATASENSOR = 5

wiringpi.wiringPiSetup()
wiringpi.wiringPiSetupGpio()
if (wiringpi.wiringPiSPISetup(0,5000) == -1):
    print("error in wiringpi setup. Initialization failed!")

wiringpi.pinMode(SSS, OUTPUT)
wiringpi.digitalWrite(SSS, HIGH)
wiringpi.pinMode(SSM, OUTPUT)
wiringpi.digitalWrite(SSM, HIGH)

wiringpi.pinMode(NEWDATASENSOR, INPUT)

wiringpi.pinMode(SSS, OUTPUT)
wiringpi.pinMode(SSM, OUTPUT)


'''''''''''''''''
End Setup

'''''''''''''''''

'''
Checks if there is data to receive from the 'sensormodul'
'''
def hasNewDataSensor():
    return wiringpi.digitalRead(NEWDATASENSOR)


'''
Transceives data with motor, receives one value(rotations per minute, rpm) and
sends two values(speed and angle).

order in 'data' list is following:
[speed, angle]

order in recieved data is following:
[rpm]
'''
def motorTransceiver(data):
    wiringpi.digitalWrite(SSM, LOW)

    data.append(calcChecksum(data))
    buff = bytes([data[0], data[1], data[2]])

    print("data: ", data)
    
    retlen, retdata = wiringpi.wiringPiSPIDataRW(0, buff)

    motor_data = [retdata[0], retdata[1], retdata[2]]

    wiringpi.digitalWrite(SSM, HIGH)

    '''
    removes all reduntant elements in the list. 
    When the incomming data is less big than the
    outgoing data there must be dummy elements 
    because of the full duplex bus (dummy = 255).
    '''
    #print("before cleanup: ", motor_data)
    for i in range(len(motor_data)):
        if motor_data[i] == 255:
            motor_data = motor_data[:i]
            break

    if len(motor_data) > 1 and calcChecksum(motor_data[:-1]) == motor_data[-1]:
        return motor_data[:-1]
    else:
         print("Invalid checksum, data: ", motor_data)
    return None

'''
Receives data from sensor and returns it in a list

order of recieved data is as follows:
[sonar0, sonar1, sonar2, sonar3, lapsensor]
'''
def sensorTransceiver():
    
    wiringpi.digitalWrite(SSS, LOW)
    
    buff = bytes([0, 0, 0, 0, 0, 0])
    retlen, retdata = wiringpi.wiringPiSPIDataRW(0, buff)    
    
    data = [retdata[0], retdata[1], retdata[2], retdata[3], retdata[4], retdata[5]]
    
    wiringpi.digitalWrite(SSS, HIGH)

    if calcChecksum(data[:-1]) == data[-1]:
        return data[:-1]
    return None

'''
Calculates checksum of data. 
'''
def calcChecksum(data):
    chk = 0
    for elem in data:
        chk ^= elem

    return chk

