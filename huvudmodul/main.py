speed = 0 # 0 <= speed <= 200
angle = 0 # 0 <= angle <= 180
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
    speed = 3
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
    anvrageDistance = 0

    #Lidarvalue is a list of tuples
    for data in lidarValue:
        #data[0] is the angle of the meassurment, <18 and >342 is +- 18 degrees
        #from angle 0, i.e straight forward. (The cone forward)
        #data[2] > 0 is the quality of the meassurmetn, 0 is bad.
        if(data[0] <= 18 and data[0] >= 342 and data[2] > 0):
            anvrageDistance += data[1]
            count += 1

    anvrageDistance = anvrageDistance/count
    #Free road ahed
    if(anvrageDistance > 6000):
        speed = 200 #Full speed
    #Free road ahead, but not for long
    elif anvrageDistance > 3000:
        speed = 150
    #To close to a obsticle
    elif anvrageDistance < 300:
        stop()
    #If we are at distance 1000 mm from an obsticle, drive slowley
    elif anvrageDistance < 1000:
        speed = 60
    #Keep constant speed inbetween 1000 and 3000
    else:
        speed = 100

def regulateAngle(lidarValue, sensorValue):



def main():
    while 1:
        sensorValue = syncSonar() #List of values, 0-3 is sonar, 4 is round count
        rpm = syncMotor(speed, angle, pid) #Int
        lidarValue = syncLidar() #List of tuples

        if hitbox(sensorValue) or countRounds(sensorValue):
            break

        regulateSpeed(lidarValue)
        regulateAngle(lidarValue, sensorValue)
