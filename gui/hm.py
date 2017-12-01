#!/usr/bin/python3
from threadTCPServer import *
import threading
import socketserver
import instructions

import time

if __name__ == "__main__":
    print("Currently in main thread:", threading.current_thread())
    HOST, PORT = "localhost", 10000
    socketserver.TCPServer.allow_reuse_address = True

    server = ThreadedTCPServer( (HOST, PORT), ThreadedTCPRequestHandler)
    server.message = b''
    server.recvd = False

    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    # client(HOST, PORT, "Hello World 1")
    # client(HOST, PORT, "Hello World 2")

    instr = instructions.Instruction()
    try:
        while True:
            time.sleep(0.01)
            if server.recvd:
                instr.decode(server.message)
                instr.printSelf()
                server.recvd = False
            pass
    except KeyboardInterrupt:
        print ("exiting program")

    #Cleanup
    server.shutdown()
    server.socket.close()
