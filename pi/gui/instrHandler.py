'''
Handler for connections from client side.
Participants:
    Alexander Zeijlon
Last changed:
    07/12-2017
'''
import threading
import socket
from threadTCPServer import client
from queue import Queue
import time
from instructions import sendData

# Uses queue with lock to be thread safe when running in separate thread.
class Handler:
    def __init__(self, host = "localhost", port = 10000):
        self.host = host
        self.port = port
        self.queue = Queue()
        self.response = b''
        self.send_data = sendData()
        self.qLock = threading.Lock()

    def hantera(self):
        while True:
            time.sleep(0.01) # Send and request data at interval.
            if self.queue.empty():
                s = b'1'
            else:
                with self.qLock:
                    s = self.queue.get()
            resp = client(self.host, self.port, s)

            with self.qLock:
                self.send_data.decode(resp)

    # Put data in send queue.
    def add(self, s):
        with self.qLock:
            self.queue.put(s)
