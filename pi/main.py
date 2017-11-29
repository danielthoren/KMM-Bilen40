from pid import *
from speed import *
from lidar import memelidar
import numpy as np
from spi import *
import sys
import time

GOAL_LAPS = 3 # Amount of laps that the robot should drive

'''
Defines the hitbox derived from the sonar sensors
The values are in the following order:

[sonar1, sonar2, sonar3, sonar4]
'''
HITBOX = [30, 30, 30, 30]
TURNTHRESHOLD = 40  #Defines the threshold for when in a curve or not
#Defines between wich degrees each cone is. Two first cones are handles as special
#case since they represent one cone in actuality
CONES = ((18,0),(360,342),(90,54),(306,270),(53,19),(341,307))
NEUTRALWHEELANGLE = 80
PRODUCTSPEEDSTRAIGHT = 0.5
PRODUCTSPEEDTURN = 0.2
MAXSPEED = 200
NEUTRALSPEED = 100

'''
Calculates the avarage distance for the measurments in each cone and saves
them in 'averageDistance' variable. The first two values in the 'CONES' constant
are handled as a special case since theese represent the cone that exists in them
gap (between 1 and 360 degrees).
'''
def calcaverageCones(lidarData):
    average = 0
    valueCount = 0
    averageDistance = [0,0,0,0,0]
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
            averageDistance[i - 1] = int((average/valueCount)/10)
            valueCount = 0
            average = 0
        else:
            averageDistance[i - 1] = 0

    return averageDistance

def main():
    speed = 140 # 0 <= speed <= 200, 100 is neutral
    pd = PdHandler()

    #Pid == true => use pid in motormodul, if false, dont use pid.
    pid = True
    lapCount = 0 #Counts the amount of laps we have driven

    averageDistance = [0,0,0,0,0] #holds average distance for all cones


    lidar = memelidar.PyLidar()
    lidar.start_motor()
    lidar.start_scan()

    while 1:
        try:    
            sensorValue = [10,10,10,10,0]
            #sensorValue = sensorTransciver() #List of values, 0-3 is sonar, 4 is round count
            print("angle :", pd.currOutAngle)
            rpm = motorTransceiver([speed, pd.currOutAngle])
            sys.stdout.flush()
            data = np.array(lidar.grab_data())
            averageDistance = calcaverageCones(data)
            for i in range(len(averageDistance)):
                print("cone", i , "distance :", averageDistance[i])

            '''
            print("cone1: ", averageDistance[0], " cone2: ", averageDistance[1], " cone3: ", averageDistance[2],
            " cone4: ", averageDistance[3], " cone5: ", avxerageDistance[4])
            '''

            '''
            if the hitbox is hit or if amount of laps has been completed then
            stop the car and break
            '''

            '''
            if hitbox(sensorValue) or countLaps(sensorValue):
                stop()
                break
            '''

            pd.regulateAngle(sensorValue, averageDistance)

        except KeyboardInterrupt:
            motorTransceiver([NEUTRALSPEED, NEUTRALWHEELANGLE])
            lidar.stop()
            lidar.stop_motor()
            break

        except Exception as e:
            print(e)
            motorTransceiver([NEUTRALSPEED, NEUTRALWHEELANGLE])
            lidar.stop()
            lidar.stop_motor()
            break


if __name__ == '__main__':
    main()
