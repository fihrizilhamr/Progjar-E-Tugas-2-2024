from socket import *
import socket
import threading
import logging
import time
import sys

class ProcessTheClient(threading.Thread):
    def __init__(self,connection,address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)
		
    def run(self):
        while True:
            data = b''
            while b'\r\n' not in data:
                chunk = self.connection.recv(64)
                if not chunk:
                    break
                data += chunk
            logging.warning(f"data {data} received from {self.address}")
            if data:
                # request = data.decode().upper() # Jika ingin memasukkan lowercase
                request = data.decode()

                if request == ("TIME\r\n"):
                    self.connection.sendall(f"JAM {time.strftime('%H:%M:%S', time.localtime())}\r\n".encode())
                elif request == ("QUIT\r\n"):
                    break 
                else:
                    self.connection.sendall(f"\"{data}\" IS AN INVALID REQUEST\n".encode())
            else:
                break
        self.connection.close()



class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)
            
    def run(self):
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(1)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"connection from {self.client_address}")
            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)
	

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()
