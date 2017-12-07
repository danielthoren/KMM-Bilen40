#!/usr/bin/python3
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
        #self.cvImage = cv2.imread(r'cat.jpg')
        #height, width, byteValue = self.cvImage.shape
        #byteValue = byteValue * width

        #cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB, self.cvImage)

        #self.mQImage = QtGui.QImage(self.cvImage, width, height, byteValue, QtGui.QImage.Format_RGB888)

        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        
# def paintEvent(self, QPaintEvent):
#         painter = QtGui.QPainter()
#         painter.begin(self)
#         painter.drawImage(1021, 10, self.mQImage)
#         painter.end()

    def update(self):
        self.img = np.zeros(self.img_size, dtype=np.uint8)
        cv2.circle(self.img,((self.offset_x),(self.offset_y)), 2, (0,200,50), 20)
        for point in self.handler.send_data.lidar_data:
            x, y = self.polar2cart(point[2]//10, point[1]-90)
            cv2.circle(self.img,((x+self.offset_x),(y+self.offset_y)), 2, (255,0,0), 2)
        self.lcdNumber.display(self.handler.send_data.lap)
        self.lcdNumber_2.display(self.handler.send_data.rpm[0])

        height, width, byteValue = self.img.shape
        byteValue = byteValue * width
        imgg = QtGui.QImage(self.img, width, height, byteValue, QtGui.QImage.Format_RGB888)
        self.frame.setImage(imgg)


    # polar to cartesian
    def polar2cart(self,r, theta):
        temp = np.radians(theta)
        x = r * np.cos(temp)
        y = r * np.sin(temp)
        x = int(x)
        y = int(y)
        return x, y
    
    def keyPressEvent(self, event):
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

    def send(self):
        message = self.instr.encode()
        self.handler.add(message)

    def doer(self, func):
        func()
        #instr.printSelf()
        self.send()

    def forward(self):
        #self.S.setChecked(False)
        self.instr._w()
        #instr.printSelf()
        self.send()

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

    def run(self):
        self.instr._run()
        self.send()

    def gettxt(self):
        self.instr.set_p(self.pid_p.text())
        self.instr.set_d(self.pid_d.text())
        #instr.printSelf()
        self.send()
    
    def show_data(self):
        with self.handler.qLock:
            self.send_data.decode(self.handler.response)

    def auto_mode(self):
        self.instr._auto_mode()
        self.send()

    def get_rpm(self):
        return self.handler.send_data.rpm



def main():
    app = QtGui.QApplication(sys.argv)    
    form = ExampleApp()
    
    
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
