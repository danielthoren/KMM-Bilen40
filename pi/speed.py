from main import *

#Stops the car
def stop():
    speed = 100
    pid = False
    motorTranciever([speed, angle])

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
        if sensorValue[i] <= HITBOX[i]:
            return True

#Regulates the speed depending on average value from lidar and the sonar values
def regualteSpeed(lidarValue):

    averageForwardDistance = averageDistance[0]
    #Free road ahed
    if(averageForwardDistance > 6000):
        speed = 200 #Full speed
        motorTranciever([speed, angle])
    #Free road ahead, but not for long
    elif averageForwardDistance > 3000:
        speed = 150
        motorTranciever([speed, angle])
    #To close to a obsticle
    elif averageForwardDistance < 300:
        stop()
    #If we are at distance 1000 mm from an obsticle, drive slowley
    elif averageForwardDistance < 1000:
        speed = 110
        motorTranciever([speed, angle])
    #Keep constant speed inbetween 1000 and 3000
    else:
        speed = 120
        motorTranciever([speed, angle])

def speed(averageDistance, wheelAngle):
    if averageDistance[0] > TURNTHRESHOLD:
        speed =  MAXSPEED - abs((NEUTRALWHEELANGLE - wheelAngle))
    else:
        speed = (MAXSPEED) - abs((NEUTRALWHEELANGLE - wheelAngle))
