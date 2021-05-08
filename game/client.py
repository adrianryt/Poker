import socket
import threading
import pickle
from view.game_window import game_window

HEADER = 64
PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.65.183"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

game_window = game_window()

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def receve_pickle():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length)
        return pickle.loads(msg)

def recive():
    wrapped_msg = receve_pickle()
    if wrapped_msg[0] == DISCONNECT_MESSAGE:
        client.send("Leaving message".encode(FORMAT))
        # przydolby sie usuwac z dicta rozlaczonego gracza
        client.close()
    elif wrapped_msg[0] == "YOUR PLAYER":
        game_window.player = wrapped_msg[1]
        print(wrapped_msg[1])
    elif wrapped_msg[0] == "CHOOSE MOVE":
        print("Co robisz?")
        game_window.reset_buttons()
        while game_window.ACTION == None:
            pass
        send(game_window.ACTION)
        game_window.ACTION = None

    elif wrapped_msg[0] == "OPPONENT": #dostajemy info o jednym oponencie
        game_window.update_opponent(wrapped_msg[1])
        print(wrapped_msg[1])
    elif wrapped_msg[0] == "OPPONENTS":  # dostajemy info o wszystkich oponentach
        game_window.opponents = wrapped_msg[1]
        print(wrapped_msg[1])
    elif wrapped_msg[0] == "CARDS":
        game_window.tableCards = wrapped_msg[1]
        print(wrapped_msg[1])
    elif wrapped_msg[0] == "WINNERS":
        print("WINNERS:")
        game_window.tableCards = None
        print(wrapped_msg[1])
    else:
        return wrapped_msg[0]


def listening():
    while connected:
        recive()


if __name__ == "__main__":
    connected = True
    thread = threading.Thread(target=listening, args=())
    thread.start()
    nick = str(input("Podaj nick: "))
    send(nick)
    game_window.main()