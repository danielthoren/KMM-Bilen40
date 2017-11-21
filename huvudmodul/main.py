from pid import *

speed = 100 # 0 <= speed <= 200, 100 is neutral
angle = 90 # 0 <= angle <= 180, 90 is straight
#Pid == true => use pid in motormodul, if false, dont use pid.
pid = True
roundCount = 0 #Counts the amount of rounds we have driven


#Returns a list of values, 0-3 is sonar, 4 i round count
def syncSonar():
    return sensorTransciver()

#Returns a list of tuples
def syncLidar():

#Returns a int, sends two ints
def syncMotor(speed, angle, pid):
    data = [speed,angle, pid]
    pid = True #Sets prop back to True in case it has been changed
    return motorTransciver(data)

#Stops the car
def stop():
    speed = 100
    pid = False
    syncMotor(speed, angle, pid)

#Counts the rounds
def countRounds(sensorValue):
        if(sensorValue[4]):
            roundCount += 1
        #Stops after three rounds
        if roundCount == 3:
            stop()
            return True

#Checks hitbox
def hitbox(sensorValue):
    #If the sensors say we are verry close to an obsticle we stop
    for data in sensorValue[:-1]:
        if data < 30:
            stop()
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
        pid.currVal = avrageDistanceRight - avrageDistanceLeft

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
    pid.currVal = avrageDistanceUpperRight - avrageDistanceUpperLeft

    anglePid()

#Calls the pidLoop to change the angle
def anglePid():
    pid.pidLoop()

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

    pid.currOutVal = angle

def main():
    while 1:
        sensorValue = syncSonar() #List of values, 0-3 is sonar, 4 is round count
        rpm = syncMotor(speed, angle, pid) #Int
        lidarValue = syncLidar() #List of tuples

        if hitbox(sensorValue) or countRounds(sensorValue):
            break

        regulateSpeed(lidarValue)
        regulateAngle(lidarValue, sensorValue)
