from main import *
GOAL_LAPS = 3 # Amount of laps that the robot should drive


#Counts the rounds
def countLaps(sensorValue, lapCount):
        
        if(sensorValue[4] == 1):
            lapCount += 1
            print(lapCount)
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
    if(averageForwardDistance > 180 and rightVal > 100 and leftVal > 100):
        return 140 #Full speed
 
    if (50 < averageForwardDistance <= 180 and rightVal > 100 and leftVal > 100):
        return 120
    #To close to a obsticle
    if averageForwardDistance <= 50:
         return 100 #stops car
    #Free road ahead, but not for long
    if 50 < averageForwardDistance <= 180 or rightVal <= 100 or leftVal <= 100:
        return 120
    else:
        print("in else")
