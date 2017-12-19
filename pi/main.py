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
CONES = ((10,0),(360,350),(90,54),(306,270),(53,19),(341,307),(30,10),(350,330))
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
    finished = 6


class main_driver:

    def __init__(self):
        self.state = state.wait
        self.lapCount = 0 #Counts the amount of laps we have driven
        self.pd = PdHandler()
        self.obs = obsFunc()
        self.send_data = sendData()
        self.recv_data = Instruction()
        self.server, self.server_thread = self.init_server()
        self.angle = 80
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
        average0 = 0
        valueCount0 = 0
        average1 = 0
        valueCount1 = 0
        average2 = 0
        valueCount2 = 0
        average3 = 0
        valueCount3 = 0
        average4 = 0
        valueCount4 = 0
        average5 = 0
        valueCount5 = 0
        average6 = 0
        valueCount6 = 0
        averageDistances = [0,0,0,0,0,0,0]
        #for i in range(len(CONES)):
            #Lidarvalue is a list of tuples
        for data in self.lidar_data_np:
                #data[0] is the angle of the meassurment, <18 and >342 is +- 18 degrees
                #from angle 0, i.e straight forward. (The cone forward)
                #data[2] > 0 is the quality of the meassurmetn, 0 is bad.
            if(data[1] <= CONES[0][0] and data[1] >= CONES[0][1] and data[3] > 0):
                average0 += data[2]
                valueCount0 += 1

            elif(data[1] <= CONES[1][0] and data[1] >= CONES[1][1] and data[3] > 0):
                average0 += data[2]
                valueCount0 += 1

            elif(data[1] <= CONES[2][0] and data[1] >= CONES[2][1] and data[3] > 0):
                average1 += data[2]
                valueCount1 += 1

            elif(data[1] <= CONES[3][0] and data[1] >= CONES[3][1] and data[3] > 0):
                average2 += data[2]
                valueCount2 += 1

            elif(data[1] <= CONES[4][0] and data[1] >= CONES[4][1] and data[3] > 0):
                average3 += data[2]
                valueCount3 += 1
                
            elif(data[1] <= CONES[5][0] and data[1] >= CONES[5][1] and data[3] > 0):
                average4 += data[2]
                valueCount4 += 1

            if(data[1] <= CONES[6][0] and data[1] >= CONES[6][1] and data[3] > 0):
                average5 += data[2]
                valueCount5 += 1
                
            if(data[1] <= CONES[7][0] and data[1] >= CONES[7][1] and data[3] > 0):
                average6 += data[2]
                valueCount6 += 1
                
        if(average0 != 0 and valueCount0 != 0):
            #print('average0 :', (average0/valueCount0)/10)
            averageDistances[0] = (int((average0/valueCount0)/10))
            valueCount0 = 0
            average0 = 0
        if(average1 != 0 and valueCount1 != 0):
            #print('average :', (average/valueCount))
            averageDistances[1] = (int((average1/valueCount1)/10))
            valueCount1 = 0
            average1 = 0
        if(average2 != 0 and valueCount2 != 0):
            #print('average :', (average/valueCount))
            averageDistances[2] = (int((average2/valueCount2)/10))
            valueCount2 = 0
            average2 = 0
        if(average3 != 0 and valueCount3 != 0):
            #print('average :', (average/valueCount))
            averageDistances[3] = (int((average3/valueCount3)/10))
            valueCount3 = 0
            average3 = 0
        if(average4 != 0 and valueCount4 != 0):
            #print('average :', (average/valueCount))
            averageDistances[4]= (int((average4/valueCount4)/10))
            valueCount4 = 0
            average4 = 0
        if(average5 != 0 and valueCount5 != 0):
            #print('average5 :', (average5/valueCount5)/10)
            averageDistances[5] = (int((average5/valueCount5)/10))
            valueCount5 = 0
            average5 = 0
        if(average6 != 0 and valueCount6 != 0):
            #print('average6 :', (average6/valueCount6)/10)
            averageDistances[6] = (int((average6/valueCount6)/10))
            valueCount6 = 0
            average6 = 0
        if averageDistances[0] < 10:
                averageDistances[0] = 800
        if averageDistances[5] < 10:
            averageDistances[5] = 800
        if averageDistances[6] < 10:
            averageDistances[6] = 800
        return averageDistances
    
    #Counts the rounds
    def countLaps(self,sensorValue):
        if(sensorValue[4] == 1):
           self.lapCount += 1
        #returns true when roundCount equals GOAL_LAPS
        if self.lapCount == GOAL_LAPS:
            return True
    #Halts the car and lidar
    def halt(self,lidar):
        motorTransceiver([NEUTRALSPEED, NEUTRALWHEELANGLE, SPEEDPGAIN])
        lidar.stop()
        lidar.stop_motor()

    #Starts the lidar
    def start_lidar(self,lidar):
        lidar.start_motor()
        lidar.start_scan()

    '''
    Init the server to commuicate with the gui
    '''
    def init_server(self):
        socketserver.TCPServer.allow_reuse_address = True        
        server = ThreadedTCPServer( (HOST, PORT), ThreadedTCPRequestHandler)
        server.message = b''
        server.sendmessage = b''
        server_thread = threading.Thread(target = server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        return server, server_thread

    '''
    Sends and receives data from/to gui
    '''
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
    '''
    Takes in arguments from gui to drive the car manualy 
    '''        
    def manual_drive(self):
        time.sleep(0.01)
        self.speed = int(100+(self.recv_data.W*150-self.recv_data.S*100))
        self.angle = int(80+((-self.recv_data.AD)*60))   
        self.lidar_data = self.lidar.grab_data()
        self.rpm = motorTransceiver([self.speed, self.angle, SPEEDPGAIN])
    
        if self.rpm != None:
            self.send_data.rpm = self.rpm
        self.send_data.lidar_data = self.lidar_data
        self.send_data.lap = self.lapCount
       

    '''
    If sensormodul has nu data (lapsensor), take in the new data. 
    '''
    def get_sensor_data(self):
        self.sensorValue = [0,0,0,0,0]
        if hasNewDataSensor():
            self.sensorValue = sensorTransceiver() #List of values, 0-3 is sonar, 4 is round count

    '''
    Autonumus drive
    '''
    def auto_drive(self):
        try:    
            sys.stdout.flush()
            self.lidar_data  = self.lidar.grab_data()
            self.lidar_data_np = np.array(self.lidar_data)
            self.averageDistance.clear()
            self.averageDistance = self.calcaverageCones()    
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
            if self.state == state.finished:
                pass
            elif self.state == state.wait:
                self.state = state.start
            else:
                if self.recv_data.auto_mode:
                    self.state = state.auto
                else:
                    self.state = state.manual
        else:
            if self.state == state.finished:
                self.state = state.wait
            elif not self.state == state.wait:
                self.state = state.halt
        


    def drive(self):
        while 1:
            try:
                self.tranceiver()
                self.mode()
                self.get_sensor_data()
                if self.state == state.auto:
                    self.auto_drive()
                    if self.countLaps(self.sensorValue):
                        self.halt(self.lidar)
                        self.state = state.finished
                        
                if self.state == state.manual:
                    self.countLaps(self.sensorValue)
                    self.manual_drive()    
                if self.state == state.halt:
                    print("Halting...")
                    self.halt(self.lidar)
                    self.state = state.wait
                if self.state == state.start:
                    self.start_lidar(self.lidar)
                    self.state = state.manual
                if self.state == state.wait:
                    self.lapCount = 0
                    print("waiting")
                if self.state == state.error:
                    break
                if self.state == state.finished:
                    self.lapCount = 0
                    print("Finished")
                
            except KeyboardInterrupt:
                self.halt(self.lidar)
                self.state = state.error

            except Exception as e:
                print(e)
                self.halt(self.lidar)
                self.state = state.error



def main():
    
    driver = main_driver()
    driver.drive()

if __name__ == '__main__':
    main()


    
