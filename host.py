#http127.0.0.1 port 9000
import pickle
import socket
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 9000 
players_connected = {}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
#to who, what
actions_receveid = "False"
while True:
    data,addr = s.recvfrom(4096)
    data = pickle.loads(data)
    if data == "break":
        print("shutting down server")
        break

    if data == "login":
        players_connected[addr] = data
        print(players_connected)
        s.sendto(pickle.dumps("logged in succesfull"), addr)
    
    if data == "req peer online":
        l = len(list(players_connected))
        s.sendto(pickle.dumps(str(l)), addr)
    
    if data == "req clients turn":
        l = list(players_connected)
        s.sendto(pickle.dumps(str(l.index(addr)==0)), addr)

    if "actio;" in data:
        print(data)
        print(data.split(";"))
        #output: ['actio', "['create:card0,arvid_charzard_deck0.png,arvid_charzard_deck0.png0']"]
        actions_receveid = data.split(";")[1]
        print(actions_receveid)

    if data == "req:actio":
        print(actions_receveid)
        if actions_receveid == "False":
            s.sendto(pickle.dumps("False"), addr)
        else:
            s.sendto(pickle.dumps(actions_receveid), addr)

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
