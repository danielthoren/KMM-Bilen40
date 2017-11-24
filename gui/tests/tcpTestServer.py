import threading
import socket
import time

if __name__ == "__main__":
    server_address = ("", 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Starting up on {}:{}".format(*server_address))
    sock.bind(server_address)

    print("Listening for connections")
    sock.listen(1)

    connection, cli_address = sock.accept()
    print("Accepted connection")
    while True:
        try:
            status = connection.recv(1024)
            if status:
                connection.sendall(status)
                print(status)
        except Exception as e:
            print(e)

        except KeyboardInterrupt:
            break
    connection.close()
    sock.close()
