from main import *

#Regulates the angle of the tires with the help of the pidLoop in pid.py
#Uses the cones to the far right and left
def regulateAngle(lidarValue, sensorValue):

        averageDistanceLeft = averageDistance[1]
        averageDistanceRight = averageDistance[2]

        #Positive value means we are more to the right, negative value
        #means we are more to the left.
        currVal = averageDistanceRight - averageDistanceLeft

        anglePid()

        secondRegulateAngle()

#regulates the angle with the upper left and right cones.
def secondRegulateAngle():

    averageDistanceUpperLeft = averageDistance[3]
    averageDistanceUpperRight = averageDistance[4]

    #Positive value means we are more to the right, negative value
    #means we are more to the left.
    currVal = averageDistanceUpperRight - averageDistanceUpperLeft

    anglePid()

#Calls the pidLoop to change the angle
def anglePid():
    pidLoop()

    #Incase the pidloop wnats to turn to much, in this case, lower the speed
    if angle > 180:
        angle = 180
        speed = 110 #Slow

    elif angle < 0:
        angle = 0
        speed = 110 #Slow

    #Speed should be less when we turn more, find some good scale to caclulate
    #The speed depending on the angle (Maybee)

    syncMotor(speed, angle, pid)

    currOutVal = angle

def pidLoop():
    pTerm = 0
    dTerm = 0

    errorVal = setVal - currVal

    pTerm = pGain * errorVal
    dTerm = dGain * (old_dGain - errorVal)
    old_dGain = dTerm

    angle = currOutVal - (pTerm + dTerm)
