from pid import *
from speed import *

speed = 100 # 0 <= speed <= 200, 100 is neutral
angle = 90 # 0 <= angle <= 180, 90 is straight
#Pid == true => use pid in motormodul, if false, dont use pid.
pid = True
roundCount = 0 #Counts the amount of rounds we have driven

currVal = 0 #Input, avrage distance from the walls
pGain = 0.5 #Random value
dGain = 0.1 #Random value
old_dGain = 0 #Used in the pidloop
setVal = 0 #This is the goal.
currOutVal = angle #Output, the angle we want to turn

#Returns a list of values, 0-3 is sonar, 4 i round count
def syncSonar():
    return sensorTransciver()

#Returns a list of tuples
def syncLidar():
    return
#Returns a int, sends two ints
def syncMotor(speed, angle, pid):
    data = [speed,angle, pid]
    pid = True #Sets prop back to True in case it has been changed
    return motorTransciver(data)

def main():
    while 1:
        sensorValue = syncSonar() #List of values, 0-3 is sonar, 4 is round count
        rpm = syncMotor(speed, angle, pid) #Int
        lidarValue = syncLidar() #List of tuples

        if hitbox(sensorValue) or countRounds(sensorValue):
            break

        regulateSpeed(lidarValue)
        regulateAngle(lidarValue, sensorValue)
