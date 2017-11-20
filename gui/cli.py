import threading
from instrHandler import Handler
from threadTCPServer import client
import socket
import time

from appjar import gui

if __name__ == "__main__":

    HOST, PORT = "localhost", 10000
    handler = Handler(HOST, PORT)
    # handler.queue.put("hej")
    # handler.queue.put("hopp")

    handler_thread = threading.Thread(target =handler.hantera)
    handler_thread.daemon = True
    handler_thread.start()

    handler.add("hej")
    handler.add("hopp")

    """
    GUI
    """
    app = gui()
    app.addLabel("title", "TCP-Client test")
    app.setLabelBg("title", "red")

    app.addLabelEntry("Message")

    def press(button):
        msg = app.getEntry("Message")
        if button == "Send":
            handler.add(msg)
        elif button == "Cancel":
            app.stop()

    app.addButtons(["Send", "Cancel"], press)
    app.go()
