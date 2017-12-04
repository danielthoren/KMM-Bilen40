from main import NEUTRALWHEELANGLE

import numpy as np
import matplotlib.pyplot as plt

import os
import time

class PdHandler:
    def __init__(self):
        self._timeSinceStart = time.time()
        self.pGain = 0.6 #Random value
        self.dGain = 0.15 #Random value
        self.iGain = 0.00
        self._iAccumulated = 0
        self.setVal = 0 #This is the goal.
        self._time = time.time()

        self.currOutAngle = NEUTRALWHEELANGLE #Output, the angle we want to turn
        self._preError = 0 #Used in the pidloop

    #Regulates the angle of the tires with the help of the pidLoop in pid.py
    #Uses the cones to the far right and left
    def regulateAngle(self, sensorValue, averageDistance):

        distanceVal = ((averageDistance[2] - averageDistance[1]) +
                       (averageDistance[4] - averageDistance[3]))/2
        
        if distanceVal > 200:
            distanceVal = 200
        elif distanceVal < -200:
            distanceVal = -200
            
        tmpAngle = int(self._pidLoop(distanceVal, time.time() - self._time))
        
#        os.system('clear')

#        print("tmpAngle :", tmpAngle, "currVal:", distanceVal)

        #Incase the pidloop wnats to turn to much, in this case, lower the speed
        if tmpAngle > 140:
            tmpAngle = 140
        elif tmpAngle < 20:
            tmpAngle = 20

        self.currOutAngle = tmpAngle
        self._time = time.time()

    def _pidLoop(self, currVal, timeSince):
        pTerm = 0
        dTerm = 0
        iTerm = 0

        
        errorVal = self.setVal - currVal
        print('setVal: ', self.setVal)
        pTerm = self.pGain * errorVal
        dTerm = self.dGain * ((errorVal - self._preError) / timeSince)
        self._iAccumulated += errorVal * timeSince
        iTerm = self._iAccumulated * self.iGain
        
        self._preError = errorVal

        return NEUTRALWHEELANGLE - (pTerm + dTerm + iTerm)
