from lidar import memelidar
import numpy as np
#import cv2
import time
from enum import Enum
#Defines between wich degrees each cone is. Two first cones are handles as special
#case since they represent one cone in actuality
CONES = ((90,54),(306,270),(53,19),(341,307))
#HITBOX = ((15,0),(360,345),(40,16),(344,320))
HITBOX = ((40,0),(360,320))

class obs(Enum):
    noObs = 0
    obsRig = 1
    obsLef = 2
    obsStr = 3

class obsFunc():
    def __init__(self):
        self.probileft = 0
        self.probiright = 0
        self.critprobiright = 0
        self.critprobileft = 0
        self.r_setVal = 0
        self.l_setVal = 0
        self.setVal = 0
        self.obsBool = False
        self.checkDist = 1100
        self.state = obs.noObs

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

                
            '''
            #probileft, probiright = obdetect(point,img,probileft, probiright)
            if HITBOX[0][1]<=point[1]<=HITBOX[0][0] and point[3] != 0:
                if point[2] < self.checkDist - (point[1]*10):
                    self.critprobiright += 1
            if HITBOX[1][1]<=point[1]<=HITBOX[1][0] and point[3] != 0:
                if point[2] < self.checkDist - (360 - point[1])*10: 
                    self.critprobileft += 1
            if HITBOX[2][1]<=point[1]<=HITBOX[2][0] and point[3] != 0:
                if point[2] < self.checkDist:
                    if point[2] < 800:
                        self.critprobileft += 1
                    self.probiright += 1
            if HITBOX[3][1]<=point[1]<=HITBOX[3][0] and point[3] != 0:
                if point[2] < self.checkDist:
                    if point[2] < 800:
                        self.critprobileft += 1
                    self.probileft += 1
            '''
    def calcSetVal(self):
        self.obsBool = False
        probicount = 2
        self.l_setVal = -(self.probileft*5 + self.critprobileft*20)
        self.r_setVal = self.probiright*5 + self.critprobiright*20
        self.setVal = 0

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
        if True:
            if self.critprobileft > probicount:
                print("Critical hinder")
                #if self.probileft >= self.probiright:
                self.l_setVal += 100
                self.state = obs.obsLef
                self.obsBool = True
                #else:
                #self.setVal += +80
                 #   self.state = obs.obsRig
            if self.critprobiright > probicount:
                print("Critical hinder")
                #if self.probileft >= self.probiright:
                self.r_setVal -= 100
                self.state = obs.obsRig
                self.obsBool = True

            if self.probileft > probicount:
                print("Hinder left ", self.probileft)
                self.l_setVal += 50
                self.obsBool = True
            if self.probiright > probicount:
                print("Hinder right ", self.probiright)
                self.r_setVal -= 50
                self.obsBool = True
        elif self.state == obs.obsLef:
            if self.critprobiright > probicount or self.critprobileft > probicount:
                self.obsBool = True
            else:
                self.obsBool = False
        elif self.state == obs.obsRig:
            if self.critprobileft > probicount or self.critprobiright > probicount:
                self.obsBool = True
            else:
                self.obsBool = False
        '''
        print('l_setval:', self.l_setVal, '\tr_setval:', self.r_setVal)
        print(self.obsBool)
        
        
    def obsDetect(self,data):
        self.calcHitboxes(data)
        self.calcSetVal()
        '''
        if not self.obsBool:
            self.state = obs.noObs
            self.checkDist = 1000
            self.setVal = 0
        '''
        if self.setVal > 150:
            self.setVal = 150
        elif self.setVal < -150:
            self.setval = -150
        print('Setval: ', self.setVal)

        return self.setVal
