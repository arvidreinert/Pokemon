#http127.0.0.1 port 9000
import pickle
import socket
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 9000 
players_connected = {}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
while True:
    data,addr = s.recvfrom(4096)
    print(pickle.loads(data),addr)
    """if data == b"get_me_the_others_location":
        for address in players_connected:
            if address != addr:
                print("get:othersl", addr, address)
                s.sendto(pickle.dumps(players_connected[address]), addr)

    if b"how many players are online" in data:
        print(True, addr)
        n = len(players_connected)
        s.sendto(pickle.dumps(int(n)), addr)

    if b"adp" in data:
        encoded_string = pickle.loads(data)
        encoded_list = list(encoded_string)
        encoded_string = ""
        for i in range(3,len(encoded_list)):
            encoded_string += str(encoded_list[i])
        players_connected[f"{addr}"] = encoded_string
        s.sendto(pickle.dumps(encoded_string),addr)"""
