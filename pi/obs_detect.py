from lidar import memelidar
import numpy as np
#import cv2
import time

#Defines between wich degrees each cone is. Two first cones are handles as special
#case since they represent one cone in actuality
CONES = ((90,54),(306,270),(53,19),(341,307))
HITBOX = ((10,0),(360,350),(20,10),(350,340))
minLineLength = 100
maxLineGap = 10

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


def obsDetect(data):
    probileft = 0
    probiright = 0
    critprobiright = 0
    critprobileft = 0
    setVal = 0
    for point in data:   
        #probileft, probiright = obdetect(point,img,probileft, probiright)
        if HITBOX[0][1]<point[1]<HITBOX[0][0] and point[3] != 0:
            if point[2] < 1000:
                #x5, y5 = polar2cart(point[2], point[1]-90)
                #cv2.circle(img,((x5+offset),(y5+offset)), 2, (23,200,20), 80)
                critprobiright += 1
        elif HITBOX[1][1]<point[1]<HITBOX[1][0] and point[3] != 0:
            if point[2] < 1000:
                #x5, y5 = polar2cart(point[2], point[1]-90)
                #cv2.circle(img,((x5+offset),(y5+offset)), 2, (23,200,20), 80)
                critprobileft += 1
        elif HITBOX[2][1]<point[1]<HITBOX[2][0] and point[3] != 0:
            if point[2] < 1000:
                x5, y5 = polar2cart(point[2], point[1]-90)
                #cv2.circle(img,((x5+offset),(y5+offset)), 2, (23,200,255), 80)
                probiright += 1
        elif HITBOX[3][1]<point[1]<HITBOX[3][0] and point[3] != 0:
            if point[2] < 1000:
                #x5, y5 = polar2cart(point[2], point[1]-90)
                #cv2.circle(img,((x5+offset),(y5+offset)), 2, (23,200,255), 80)
                probileft += 1
        
        x, y = polar2cart(point[2], point[1]-90)
        #cv2.circle(img,((x+offset),(y+offset)), 2, (0,0,255), 50)
    if critprobileft > 5:
        print("Critical hinder left ", critprobileft)
        setVal += 80
    if critprobiright > 5:
        print("critical hinder right ", critprobiright)
        setVal += -80
    if probileft > 5:
        print("Hinder left ", probileft)
        setVal += 50
    if probiright > 5:
        print("Hinder right ", probiright)
        setVal += -50
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
        
