from main import NEUTRALWHEELANGLE

import os

class PdHandler:
    def __init__(self):
        self.pGain = 0.05 #Random value
        self.dGain = 0 #Random value
        self._setVal = 0 #This is the goal.

        self.currOutAngle = NEUTRALWHEELANGLE #Output, the angle we want to turn
        self._dGainOld = 0 #Used in the pidloop


    #Regulates the angle of the tires with the help of the pidLoop in pid.py
    #Uses the cones to the far right and left
    def regulateAngle(self, sensorValue, averageDistance):
        tmpAngle = int(self._pidLoop(averageDistance[2] - averageDistance[1]))
        os.system('clear')
        
        print("tmpAngle :", tmpAngle)

        #Incase the pidloop wnats to turn to much, in this case, lower the speed
        if tmpAngle > 180:
            tmpAngle = 180
        elif tmpAngle < 0:
            tmpAngle = 0

        self.currOutAngle = tmpAngle
        

    def _pidLoop(self, currVal):
        pTerm = 0
        dTerm = 0

        errorVal = self._setVal - currVal

        pTerm = self.pGain * errorVal
        dTerm = self.dGain * (self._dGainOld - errorVal)
        self._dGainOld = dTerm

        return self.currOutAngle - (pTerm + dTerm)
