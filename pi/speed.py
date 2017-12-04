from main import *

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
def regulateSpeed(averageForwardDistance, rightVal, leftVal):

    #Free road ahed
    if(averageForwardDistance > 160 and rightVal > 80 and leftVal > 80):
        return 160 #Full speed
 
    if (50 < averageForwardDistance <= 160 and rightVal > 80 and leftVal > 80):
        return 120
    #To close to a obsticle
    if averageForwardDistance <= 50:
         return 100 #stops car
    #Free road ahead, but not for long
    if 50 < averageForwardDistance <= 160 or rightVal <= 80 or leftVal <= 80:
        return 120
    else:
        print("in else")
