from pid import *
from speed import *
from lidar import memelidar
import numpy as np
from spi import *
import sys
import time
from obs_detect import *
from enum import Enum
from instructions import *
from threadTCPServer import *
import threading
import socketserver


SPEEDPGAIN = 10

'''
Defines the hitbox derived from the sonar sensors
The values are in the following order:

[sonar1, sonar2, sonar3, sonar4]
'''

HOST_l = ""
HITBOX = [30, 30, 30, 30]
TURNTHRESHOLD = 40  #Defines the threshold for when in a curve or not
#Defines between wich degrees each cone is. Two first cones are handles as special
#case since they represent one cone in actuality
CONES = ((10,0),(360,350),(90,54),(306,270),(53,19),(341,307),(20,10),(350,340))
NEUTRALWHEELANGLE = 80
PRODUCTSPEEDSTRAIGHT = 0.5
PRODUCTSPEEDTURN = 0.2
MAXSPEED = 200
NEUTRALSPEED = 100
GOAL_LAPS = 3 # Amount of laps that the robot should drive

lapCount = 0 #Counts the amount of laps we have driven

class state(Enum):
    auto = 0
    manual = 1
    halt = 2
    wait = 3
    start = 4

state = state.auto

'''
Calculates the avarage distance for the measurments in each cone and saves
them in 'averageDistance' variable. The first two values in the 'CONES' constant
are handled as a special case since theese represent the cone that exists in them
gap (between 1 and 360 degrees).
'''
def calcaverageCones(lidarData):
    average = 0
    valueCount = 0
    averageDistance = []
    for i in range(len(CONES)):
        #Lidarvalue is a list of tuples
        for data in lidarData:
            #data[0] is the angle of the meassurment, <18 and >342 is +- 18 degrees
            #from angle 0, i.e straight forward. (The cone forward)
            #data[2] > 0 is the quality of the meassurmetn, 0 is bad.
            if(data[1] <= CONES[i][0] and data[1] >= CONES[i][1] and data[3] > 0):
                average += data[2]
                valueCount += 1

        if i == 0:
            pass
        elif(average != 0 and valueCount != 0):
            averageDistance.append(int((average/valueCount)/10))
            if averageDistance[0] < 10:
                averageDistance[0] = 100
            valueCount = 0
            average = 0
        else:
            averageDistance.append(0)

    return averageDistance

#Counts the rounds
def countLaps(sensorValue):
        global lapCount
        if(sensorValue[4] == 1):
           lapCount += 1
           print(lapCount)
           #returns true when roundCount equals GOAL_LAPS
        if lapCount == GOAL_LAPS:
            return True

def halt(lidar):
    motorTransceiver([NEUTRALSPEED, NEUTRALWHEELANGLE, SPEEDPGAIN])
    lidar.stop()
    lidar.stop_motor()

def start_lidar(lidar):
    lidar.start_motor()
    lidar.start_scan()


def init_server():
    HOST, PORT = HOST_l, 10000
    socketserver.TCPServer.allow_reuse_address = True

    server = ThreadedTCPServer( (HOST, PORT), ThreadedTCPRequestHandler)
    server.message = b''
    server.sendmessage = b''
    #server.recvd = False

    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server, server_thread 

def main():
    speed = 200 # 0 <= speed <= 200, 100 is neutral
    pd = PdHandler()
    obs = obsFunc()
    global state
    send_data = sendData()
    recv_data = Instruction()
    #Pid == true => use pid in motormodul, if false, dont use pid.
    pid = True
    server, server_thread = init_server()
    angle = 90
    speed = 100
    lidar = memelidar.PyLidar()
    data_temp = [[0,0,0,0]]
    averageDistance = [0,0,0,0,0] #holds average distance for all cones
    

    while 1:
        if server.message and server.message != b'1':
            recv_data.decode(server.message)
            recv_data.printSelf()
        send = send_data.encode()
        server.sendmessage = send
        pGain = recv_data.p
        dGain = recv_data.d
        if state == state.halt:
            state == state.wait
        if not recv_data.run and state != state.wait:
            state = state.halt
        elif recv_data.run:
            if recv_data.auto_mode:
                if state == state.wait:
                    print("here")
                    state = state.start
                else:
                    print("hjer")
                    state = state.auto
            elif not recv_data.auto_mode:
                if state == state.wait:
                    state = state.start
                else:
                    state = state.manual
            else:
                state = state.wait
        else:
            state = state.wait  
                
        
        if state == state.auto:
            print("Auto")
            try:    
                sys.stdout.flush()
                #os.system('clear')
                sensorValue = [0,0,0,0,0]
                if hasNewDataSensor():
                    sensorValue = sensorTransceiver() #List of values, 0-3 is sonar, 4 is round count
                data = np.array(data_temp)
                data_temp  = lidar.grab_data()
                averageDistance.clear()
                averageDistance = calcaverageCones(data)
                #for i in range(len(averageDistance)):
                    #print("cone", i , "distance :", averageDistance[i])

           
                if countLaps(sensorValue):
                    state = state.halt
                    print("Three laps done")
             
                pd.setVal = obs.obsDetect(data)
                pd.regulateAngle(sensorValue, averageDistance)
                
                rpm = motorTransceiver([regulateSpeed(averageDistance[0], averageDistance[5], averageDistance[6]), pd.currOutAngle, SPEEDPGAIN])
                
                if rpm != None:
                    send_data.rpm = rpm
                #print("Rpm: ", rpm)
                send_data.lidar_data = data_temp
                send_data.lap = lapCount
                
                
            except KeyboardInterrupt:
                halt(lidar)
                break

            except Exception as e:
                print(e)
                halt(lidar)
                break

        elif state == state.manual:
            time.sleep(0.01)
            data_temp  = lidar.grab_data()
            send_data.lidar_data = data_temp
            print("Manual")
            if recv_data.W:
               speed = 150
            elif recv_data.S:
                speed = 50
            else:
                speed = 100
            if recv_data == 0:
                angle = 90
            elif recv_data == 1:
                angle = 140 
            elif recv_data == -1:
                angle = 40

            rpm = motorTransceiver([speed, angle, SPEEDPGAIN])
            if rpm != None:
                send_data.rpm = rpm
            #print("Rpm: ", rpm)
            send_data.lidar_data = data_temp
            send_data.lap = lapCount
                
        elif state == state.halt:
            send_data.lidar_data = data_temp
            print("Halting..")
            halt(lidar)
            state = state.wait

        elif state == state.start:
            send_data.lidar_data = data_temp
            start_lidar(lidar)
        elif state == state.wait:
            send_data.lidar_data = data_temp
            print("waiting")
            #time.sleep(1)

if __name__ == '__main__':
    main()


    
