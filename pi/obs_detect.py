from lidar import memelidar
from enum import Enum
#Defines between wich degrees each cone is. Two first cones are handles as special
#case since they represent one cone in actuality
CONES = ((90,54),(306,270),(53,19),(341,307))
#HITBOX = ((15,0),(360,345),(40,16),(344,320))
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
        self.checkDist = 1400

    def calcHitboxes(self, data):
        self.probileft = 0
        self.probiright = 0
        self.critprobiright = 0
        self.critprobileft = 0
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
                if point[2] < 700:
                    self.probileft += 1

            if HITBOX[3][1]<=point[1]<=HITBOX[3][0] and point[3] != 0:
                if point[2] < 700:
                    self.probiright += 1


                    
                
    def calcSetVal(self):
        self.l_setVal = -(self.probileft*5 + self.critprobileft*20)
        self.r_setVal = self.probiright*5 + self.critprobiright*20
        #self.setVal = 0
        '''
        if self.l_setVal == -(self.r_setVal) and self.l_setVal > 0:
            self.setVal = self.l_setVal
        elif self.setVal == 0:
            self.setVal = self.l_setVal + self.r_setVal

        
        if self.critprobiright > 10 and self.critprobileft > 10:
            if self.probileft > self.probiright:
                self.setVal = -100
            else:
                self.setVal = 100
        
        '''

        self.setVal = self.l_setVal + self.r_setVal
        #print('l_setval:', self.l_setVal, '\tr_setval:', self.r_setVal)
        #print(self.obsBool)
    
        
    def obsDetect(self,data):
        self.calcHitboxes(data)
        self.calcSetVal()

        if self.setVal > 150:
            self.setVal = 150
        if self.setVal < -150:
            self.setval = -150
        print('Setval: ', self.setVal)

        return self.setVal
