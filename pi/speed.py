from main import *

#Stops the car
def stop():
    speed = 100
    pid = False
    syncMotor(speed, angle, pid)

#Counts the rounds
def countLaps(sensorValue):
        if(sensorValue[4]):
            lapCount += 1
        #returns true when roundCount equals GOAL_LAPS
        if lapCount == GOAL_LAPS:
            return True

#Checks hitbox
def hitbox(sensorValue):
    #If the sensors say we are verry close to an obsticle we stop
    for i in range(sensorValue.lenth - 1):
        if sensorValue[i] < HITBOX[i]:
            return True

#Regulates the speed depending on avrage value from lidar and the sonar values
def regualteSpeed(lidarValue):
    #Variables used in the loop down below
    count = 0
    avrageDistance = 0

    #Lidarvalue is a list of tuples
    for data in lidarValue:
        #data[0] is the angle of the meassurment, <18 and >342 is +- 18 degrees
        #from angle 0, i.e straight forward. (The cone forward)
        #data[2] > 0 is the quality of the meassurmetn, 0 is bad.
        if(data[0] <= 18 and data[0] >= 342 and data[2] > 0):
            avrageDistance += data[1]
            count += 1

    avrageDistance = anvrageDistance/count
    #Free road ahed
    if(avrageDistance > 6000):
        speed = 200 #Full speed
        syncMotor(speed, angle, pid)
    #Free road ahead, but not for long
    elif avrageDistance > 3000:
        speed = 150
        syncMotor(speed, angle, pid)
    #To close to a obsticle
    elif avrageDistance < 300:
        stop()
    #If we are at distance 1000 mm from an obsticle, drive slowley
    elif avrageDistance < 1000:
        speed = 110
        syncMotor(speed, angle, pid)
    #Keep constant speed inbetween 1000 and 3000
    else:
        speed = 120
        syncMotor(speed, angle, pid)
