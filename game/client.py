import socket
import threading
import pickle

HEADER = 64
PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.65.183"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def listening():
    while connected:
        action = client.recv(2048).decode(FORMAT)
        if action == "YOUR PLAYER":
            status = client.recv(2048)
            full_msg = b'' + status
            d = pickle.loads(full_msg[HEADER:])

            print(d)
        elif action == "CHOOSE MOVE":
            status = client.recv(2048).decode(FORMAT)
            print(status)
            msg = input()
            send(msg)


connected = True
thread = threading.Thread(target=listening, args=())
thread.start()
nick = str(input("Podaj nick: "))
send(nick)

