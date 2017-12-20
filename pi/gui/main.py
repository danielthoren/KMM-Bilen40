#!/usr/bin/python3

'''
Defines functionality of the GUI, uses PyQt4

Participants:
    Alexander Zeijlon
    Gustaf Söderholm
Last changed:
    18/12-2017
'''


from PyQt4 import QtGui, QtCore
import sys
import design2
import threading
from instrHandler import Handler
from threadTCPServer import client
import time
from instructions import *
import cv2
import numpy as np
import pygame
HITBOX = ((40,0),(360,320),(41,75),(319,285))


class ImageWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        super(ImageWidget,self).__init__(parent)
        self.image=None

    def setImage(self,image):
        self.image=image
        sz=image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self,event):
        qp=QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0,0),self.image)
        qp.end()


class ExampleApp(QtGui.QMainWindow, design2.Ui_MainWindow, QtGui.QDialog):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.setupTCP()
        self.W.clicked.connect(lambda: self.forward())
        self.S.clicked.connect(lambda: self.backward())
        self.A.clicked.connect(lambda: self.doer(self.instr._a))
        self.D.clicked.connect(lambda: self.doer(self.instr._d))
        self.stop.clicked.connect(lambda: self.run())
        self.pushButton.clicked.connect(lambda: self.auto_mode())
        self.sendparam.clicked.connect(lambda: self.gettxt())
        self.frame=ImageWidget(self.widget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 1021, 611))
        #self.setCentralWidget(self.frame)
        self.img_size = (self.widget.frameGeometry().height(),self.widget.frameGeometry().width(),3)
        self.img = np.zeros(self.img_size, dtype=np.uint8) +255
        self.offset_x = self.widget.frameGeometry().width()//2
        self.offset_y = self.widget.frameGeometry().height()//2
        self.checkDist = 1400
    
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        self.joystick = self.init_joystick()

    #Update the gui
    def update(self):
        #takes input from joystick
        if pygame.event.get() and self.joystick != None and not self.instr.auto_mode and self.instr.run:
            self.instr.W = (1+self.joystick.get_axis(5))/2
            self.instr.S = (1+self.joystick.get_axis(2))/2
            self.instr.AD = (self.joystick.get_axis(0))
            self.send()

        #Makes new frame for lidar data
        self.img = np.zeros(self.img_size, dtype=np.uint8)

        #Paint car on frame
        cv2.rectangle(self.img, (self.offset_x-3, self.offset_y-20),( self.offset_x+3, self.offset_y+20),(255,255,0),20)
        cv2.rectangle(self.img, ( self.offset_x-20, self.offset_y-18),( self.offset_x-5, self.offset_y-5),(255,255,0),8)
        cv2.rectangle(self.img, ( self.offset_x+5, self.offset_y-18),( self.offset_x+20, self.offset_y-5),(255,255,0),8)
        cv2.rectangle(self.img, ( self.offset_x+5, self.offset_y+7),( self.offset_x+20, self.offset_y+20),(255,255,0),8)
        cv2.rectangle(self.img, ( self.offset_x-20, self.offset_y+7),( self.offset_x-5, self.offset_y+20),(255,255,0),8)

        #Paint lidar data for each value from lidar
        for point in self.handler.send_data.lidar_data:
            self.hitBox(point)

        #Show rpm and lapcount in gui
        self.lcdNumber.display(self.handler.send_data.lap)
        self.lcdNumber_2.display(self.handler.send_data.rpm[0])

        height, width, byteValue = self.img.shape
        byteValue = byteValue * width
        imgg = QtGui.QImage(self.img, width, height, byteValue, QtGui.QImage.Format_RGB888)
        self.frame.setImage(imgg)

    #Checks if points are inside hitbox, then color them green or blue, else paint them red
    def hitBox(self, point):
        if HITBOX[0][1]<=point[1]<=HITBOX[0][0] and point[3] != 0:
            self.paintPoint(point, 1, 1)
        elif HITBOX[1][1]<=point[1]<=HITBOX[1][0] and point[3] != 0:
            self.paintPoint( point, 0, 1)
        elif HITBOX[2][1]<=point[1]<=HITBOX[2][0] and point[3] != 0:
            self.paintPoint(point, 1, 1)
        elif HITBOX[3][1]<=point[1]<=HITBOX[3][0] and point[3] != 0:
            self.paintPoint(point, 0, 1)
        else:
            self.paintPoint(point, 0, 0)

    #Paints a point
    def paintPoint(self, point, lefrig, hitbox):
        x, y = self.polar2cart(point[2]//10, point[1]-90)
        if point[2] < self.checkDist and hitbox == 1 :
            if point[2] < self.checkDist - point[1]*10 and lefrig == 1:
                cv2.circle(self.img,((x+self.offset_x),(y+self.offset_y)), 2, (0,255,0), 2)
            elif point[2] < self.checkDist - (360-point[1])*10 and lefrig == 0:
                cv2.circle(self.img,((x+self.offset_x),(y+self.offset_y)), 2, (0,255,0), 2)
            else:
                cv2.circle(self.img,((x+self.offset_x),(y+self.offset_y)), 2, (0,0,255), 2)
        else:
            cv2.circle(self.img,((x+self.offset_x),(y+self.offset_y)), 2, (255,0,0), 2)
        
    # polar to cartesian
    def polar2cart(self,r, theta):
        temp = np.radians(theta)
        x = r * np.cos(temp)
        y = r * np.sin(temp)
        x = int(x)
        y = int(y)
        return x, y

    #Init the joystick, if any is detected
    def init_joystick(self):
        pygame.init()
        if (pygame.joystick.get_count() != 0):
            my_joystick = pygame.joystick.Joystick(0)
            my_joystick.init()
            return my_joystick
        else:
            return None

    #Register a keyboard press
    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

        elif event.key() == QtCore.Qt.Key_W:
            self.forward()
        elif event.key() == QtCore.Qt.Key_A:
            self.doer(self.instr._a)
        elif event.key() == QtCore.Qt.Key_S:
            self.backward()
        elif event.key() == QtCore.Qt.Key_D:
            self.doer(self.instr._d)
        elif event.key() == QtCore.Qt.Key_R:
            self.reset()
            
    #Register i keyborad release
    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        if event.key() == QtCore.Qt.Key_W:
            self.forward()
        elif event.key() == QtCore.Qt.Key_S:
            self.backward()

        if event.key() == QtCore.Qt.Key_A:
            self.center()

        if event.key() == QtCore.Qt.Key_D:
            self.center()
    
    def setupTCP(self):
        self.instr = Instruction()
        #self.send_data = sendData()
        """
        TCP
        """
        host, port = "192.168.1.10", 10000
        self.handler = Handler(host, port)
        
        self.handler_thread = threading.Thread(target = self.handler.hantera)
        self.handler_thread.daemon = True
        self.handler_thread.start()

    #Sends a message to the car
    def send(self):
        message = self.instr.encode()
        self.handler.add(message)

    #Do the function input and send to car
    def doer(self, func):
        func()
        #instr.printSelf()
        self.send()

    #Trigged by "W" press, sends command
    def forward(self):
        #self.S.setChecked(False)
        self.instr._w()
        #instr.printSelf()
        self.send()

    #Trigged by "A" or "D" press, sends command
    def center(self):
        self.instr.AD = 0
        self.send()

    #Trigged by "S" press, sends command
    def backward(self):
        #self.W.setChecked(False)
        self.instr._s()
        #instr.printSelf()
        self.send()

    def reset(self):
        self.instr.reset_wasd()
        # self.S.setChecked(False)
        # self.W.setChecked(False)
        #instr.printSelf()
        self.send()

    #Change run mode to true or false, and send 
    def run(self):
        self.instr._run(self.stop)
        self.send()
    
    #Get pGain or dGain value and send to car
    def gettxt(self):
        self.instr.set_p(self.pid_p.text())
        self.instr.set_d(self.pid_d.text())
        self.send()
    
    
    def show_data(self):
        with self.handler.qLock:
            self.send_data.decode(self.handler.response)

    #Change auto mode to true or false, and send
    def auto_mode(self):
        self.instr._auto_mode(self.label_5)
        self.send()

    #Read rpm from recieved data
    def get_rpm(self):
        return self.handler.send_data.rpm



def main():
    app = QtGui.QApplication(sys.argv)    
    form = ExampleApp()
    
    
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
