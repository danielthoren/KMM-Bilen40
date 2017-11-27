from main import NEUTRALWHEELANGLE

import os
import time

class PdHandler:
    def __init__(self):
        self.pGain = 0.05 #Random value
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
        tmpAngle = int(self._pidLoop(averageDistance[2] - averageDistance[1]), time.time() - _time)
        os.system('clear')
        
        print("tmpAngle :", tmpAngle)

        #Incase the pidloop wnats to turn to much, in this case, lower the speed
        if tmpAngle > 180:
            tmpAngle = 180
        elif tmpAngle < 0:
            tmpAngle = 0

        self.currOutAngle = tmpAngle
        _time = time.time()
        
        

    def _pidLoop(self, currVal, timeSince):
        pTerm = 0
        dTerm = 0
        iTerm = 0

        errorVal = self._setVal - currVal

        pTerm = self.pGain * errorVal
        dTerm = self.dGain * (errorVal - self._dGainOld) / timeSince
        self._iAccumulated += errorVal * timeSince
        iTerm = self._iAccumulated * iGain
        
        self._dGainOld = dTerm

        return self.currOutAngle - (pTerm + dTerm + iTerm)
