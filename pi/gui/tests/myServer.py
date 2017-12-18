#!/usr/bin/python3
import json
from time import sleep
from clientserver import Server
from instr import *
import pickle
import socket, errno

def main():
    myServer = Server()

    while True:
        myServer.sendMessage("1".encode("ascii"))
             
        message = myServer.recv()
        if message:
            myInstr = pickle.loads(message)
            myInstr.printSelf()
            if myInstr.quit == True:
                break

    myServer.disconnect()

main()
