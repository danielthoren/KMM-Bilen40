import socket
import threading
import socketserver
import os
import signal
from instructions import Instruction

import time
import random

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.server.message = self.request.recv(4096)
        self.request.sendall(str(random.randint(1,9)).encode('ascii'))
        #cur_thread = threading.current_thread()
        #pid = os.getpid()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    response = b''
    
    try:
        sock.sendall(message)
        response = sock.recv(4096)
    finally:
        #sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        return response

if __name__ == "__main__":

    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 10000
    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address


    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name, "PID =", os.getpid())

    print(server.test)
    # try:
    #     while True:
    #         pass
    # except KeyboardInterrupt:
    #     print("Ctrl-C")

    server.shutdown()
    server.socket.close()
