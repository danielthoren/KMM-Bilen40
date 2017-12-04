from lidar import memelidar
import numpy as np
#import cv2
import time
from enum import Enum
#Defines between wich degrees each cone is. Two first cones are handles as special
#case since they represent one cone in actuality
CONES = ((90,54),(306,270),(53,19),(341,307))
HITBOX = ((10,0),(360,350),(20,10),(350,340))
minLineLength = 100
maxLineGap = 10
state = obs.noObs
obsBool = false

class obs(Enum):
    noObs = 0
    obsRig = 1
    obsLef = 2
    obsStr = 3
        
        

img_size = (5000,5000,3)
offset = 2500
        
# polar to cartesian
def polar2cart(r, theta):
    temp = np.radians(theta)
    x = r * np.cos(temp)
    y = r * np.sin(temp)
    x = int(x)
    y = int(y)
    return x, y


def obsDetect(data, averageDistance):
    probileft = 0
    probiright = 0
    critprobiright = 0
    critprobileft = 0
    stra = 0
    setVal = 0
    checkDis = 1000
    obsBool = false
    for point in data:   
        #probileft, probiright = obdetect(point,img,probileft, probiright)
        if HITBOX[0][1]<point[1]<HITBOX[0][0] and point[3] != 0:
            if point[2] < checkDis:
                #x5, y5 = polar2cart(point[2], point[1]-90)
                #cv2.circle(img,((x5+offset),(y5+offset)), 2, (23,200,20), 80)
                critprobiright += 1
                stra += 1
        elif HITBOX[1][1]<point[1]<HITBOX[1][0] and point[3] != 0:
            if point[2] < checkDis:
                #x5, y5 = polar2cart(point[2], point[1]-90)
                #cv2.circle(img,((x5+offset),(y5+offset)), 2, (23,200,20), 80)
                critprobileft += 1
                stra += 1
        elif HITBOX[2][1]<point[1]<HITBOX[2][0] and point[3] != 0:
            if point[2] < checkDis:
                x5, y5 = polar2cart(point[2], point[1]-90)
                #cv2.circle(img,((x5+offset),(y5+offset)), 2, (23,200,255), 80)
                probiright += 1
        elif HITBOX[3][1]<point[1]<HITBOX[3][0] and point[3] != 0:
            if point[2] < checkDis:
                #x5, y5 = polar2cart(point[2], point[1]-90)
                #cv2.circle(img,((x5+offset),(y5+offset)), 2, (23,200,255), 80)
                probileft += 1
        
        x, y = polar2cart(point[2], point[1]-90)
        #cv2.circle(img,((x+offset),(y+offset)), 2, (0,0,255), 50


    if state == noObs:
        if critprobileft > 5 and critprobiright > 5 and stra > 12:
            if critprobileft > critprobiright:
                print("Hinder forward, going left")
                setVal += 100
                state = obs.obsStr
                checkDist = 400
            else:
                print("Hinder forward, going right")
                setVal -= 100
                state = obs.obsStr
                checkDist = 400
            obsBool = True
        else:
            
            if critprobileft > 3:
                print("Critical hinder left ", critprobileft)
                setVal += 80
                state = obs.criObsLef
                checkDist = 600
            if critprobiright > 3:
                print("critical hinder right ", critprobiright)
                setVal += -80
                state = obs.criObsRig
                checkDist = 600
            if probileft > 3:
                print("Hinder left ", probileft)
                setVal += 50
                state = obs.obsLef
                checkDist = 600
            if probiright > 3:
                print("Hinder right ", probiright)
                setVal += -50
                state = obs.obsRig
                checkDist = 600
    elif state == obs.obsLef or state == obs.obsRig:
        if critprobileft > 8 and critprobiright > 8 and stra > 12:
            if critprobileft > critprobiright:
                print("Hinder forward, going left")
                setVal += 100
                state = obs.obsStr
                checkDist = 400
            else:
                print("Hinder forward, going right")
                setVal -= 100
                state = obs.obsStr
                checkDist = 400
        else:
            if critprobileft > 5:
                print("Critical hinder left ", critprobileft)
                setVal += 80
                state = obs.criObsLef
                checkDist = 600
            if critprobiright > 5:
                print("critical hinder right ", critprobiright)
                setVal += -80
                state = obs.criObsRig
                checkDist = 600
            if probileft > 5:
                print("Hinder left ", probileft)
                setVal += 50
                state = obs.obsLef
                checkDist = 600
            if probiright > 5:
                print("Hinder right ", probiright)
                setVal += -50
                state = obs.obsRig
                checkDist = 600
    elif state == obs.obsStr:
        if critprobileft > 8 and critprobiright > 8 and stra > 12:
            if critprobileft > critprobiright:
                print("Hinder forward, going left")
                setVal += 100
                state = obs.obsStr
                checkDist = 400
            else:
                print("Hinder forward, going right")
                setVal -= 100
                state = obs.obsStr
                checkDist = 400
        else:
            if critprobileft > 5:
                print("Critical hinder left ", critprobileft)
                setVal += 80
                state = obs.criObsLef
                checkDist = 600
            if critprobiright > 5:
                print("critical hinder right ", critprobiright)
                setVal += -80
                state = obs.criObsRig
                checkDist = 600
            if probileft > 5:
                print("Hinder left ", probileft)
                setVal += 50
                state = obs.obsLef
                checkDist = 600
            if probiright > 5:
                print("Hinder right ", probiright)
                setVal += -50
                state = obs.obsRig
                checkDist = 600
        
        
    
        
    if setVal > 100:
        setVal = 100
    if setVal < -100:
        setval = -100
    return setVal


def main():
    
    lidar = memelidar.PyLidar()
    lidar.start_motor()
    lidar.start_scan()

    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 600,600)
    
    while 1:
        try:
            img = np.zeros(img_size, dtype=np.uint8) +255
            sensorValue = [10,10,10,10,0]
            data = np.array(lidar.grab_data())
            obDetect(data,img)
            cv2.imshow('image',img)
            cv2.waitKey(1)
            
        except KeyboardInterrupt:
            lidar.stop()
            lidar.stop_motor()
            break

        except Exception as e:
            print(e)
            lidar.stop()
            lidar.stop_motor()
            break
        
