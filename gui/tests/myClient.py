#!/usr/bin/python3
from time import sleep
from clientserver import Client
import json
from instr import *
import pickle

def main():

    myInstr = Instr()
    myInstr.printSelf()
    message = pickle.dumps(myInstr, -1)

    myClient = Client()
    myClient.connect()

    myClient.sendMessage(message)

    sleep(0.5)

    myInstr.turnLeft(True)
    myInstr.printSelf()
    message = pickle.dumps(myInstr, -1)
    myClient.sendMessage(message)

    sleep(0.5)

    myInstr.turnRight(True)
    myInstr.printSelf()
    message = pickle.dumps(myInstr, -1)
    myClient.sendMessage(message)

    myClient.disconnect()

main()
