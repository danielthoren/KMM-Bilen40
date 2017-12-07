import threading
import socket
from threadTCPServer import client
from queue import Queue
import time
from instructions import sendData

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
            time.sleep(0.01)
            if self.queue.empty():
                s = b'1'
            else:
                with self.qLock:
                    s = self.queue.get()
            resp = client(self.host, self.port, s)
            # print(resp)
            with self.qLock:
                # self.response = resp
                self.send_data.decode(resp)
            # print(self.response)

    def add(self, s):
        with self.qLock:
            self.queue.put(s)
