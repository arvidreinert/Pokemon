import pickle
import socket
HOST = "127.0.0.1"
PORT = 9000

class server_manager():
    def __init__(self):
        self.server_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_s.connect((HOST, PORT))
        self.send("login")

    def send(self,msg):
        msg = pickle.dumps(msg)
        self.server_s.sendall(msg)

    def send_and_listen(self,msg):
        self.send(msg)
        received_data = pickle.loads(self.server_s.recv(4096))
        return received_data
