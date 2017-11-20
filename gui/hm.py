from threadTCPServer import *
import threading
import socketserver


import time

if __name__ == "__main__":
    print("Currently in main thread:", threading.current_thread())
    HOST, PORT = "localhost", 10000
    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer( (HOST, PORT), ThreadedTCPRequestHandler)

    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    # client(HOST, PORT, "Hello World 1")
    # client(HOST, PORT, "Hello World 2")

    try:
        while True:
            time.sleep(0.0000001)
            pass
    except KeyboardInterrupt:
        print ("exiting program")

    #Cleanup
    server.shutdown()
    server.socket.close()
