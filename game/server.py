import socket
import threading
from classes.table import Table
from classes.layouts import *
from classes.game_info import GameInfo
from classes.limited_player import LimitedPlayer
import itertools
import pickle

HEADER = 64
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

game_info = GameInfo(10,30)
game_table = Table(game_info)
conn_dict = {}

LIMIT = int(input("Podaj liczbe graczy"))

def recive(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            conn.send("Leaving message".encode(FORMAT))
            #przydolby sie usuwac z dicta rozlaczonego gracza
            conn.close()
        else:
            return msg

def send(msg_to, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    msg_to.send(send_length)
    msg_to.send(message)

def start():
    print(f"[LISTENING] Server is listening on {SERVER}")
    server.listen()
    idx = 0
    while True:
        conn, addr = server.accept()
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            nick = conn.recv(msg_length).decode(FORMAT)
            player = Player(1000, idx, nick)
            game_table.add_player(player)
            conn_dict[idx] = conn
        print(f"[ACTIVE CONNECTIONS] {len(conn_dict)}")
        idx+=1
        if len(conn_dict) == LIMIT:
            return

#def sendToAllPlayers():
    #for conn in conn_dict:
        #conn.send("Msg to all".encode(FORMAT))

def send_pickle(player,msg): #(do kogo, co)
    bin = recive(conn_dict[player.id])
    msg_to_client = pickle.dumps(msg)
    msg_to_client = bytes(f'{len(msg_to_client):<{HEADER}}', "utf-8") + msg_to_client
    conn_dict[player.id].send(msg_to_client)

def sendCardsOnTable(players):
    for p in players:
        send(conn_dict[p.id], "CARDS")
        send_pickle(p,game_table.tableCards) #do kogo oraz co wysyłamy

def sendClientData(players):
    for p in players:
        send(conn_dict[p.id], "YOUR PLAYER")
        send_pickle(p,p)

def sendDataToRivals(players, client):
    rivals = [p for p in players if p.id != client.id]
    for r in rivals:
        send(conn_dict[r.id], "OPPONENT")
        tmp = LimitedPlayer(client)
        send_pickle(r,tmp)

def sendWhoWon(players, winners):
    tmp =[]
    for winner in winners:
        tmp.append(LimitedPlayer(winner))
    for p in players:
        send(conn_dict[p.id], "WINNERS")
        send_pickle(p,tmp)

def round_action(p):
    send(conn_dict[p.id], "CHOOSE MOVE")
    what_to_do = recive(conn_dict[p.id])
    if what_to_do == "fold":
        p.fold(game_table)
    if what_to_do == "raise":
        p.raisee(game_table, 100)
    if what_to_do == "check":
        p.check()
    if what_to_do == "call":
        p.call(game_table)
    if what_to_do == "allIn":
        p.allIn(game_table)

    sendClientData([p])  # po to zeby klient mial pewnosc co zrobil, znikna mu wtedy zetony np.
    sendDataToRivals(game_table.players, p)

def make_round():
    players_number = len(game_table.players)
    for idx, p in enumerate(itertools.cycle(game_table.players), 1):
        if p in game_table.players_in_round and len(game_table.players_in_round) > 1:
            round_action(p)
        if all(p.tokens_in_pool == game_table.get_biggest_bet() or p.tokens == 0 for p in
               game_table.players_in_round) and idx >= players_number:
            break

#Uwagi do silnika:
#1.Raise do danej ilości mamony i żeby nie przekraczało obecnie posiadanej
#2.Check musi być czasami wyłączony - chyba da się to zrobić sprawdzając czy poprzedni gracz ma tyle samo "token_in_pool" co gracz na ruchu
#3.Opcja allIn - On powinien cały czas być w grze ale już mi się łeb kopci i nie wiem


def engine():
    while True:
        print("NEW ROUND")
        game_table.update_players_in_round()
        # tutaj pobieramy small i big blinda od odpowiednich osob, ostatnia osoba w liscie jest dealerem
        game_table.add_to_pool(game_table.get_small_blind(), game_table.players[0])
        game_table.add_to_pool(game_table.get_big_blind(), game_table.players[1])
        # na poczatek zawsze rozdajemy karty graczom
        game_table.deal_cards_players()
        sendClientData(game_table.players)
        # te petle to te rozdania
        if len(game_table.players_in_round) > 1:
            players_number = len(game_table.players)
            for idx, p in enumerate(itertools.cycle(game_table.players), 1):
                if p in game_table.players_in_round and idx != 1 and idx != 2 and len(game_table.players_in_round) > 1:
                   round_action(p)
                if all(p.tokens_in_pool == game_table.get_biggest_bet() or p.tokens == 0 for p in
                       game_table.players_in_round) and idx >= players_number + 2:
                    break

        print("AFTER FLOP (3karty pokazane na stole)")
        game_table.deal_flop()
        sendCardsOnTable(game_table.players)
        print(game_table.players_in_round)
        if len(game_table.players_in_round) > 1:
            make_round()

        print("AFTER TURN (kolejna karta na stole)")
        game_table.deal_turn_river()
        sendCardsOnTable(game_table.players)
        if len(game_table.players_in_round) > 1:
           make_round()

        print("AFTER RIVER (kolejna karta na stole)")
        game_table.deal_turn_river()
        sendCardsOnTable(game_table.players)
        if len(game_table.players_in_round) > 1:
            make_round()

        winners = game_table.reveal_winners()
        sendWhoWon(game_table.players, winners)
        game_table.new_round()

if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()
    engine()
