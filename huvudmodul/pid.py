from main import *

#Regulates the angle of the tires with the help of the pidLoop in pid.py
#Uses the cones to the far right and left
def regulateAngle(lidarValue, sensorValue):
        #Variables used in the loop down below
        count = 0
        avrageDistanceLeft = 0
        avrageDistanceRight = 0

        #Lidarvalue is a list of tuples
        for data in lidarValue:
            #data[0] is the angle of the meassurment, <90 and >54 is the
            #cone to the far left.
            #data[2] > 0 is the quality of the meassurmetn, 0 is bad.
            if(data[0] <= 90 and data[0] >= 54 and data[2] > 0):
                avrageDistanceLeft += data[1]
                count += 1

        avrageDistanceLeft = avrageDistanceLeft / count
        count = 0

        for data in lidarValue:
            #data[0] is the angle of the meassurment, <306 and >270 is the
            #cone to the far right.
            #data[2] > 0 is the quality of the meassurmetn, 0 is bad.
            if(data[0] <= 306 and data[0] >= 270 and data[2] > 0):
                avrageDistanceRight += data[1]
                count += 1

        avrageDistanceRight = avrageDistanceRight / count

        #Positive value means we are more to the right, negative value
        #means we are more to the left.
        currVal = avrageDistanceRight - avrageDistanceLeft

        anglePid()

        secondRegulateAngle()

#regulates the angle with the upper left and right cones.
def secondRegulateAngle():
    #Variables used in the loop down below
    count = 0
    avrageDistanceUpperLeft = 0
    avrageDistanceUpperRight = 0

    #Lidarvalue is a list of tuples
    for data in lidarValue:
        #data[0] is the angle of the meassurment, <54 and >18 is the
        #cone to the upper left.
        #data[2] > 0 is the quality of the meassurmetn, 0 is bad.
        if(data[0] < 54 and data[0] > 18 and data[2] > 0):
            avrageDistanceUpperLeft += data[1]
            count += 1

    avrageDistanceUpperLeft = avrageDistanceUpperLeft / count
    count = 0

    for data in lidarValue:
        #data[0] is the angle of the meassurment, <342 and >306 is the
        #cone to the upper right.
        #data[2] > 0 is the quality of the meassurmetn, 0 is bad.
        if(data[0] < 342 and data[0] > 306 and data[2] > 0):
            avrageDistanceUpperRight += data[1]
            count += 1

    avrageDistanceUpperRight = avrageDistanceUpperRight / count

    #Positive value means we are more to the right, negative value
    #means we are more to the left.
    currVal = avrageDistanceUpperRight - avrageDistanceUpperLeft

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

def pidLoop(self):
    pTerm = 0
    dTerm = 0

    errorVal = setVal - currVal

    pTerm = pGain * errorVal
    dTerm = dGain * (old_dGain - errorVal)
    old_dGain = dTerm

    angle = currOutVal - (pTerm + dTerm)
