from main import NEUTRALWHEELANGLE

import numpy as np
import matplotlib.pyplot as plt

import os
import time

PLOT = True

if PLOT:
    plt.axis([0, 5000, -200, 200])
    plt.ion()

class PdHandler:
    def __init__(self):
        self.pGain = 1.5 #Random value
        self.dGain = 0 #Random value
        self.iGain = 0
        self._iAccumulated = 0
        self._setVal = 0 #This is the goal.
        self._time = time.time()

        self.currOutAngle = NEUTRALWHEELANGLE #Output, the angle we want to turn
        self._dGainOld = 0 #Used in the pidloop


    #Regulates the angle of the tires with the help of the pidLoop in pid.py
    #Uses the cones to the far right and left
    def regulateAngle(self, sensorValue, averageDistance):

        distanceVal = ((averageDistance[2] - averageDistance[1]) + (averageDistance[4] - averageDistance[3]))/2
        
        if distanceVal > 200:
            distanceVal = 200
        elif distanceVal < -200:
            distanceVal = -200
            
        tmpAngle = int(self._pidLoop(distanceVal, time.time() - self._time))
        
        #os.system('clear')

        #print("tmpAngle :", tmpAngle)

        #Incase the pidloop wnats to turn to much, in this case, lower the speed
        if tmpAngle > 180:
            tmpAngle = 180
        elif tmpAngle < 0:
            tmpAngle = 0

        if PLOT:
            plt.plot(distanceVal, 'bo', marksize=1)
            plt.plot(tmpAngle, 'ro', markersize=1)
            plt.pause(0.00000000000000000001)

        self.currOutAngle = tmpAngle
        self._time = time.time()

    def _pidLoop(self, currVal, timeSince):
        pTerm = 0
        dTerm = 0
        iTerm = 0

        os.system('clear')
        errorVal = self._setVal - currVal

        print("currval: ", currVal)

        pTerm = self.pGain * errorVal
        dTerm = self.dGain * (errorVal - self._dGainOld) / timeSince
        self._iAccumulated += errorVal * timeSince
        iTerm = self._iAccumulated * self.iGain
        
        self._dGainOld = dTerm

        return self.currOutAngle - (pTerm + dTerm + iTerm)
