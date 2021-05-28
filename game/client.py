import socket
import threading
import pickle
from view.game_window import game_window
from view.game_window import lock

HEADER = 64
PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.52"
ADDR = (SERVER, PORT)


class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.game_window = game_window(self)
        self.connected = True
        self.to_disconnect = False
        self.your_move = False

    def send(self,msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        self.your_move = False

    def receve_pickle(self):
        msg_length = self.client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length)
            return pickle.loads(msg)

    def recive(self):
        wrapped_msg = self.receve_pickle()
        print(wrapped_msg[0])
        if wrapped_msg[0] == DISCONNECT_MESSAGE:
            #self.client.send("Leaving message".encode(FORMAT))
            # przydolby sie usuwac z dicta rozlaczonego gracza
            print("NAURA")
            self.client.close()
            self.connected = False
        elif wrapped_msg[0] == "YOUR PLAYER":
            self.game_window.player = wrapped_msg[1]
            print(wrapped_msg[1])
        elif wrapped_msg[0] == "CHOOSE MOVE":
            self.your_move = True
            print("Co robisz?")
            if self.to_disconnect:
                self.send("!DISCONNECT")
            else:
                self.game_window.enable_buttons()

        #lock dla opponentów - chyba działa ale nie mam jak sprawdzić
        elif wrapped_msg[0] == "OPPONENT": #dostajemy info o jednym oponencie
            lock.acquire()
            self.game_window.update_opponent(wrapped_msg[1])
            lock.release()
            # print(wrapped_msg[1])
        elif wrapped_msg[0] == "OPPONENTS":  # dostajemy info o wszystkich oponentach
            lock.acquire()
            self.game_window.opponents = wrapped_msg[1]
            dict(sorted(self.game_window.opponents.items(), key=lambda item: item[1].id))
            lock.release()
            # print(wrapped_msg[1])
        elif wrapped_msg[0] == "CARDS":
            self.game_window.tableCards = wrapped_msg[1]
            # print(wrapped_msg[1])
        elif wrapped_msg[0] == "WINNERS":
            # print("WINNERS:")
            #TODO TUTAJ WYWALA ERROR JAK SIE KOLES ROZLACZY - JAKIS IF POWINIEN ZADZIALAC
            self.game_window.tableCards = None
            if not self.to_disconnect:
                self.game_window.update_history(wrapped_msg[1])
            # print(wrapped_msg[1])
        elif wrapped_msg[0] == "GAME INFO":
            lock.acquire()
            self.game_window.game_info = wrapped_msg[1]
            lock.release()
        elif wrapped_msg[0] == "POOL":
            lock.acquire()
            self.game_window.pool = wrapped_msg[1]
            lock.release()
        else:
            return wrapped_msg[0]

    def disconnect_at_move(self):
        self.send("!DISCONNECT")

    def listening(self):
        while self.connected:
            self.recive()
        print("JA JUŻ NIE SLUCHAM")

if __name__ == "__main__":
    client = Client()
    stop_threads = False
    thread = threading.Thread(target=client.listening, args=())
    thread.start()
    nick = client.game_window.login()
    client.game_window.disable_buttons()
    client.send(nick)
    client.game_window.wait_for_players()
    client.game_window.main()

