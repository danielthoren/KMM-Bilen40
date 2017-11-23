import threading
from instrHandler import Handler
from threadTCPServer import client
import socket
import time
from instructions import Instruction

from appjar import gui

if __name__ == "__main__":

    HOST, PORT = "192.168.1.10", 10000
    handler = Handler(HOST, PORT)
    # handler.queue.put("hej")
    # handler.queue.put("hopp")

    handler_thread = threading.Thread(target =handler.hantera)
    handler_thread.daemon = True
    handler_thread.start()

    """
    GUI
    """
    app = gui()
    app.addLabel("title", "TCP-Client test")
    app.setLabelBg("title", "red")

    app.addLabelNumericEntry("pid-P")
    app.addLabelNumericEntry("pid-D")
    instr = Instruction()

    def wasd():
        pass

    def press(button):
        instr.reset_wasd()
        if button == "Send param.":
            p = app.getEntry("pid-P")
            d = app.getEntry("pid-D")
            instr.set_p(p)
            instr.set_d(d)

        elif button == "W":
            instr._w(True)

        elif button == "A":
            instr._a(True)

        elif button == "S":
            instr._s(True)

        elif button == "D":
            instr._d(True)

        message = instr.encode()
        handler.add(message)

        if button == "Quit":
            app.stop()




    app.addButtons(["Send param."], press)
    app.addButtons(["W"], press)
    app.addButtons(["A", "S", "D"], press)
    app.addButtons(["Quit"], press)
    app.enableEnter(app.stop)
    app.go()
