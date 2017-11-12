#!/usr/bin/python3

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
SSS = 22
SSM = 23
NEWDATA = 5

wiringpi.wiringPiSetupGpio()
if (wiringpi.wiringPiSPISetup(0,5000) == -1):
    print("error in wiringpi setup. Initialization failed!")

wiringpi.pinMode(SSS, OUTPUT)
wiringpi.digitalWrite(SSS, HIGH)


'''''''''''''''''
End Setup

'''''''''''''''''

'''
Checks if there is data to receive.
Has needs to be done before Trancieving data, to take load of the AVR.
'''
def hasNewData():
    return wiringpi.digitalRead(NEWDATA)


'''
Receives data from sensor and returns it in a list
'''
def sensorTransceiver():
    
    wiringpi.digitalWrite(SSS, LOW)
    
    buff = bytes([0, 0, 0, 0, 0, 0])
    retlen, retdata = wiringpi.wiringPiSPIDataRW(0, buff)
    
    
    data = [retdata[0], retdata[1], retdata[2], retdata[3], retdata[4], retdata[5]]

    #print("buff =\t\t",buff)
    #print("retdata =\t", retdata)
    #print("data =\t", data)
    
    wiringpi.digitalWrite(SSS, HIGH)

    if checksum(data):
        return data[:-1]
    return None

'''
Transceives data with motor, receives one value(rotations per minute, rpm) and
sends two values(speed and angle).
'''
def motorTransceiver(data):
    wiringpi.digitalWrite(SSM, LOW)

    buff = bytes(data)
    retlen, retdata = wiringpi.wiringPiSPIDataRW(0, buff)

    motor_data = retdata[2]

    print(motor_data)

    wiringpi.digitalWrite(SSM, HIGH)

    return motor_data


'''
Calculates checksum for received data. 
'''
def checksum(data):
    chk = 0
    _chk = data[-1]
    for elem in data[:-1]:
        chk ^= elem

    #print("Calculated checksum:", chk, "\nReceived checksum:", _chk)
    return chk == _chk

        
'''''''''''''''''
The Testchamber

'''''''''''''''''
if __name__ == "__main__":

    while True:
        if hasNewData():

            data = sensorTransceiver()
            if data:
                #print(hasNewData())
                print(data)
            else:
                print("Invalid checksum.")
