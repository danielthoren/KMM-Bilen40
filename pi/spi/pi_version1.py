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
NEWDATAMOTOR = 6

wiringpi.wiringPiSetup()
wiringpi.wiringPiSetupGpio()
if (wiringpi.wiringPiSPISetup(0,5000) == -1):
    print("error in wiringpi setup. Initialization failed!")

wiringpi.pinMode(SSS, OUTPUT)
wiringpi.digitalWrite(SSS, HIGH)
wiringpi.pinMode(SSM, OUTPUT)
wiringpi.digitalWrite(SSM, HIGH)


wiringpi.pinMode(NEWDATAMOTOR, INPUT)
wiringpi.pinMode(NEWDATASENSOR, INPUT)

wiringpi.pinMode(SSS, OUTPUT)
wiringpi.pinMode(SSM, OUTPUT)


'''''''''''''''''
End Setup

'''''''''''''''''

'''
Checks if there is data to receive.
Has needs to be done before Trancieving data, to take load of the AVR.
'''
def hasNewData(pin):
    return wiringpi.digitalRead(pin)


'''
Transceives data with motor, receives one value(rotations per minute, rpm) and
sends two values(speed and angle).
'''
def motorTransceiver(data):
    wiringpi.digitalWrite(SSM, LOW)

    data.append(checksum(data))

    #buff = bytes(data)
    tmp = [66, 22]
    buff = bytes([66, 22, checksum(tmp)])
    retlen, retdata = wiringpi.wiringPiSPIDataRW(0, buff)

    print("length", retlen)

    motor_data = [retdata[0], retdata[1], retdata[2]]

    wiringpi.digitalWrite(SSM, HIGH)

    #removes all reduntant elements in the list. When the incomming data is less big than the
    #outgoing data there must be dummy elements because of the full duplex bus (dummy = 255).
    print("before cleanup: ", motor_data)
    for i in range(len(motor_data)):
        if motor_data[i] == 255:
            print('removed elem: ', i, ' = ', motor_data[i])
            motor_data = motor_data[:i]
            break

    if len(motor_data) > 1 and checksum(motor_data):
        return motor_data[:-1]
    else:
         print("Invalid checksum, data: ", motor_data)
    return None

'''
Receives data from sensor and returns it in a list
'''
def sensorTransceiver():
    
    wiringpi.digitalWrite(SSS, LOW)
    
    buff = bytes([0, 0, 0, 0, 0, 0])
    retlen, retdata = wiringpi.wiringPiSPIDataRW(0, buff)
    
    
    data = [retdata[0], retdata[1], retdata[2], retdata[3], retdata[4], retdata[5]]
    
    wiringpi.digitalWrite(SSS, HIGH)

    if checksum(data):
        return data[:-1]
    return None

'''
Creates a list with values for speed and angle
'''
def motorDataList():
    speed = 10
    angle = 40
    data_list = [speed, angle]
    return data_list

'''
Calculates checksum for received data. 
'''
def checksum(data):
    chk = 0
    _chk = data[-1]
    for elem in data[:-1]:
        chk ^= elem

    return chk == _chk

        
'''''''''''''''''
The Testchamber

'''''''''''''''''
if __name__ == "__main__":

    while True:
        print(wiringpi.digitalRead(6))
        
        if hasNewData(NEWDATASENSOR):

            sensor_data = sensorTransceiver()
            if sensor_data:
                print(sensor_data)
            else:
                print("Invalid checksum.")

        if hasNewData(NEWDATAMOTOR):
             motor_data = motorTransceiver(motorDataList())
            
             if motor_data:
                 print("Motordata")
                 print(motor_data)
        time.sleep(1)

