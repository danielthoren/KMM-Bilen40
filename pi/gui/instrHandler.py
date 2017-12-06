import threading
import socket
from threadTCPServer import client
from queue import Queue

class Handler:
    def __init__(self, host = "localhost", port = 10000):
        self.host = host
        self.port = port
        self.queue = Queue()
        self.qLock = threading.Lock()

    def hantera(self):
        while True:
            if not self.queue.empty():
                with self.qLock:
                    s = self.queue.get()
                client(self.host, self.port, s)

    def add(self, s):
        with self.qLock:
            self.queue.put(s)
