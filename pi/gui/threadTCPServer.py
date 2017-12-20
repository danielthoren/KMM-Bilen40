'''
Defines the sendData type that is used to send data from RPi to GUI.
Defines the instruction type that is used to send data from GUI to RPi.

Participants:
    Alexander Zeijlon
    Gustaf Söderholm

Last changed:
    17/12-2017
'''


import socket
import threading
import socketserver
import os
import signal
from instructions import Instruction
import time

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.server.message = self.request.recv(4096)
        self.request.sendall(self.server.sendmessage)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

# Used by client to receive arbitrary chunk of data.
def client(ip, port, message):
    def recv():
        r = sock.recv(2048)
        tot_r = r
        while r:
            r =sock.recv(2048)
            tot_r += r
            if not r:
                break
        
        return tot_r
            
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    response = b''
    
    try:
        sock.sendall(message)
        response = recv()
    finally:
        sock.close()
        return response
