from pid import *
from speed import *
import memelidar
import numpy as np

GOAL_LAPS = 3 # Amount of laps that the robot should drive

'''
Defines the hitbox derived from the sonar sensors
The values are in the following order:

[sonar1, sonar2, sonar3, sonar4]
'''
HITBOX = [30, 30, 30, 30]

CONES = ((18,342),(90,54),(306,270),(53,19),(341,307))

speed = 100 # 0 <= speed <= 200, 100 is neutral
angle = 90 # 0 <= angle <= 180, 90 is straight

#Pid == true => use pid in motormodul, if false, dont use pid.
pid = True
lapCount = 0 #Counts the amount of laps we have driven

averageDistance = [] #holds average distance for all cones

currVal = 0 #Input, average distance from the walls
pGain = 0.5 #Random value
dGain = 0.1 #Random value
old_dGain = 0 #Used in the pidloop
setVal = 0 #This is the goal.
currOutVal = angle #Output, the angle we want to turn

def calcaverageCones(lidarData):
    average = 0
    valueCount = 0
    for interval in range(CONES.length()):
        #Lidarvalue is a list of tuples
        for data in lidarData:
            #data[0] is the angle of the meassurment, <18 and >342 is +- 18 degrees
            #from angle 0, i.e straight forward. (The cone forward)
            #data[2] > 0 is the quality of the meassurmetn, 0 is bad.
            if(data[1] <= interval[0] and data[1] >= interval[1] and data[3] > 0):
                average += data[2]
                valueCount += 1

        averageDistance.append(average/valueCount)
        valueCount = 0

def main():
    lidar = memelidar.PyLidar()
    lidar.setup_lidar()
    lidar.start_motor()
    lidar.start_scan()

    while 1:
        sensorValue = sensorTransciver() #List of values, 0-3 is sonar, 4 is round count
        rpm = motorTranciever([speed, angle])#syncMotor does not support pid argument yet
        data = np.array(lidar.grabData())
        calcaverageCones(data)
        print("cone1: ", avarageDistance[0], " cone2: ", avarageDistance[1], " cone3: ", avarageDistance[2],
        " cone4: ", avarageDistance[3], " cone5: ", avarageDistance[4], " cone6: ", avarageDistance[5])

        '''
        if the hitbox is hit or if amount of laps has been completed then
        stop the car and break
        '''
        '''
        if hitbox(sensorValue) or countLaps(sensorValue):
            stop()
            break

        regulateSpeed(lidarValue)
        regulateAngle(lidarValue, sensorValue)
        '''
