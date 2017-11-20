import socket
import threading
import socketserver
import os
import signal

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        #data = str(self.rfile.readline(), 'ascii')
        data = str(self.request.recv(1024), 'utf-8')
        self.server.test = data
        cur_thread = threading.current_thread()
        pid = os.getpid()
        response = bytes("{}: {}".format(pid, data), 'utf-8')
        res = str("Server received: {}".format(response.decode("utf-8"), 'ascii'))
        print(res)
        #self.wfile.write(response)
        #self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(bytes(message, 'utf-8'))
        #response = str(sock.recv(1024), 'ascii')
        #print("Received: {}".format(response))
    finally:
        sock.close()

if __name__ == "__main__":

    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 10000
    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    server.test = ''

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name, "PID =", os.getpid())

    client(ip, port, "Hello World 1")
    client(ip, port, "Hello World 2")
    client(ip, port, "Hello World 3")
    print(server.test)
#    try:
#        while True:
#            pass
#    except KeyboardInterrupt:
#        print("Ctrl-C")

    server.shutdown()
    server.socket.close()
