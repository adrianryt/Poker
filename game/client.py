import socket
import threading
import pickle
from view.game_window import game_window
from view.game_window import lock

HEADER = 64
PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.65.183"
ADDR = (SERVER, PORT)





class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.game_window = game_window(self.client)
        self.connected = True

    def send(self,msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def receve_pickle(self):
        msg_length = self.client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length)
            return pickle.loads(msg)

    def recive(self):
        wrapped_msg = self.receve_pickle()
        if wrapped_msg[0] == DISCONNECT_MESSAGE:
            self.client.send("Leaving message".encode(FORMAT))
            # przydolby sie usuwac z dicta rozlaczonego gracza
            self.client.close()
        elif wrapped_msg[0] == "YOUR PLAYER":
            self.game_window.player = wrapped_msg[1]
            print(wrapped_msg[1])
        elif wrapped_msg[0] == "CHOOSE MOVE":
            print("Co robisz?")
            self.game_window.enable_buttons()
            while self.game_window.ACTION is None:
                pass
            self.send(self.game_window.ACTION)
            self.game_window.ACTION = None
            self.game_window.disable_buttons()
        #lock dla opponentów - chyba działa ale nie mam jak sprawdzić
        elif wrapped_msg[0] == "OPPONENT": #dostajemy info o jednym oponencie
            lock.acquire()
            self.game_window.update_opponent(wrapped_msg[1])
            lock.release()
            print(wrapped_msg[1])
        elif wrapped_msg[0] == "OPPONENTS":  # dostajemy info o wszystkich oponentach
            lock.acquire()
            self.game_window.opponents = wrapped_msg[1]
            lock.release()
            dict(sorted(self.game_window.opponents.items(), key=lambda item: item[1].id))
            print(wrapped_msg[1])
        elif wrapped_msg[0] == "CARDS":
            self.game_window.tableCards = wrapped_msg[1]
            print(wrapped_msg[1])
        elif wrapped_msg[0] == "WINNERS":
            print("WINNERS:")
            #TODO przydaloby sie gdzie indziej to dac, ale cos nie idzie bo pruje dupe
            self.game_window.tableCards = None
            print(wrapped_msg[1])
        else:
            return wrapped_msg[0]

    def listening(self):
        while self.connected:
            self.recive()


if __name__ == "__main__":
    client = Client()
    thread = threading.Thread(target=client.listening, args=())
    thread.start()
    nick = client.game_window.login()
    client.game_window.disable_buttons()
    client.send(nick)
    client.game_window.wait_for_players()
    client.game_window.main()

