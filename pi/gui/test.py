from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import QImage
from PyQt4.QtGui import QApplication, QMainWindow, QPushButton
import sys , time , datetime
import cv2
import numpy as np

video = cv2.VideoCapture(0)
video.set(3,1280)
video.set(4,1024)
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

    # here get the mouseclick and move..
    def mousePressEvent(self, event): # click
        print event.pos()

    def mouseMoveEvent(self, event): # move
        print event.pos()

class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)

        self.fAction = QtGui.QAction(u"click me", self)

        menubar = self.menuBar()
        self.fileMenu = menubar.addAction(u"click me")
        font = self.fileMenu.font()
        font.setPointSize(30)
        menubar.setFont(font)

        self.videoFrame=ImageWidget()
        self.setCentralWidget(self.videoFrame)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.showFullScreen()
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
    def update(self):
            ret, frame = video.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0],frame.strides[0], QtGui.QImage.Format_RGB888)
            image.scaledToWidth (640,QtCore.Qt.SmoothTransformation)
            image.scaledToHeight(480,QtCore.Qt.SmoothTransformation)
            # here is sclae my image...
            result = image.scaled(640, 480, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
            self.videoFrame.setImage(result)
def main():
    app=QtGui.QApplication(sys.argv)
    w=MainWindow()
    w.show()
    app.exec_()

if __name__=='__main__':
    main()
