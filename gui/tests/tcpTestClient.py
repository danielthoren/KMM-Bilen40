import threading
import socket
import time

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 10000)
    message = b'hejsan123'
    print("Connecting to {}:{}".format(*server_address))
    try:
        sock.connect(server_address)
        asd = sock.sendall(message)
        retur = sock.recv(1024)
        print (asd)
        print(retur)
        sock.close()
    except Exception as e:
        print(e)
