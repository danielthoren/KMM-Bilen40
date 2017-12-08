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


HOST = ""
PORT = 10000

SPEEDPGAIN = 10
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


class state(Enum):
    auto = 0
    manual = 1
    halt = 2
    wait = 3
    start = 4
    error = 5


class main_driver:

    def __init__(self):
        self.state = state.wait
        self.lapCount = 0 #Counts the amount of laps we have driven
        self.pd = PdHandler()
        self.obs = obsFunc()
        self.send_data = sendData()
        self.recv_data = Instruction()
        self.server, self.server_thread = self.init_server()
        self.angle = 90
        self.speed = 100
        self.lidar = memelidar.PyLidar()
        self.lidar_data = [[0,0,0,0]]
        self.averageDistance = [] #holds average distance for all cones
        self.lidar_data_np = np.array(self.lidar_data)
        self.sensorValue = [0,0,0,0,0]
        self.rpm = [0]
    
    '''
    Calculates the avarage distance for the measurments in each cone and saves
    them in 'averageDistance' variable. The first two values in the 'CONES' constant
    are handled as a special case since theese represent the cone that exists in them
    gap (between 1 and 360 degrees).
    '''
    def calcaverageCones(self):
        #print('calc')
        average = 0
        valueCount = 0
        averageDistances = []
        for i in range(len(CONES)):
            #Lidarvalue is a list of tuples
            for data in self.lidar_data_np:
                #data[0] is the angle of the meassurment, <18 and >342 is +- 18 degrees
                #from angle 0, i.e straight forward. (The cone forward)
                #data[2] > 0 is the quality of the meassurmetn, 0 is bad.
                if(data[1] <= CONES[i][0] and data[1] >= CONES[i][1] and data[3] > 0):
                    average += data[2]
                    valueCount += 1

            if i == 0:
                pass
            elif(average != 0 and valueCount != 0):
                #print('average :', (average/valueCount))
                averageDistances.append(int((average/valueCount)/10))
                if averageDistances[0] < 10:
                    averageDistances[0] = 100
                valueCount = 0
                average = 0
            else:
                averageDistances.append(0)
        return averageDistances
    
    #Counts the rounds
    def countLaps(self,sensorValue):
        if(sensorValue[4] == 1):
           self.lapCount += 1
        #returns true when roundCount equals GOAL_LAPS
        if self.lapCount == GOAL_LAPS:
            return True

    def halt(self,lidar):
        motorTransceiver([NEUTRALSPEED, NEUTRALWHEELANGLE, SPEEDPGAIN])
        lidar.stop()
        lidar.stop_motor()

        
    def start_lidar(self,lidar):
        lidar.start_motor()
        lidar.start_scan()

        
    def init_server(self):
        socketserver.TCPServer.allow_reuse_address = True        
        server = ThreadedTCPServer( (HOST, PORT), ThreadedTCPRequestHandler)
        server.message = b''
        server.sendmessage = b''
        server_thread = threading.Thread(target = server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        return server, server_thread

    
    def tranceiver(self):
        if self.server.message and self.server.message != b'1':
            self.recv_data.decode(self.server.message)
            self.recv_data.printSelf()
            self.pGain = self.recv_data.p
            self.dGain = self.recv_data.d
        
        if self.rpm != None:
            self.send_data.rpm = self.rpm
        self.send_data.lidar_data = self.lidar_data
        self.send_data.lap = self.lapCount
        send = self.send_data.encode()
        self.server.sendmessage = send
        
        
    def manual_drive(self):
        time.sleep(0.01)
        if self.recv_data.W:
            self.speed = 150
        elif self.recv_data.S:
            self.speed = 50
        else:
            self.speed = 100
        if self.recv_data.AD == 0:
            self.angle = 90
        elif self.recv_data.AD == 1:
            self.angle = 140 
        elif self.recv_data.AD == -1:
            self.angle = 40
            
        self.lidar_data = self.lidar.grab_data()
        self.rpm = motorTransceiver([self.speed, self.angle, SPEEDPGAIN])
        if self.rpm != None:
            self.send_data.rpm = self.rpm
        self.send_data.lidar_data = self.lidar_data
        self.send_data.lap = self.lapCount

    def auto_drive(self):
        try:    
            sys.stdout.flush()
            #os.system('clear')
            self.sensorValue = [0,0,0,0,0]
            if hasNewDataSensor():
                self.sensorValue = sensorTransceiver() #List of values, 0-3 is sonar, 4 is round count
            self.lidar_data  = self.lidar.grab_data()
            self.lidar_data_np = np.array(self.lidar_data)
            self.averageDistance.clear()
            self.averageDistance = self.calcaverageCones()
            #print('averageDist :', self.averageDistance)
            
            if self.countLaps(self.sensorValue):
                self.state = state.halt
                
            self.pd.setVal = self.obs.obsDetect(self.lidar_data_np)
            self.pd.regulateAngle(self.sensorValue, self.averageDistance)
                
            self.rpm = motorTransceiver(
                [regulateSpeed(self.averageDistance[0],
                               self.averageDistance[5],
                               self.averageDistance[6]),
                               self.pd.currOutAngle,
                               SPEEDPGAIN])
                
                
        except KeyboardInterrupt:
            self.halt(self.lidar)
            self.state = state.error

        except Exception as e:
            print(e)
            self.halt(self.lidar)
            self.state = state.error


    
    def mode(self):
        if self.recv_data.run:
            if self.state == state.wait:
                self.state = state.start
            else:
                if self.recv_data.auto_mode:
                    self.state = state.auto
                else:
                    self.state = state.manual
        else:
            if not self.state == state.wait:
                self.state = state.halt
        


    def drive(self):
        while 1:
            self.tranceiver()
            self.mode()
            if self.state == state.auto:
                self.auto_drive()
            if self.state == state.manual:
                self.manual_drive()    
            if self.state == state.halt:
                print("Halting...")
                self.halt(self.lidar)
                self.state = state.wait
            if self.state == state.start:
                self.start_lidar(self.lidar)
                self.state = state.manual
            if self.state == state.wait:
                print("waiting")
                #time.sleep(1)
            if self.state == state.error:
                break


def main():
    
    driver = main_driver()
    driver.drive()

if __name__ == '__main__':
    main()


    
