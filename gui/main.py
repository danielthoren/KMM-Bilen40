from PyQt4 import QtGui
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
        #self.W.clicked.connect(lambda: print("hello"))


def main():
    instr = Instruction()
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    """
    TCP
    """
    host, port = "localhost", 10000
    handler = Handler(host, port)

    handler_thread = threading.Thread(target = handler.hantera)
    handler_thread.daemon = True
    handler_thread.start()

    def send():
        message = instr.encode()
        handler.add(message)

    def doer(func):
        func()
        #instr.printSelf()
        send()

    def forward():
        form.S.setChecked(False)
        instr._w()
        #instr.printSelf()
        send()

    def backward():
        form.W.setChecked(False)
        instr._s()
        #instr.printSelf()
        send()

    def reset():
        instr.reset_wasd()
        form.S.setChecked(False)
        form.W.setChecked(False)
        #instr.printSelf()
        send()

    def gettxt():
        instr.set_p(form.pid_p.text())
        instr.set_d(form.pid_d.text())
        #instr.printSelf()
        send()
    """
    GUI
    """

    form.W.clicked.connect(lambda: forward())
    form.S.clicked.connect(lambda: backward())
    form.A.clicked.connect(lambda: doer(instr._a))
    form.D.clicked.connect(lambda: doer(instr._d))
    form.stop.clicked.connect(lambda: reset())
    form.sendparam.clicked.connect(lambda: gettxt())
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
