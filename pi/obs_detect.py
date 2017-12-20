'''
This file is for finding and avoiding obstacles.
Participants:
    Gustaf Soderholm
    Alexander Zeijlon
    Kristian Sikiric
    Daniel Thoren
    Gustav Svennas
    Martin Lindkvist
Last changed:
    20/12-2017
'''
from lidar import memelidar

#Defines between wich degrees each cone is. 
HITBOX = ((40,0),(360,320),(41,75),(319,285))


class obsFunc():
    def __init__(self):
        self.probileft = 0
        self.probiright = 0
        self.critprobiright = 0
        self.critprobileft = 0
        self.r_setVal = 0
        self.l_setVal = 0
        self.setVal = 0
        self.checkDist = 1350
        self._pGainSetVal = 0.1 #Random value
        self.target = 0
        self.setValOut = 0
    '''
    Takes in lidar data and adds point to variabels if someting is inside the hitbox. 
    '''
    def calcHitboxes(self, data):
        self.probileft = 0
        self.probiright = 0
        self.critprobiright = 0
        self.critprobileft = 0
        #For each value from lidar, check if it is in the hitbox and check if it is close ( < checkDist)
        for point in data:
            
            if HITBOX[0][1]<=point[1]<=HITBOX[0][0] and point[3] != 0:
                if point[2] < self.checkDist:
                    if point[2] < self.checkDist - point[1]*10:
                        self.critprobileft += 1
                    self.probileft += 1
            if HITBOX[1][1]<=point[1]<=HITBOX[1][0] and point[3] != 0:
                if point[2] < self.checkDist:
                    if point[2] < self.checkDist - (360-point[1])*10:
                        self.critprobiright += 1
                    self.probiright += 1
            if HITBOX[2][1]<=point[1]<=HITBOX[2][0] and point[3] != 0:
                if point[2] < 800:
                    self.probileft += 1

            if HITBOX[3][1]<=point[1]<=HITBOX[3][0] and point[3] != 0:
                if point[2] < 800:
                    self.probiright += 1


                    
    '''
    Sets a setval by checking how many points in the hitbox
    '''
    def calcSetVal(self):
        self.l_setVal = -(self.probileft*5 + self.critprobileft*20)
        self.r_setVal = self.probiright*5 + self.critprobiright*20
    
        self.setVal = self.l_setVal + self.r_setVal
    
        self.setValOut = self._pLoop(self.setVal)
    
    '''
    Uses old setval and pGainSetVal to make the transition between setval more smooth 
    '''
    def _pLoop(self, currVal):
        pTerm = 0
        errorVal = self.target - currVal
        pTerm = self._pGainSetVal * errorVal
        self.target = self.setVal
        return self.target + pTerm

    
    '''
    Sends a setval depending on if there is any obstacles in the way.
    '''
    def obsDetect(self,data):
        self.calcHitboxes(data)
        self.calcSetVal()
        
        return self.setValOut
