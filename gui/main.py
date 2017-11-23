from PyQt4 import QtGui, QtCore
import sys
import design
import threading
from instrHandler import Handler
from threadTCPServer import client
import time
from instructions import Instruction

class ExampleApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.setupTCP()
        self.W.clicked.connect(lambda: self.forward())
        self.S.clicked.connect(lambda: self.backward())
        self.A.clicked.connect(lambda: self.doer(self.instr._a))
        self.D.clicked.connect(lambda: self.doer(self.instr._d))
        self.stop.clicked.connect(lambda: self.reset())
        self.sendparam.clicked.connect(lambda: self.gettxt())
        #self.W.clicked.connect(lambda: print("hello"))

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

    def gettxt(self):
        self.instr.set_p(self.pid_p.text())
        self.instr.set_d(self.pid_d.text())
        #instr.printSelf()
        self.send()
    
    
    


def main():
    app = QtGui.QApplication(sys.argv)    
    form = ExampleApp()
    
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
