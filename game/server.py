import socket
import threading
from classes.table import Table
from classes.layouts import *
from classes.game_info import GameInfo
import itertools
import pickle

HEADER = 64
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

game_info = GameInfo(10,30)
game_table = Table(game_info)
conn_list = []

LIMIT = int(input("Podaj liczbe graczy"))

def handle_client(conn, addr, id):
    print(f"[NEW CONNECTION] {addr} connected.")
    print("Your nick: " + game_table.players[id].name)
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                conn.send("Leaving message".encode(FORMAT))
                connected = False
            print(f"[{addr}] {msg}")
            sendToAllPlayers()
    conn_list.remove(conn)
    conn.close()

def message(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            conn.send("Leaving message".encode(FORMAT))
            conn_list.remove(conn)
            conn.close()
        else:
            return msg

def start():
    print(f"[LISTENING] Server is listening on {SERVER}")
    server.listen()
    idx = 0
    while True:
        conn, addr = server.accept()
        conn_list.append(conn)
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            nick = conn.recv(msg_length).decode(FORMAT)
            player = Player(1000, idx, nick)
            game_table.add_player(player)
        # thread = threading.Thread(target=handle_client, args=(conn, addr))
        # thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        idx+=1
        if len(conn_list) == LIMIT:
            return


def sendToAllPlayers():
    for conn in conn_list:
        conn.send("Msg to all".encode(FORMAT))

def sendInfoToPlayers(players):
    for player in players:
        conn_list[player.id].send("YOUR PLAYER".encode(FORMAT))
        bin = message(conn_list[player.id])
        msg_to_client = pickle.dumps(player)
        msg_to_client = bytes(f'{len(msg_to_client):<{HEADER}}', "utf-8") + msg_to_client
        conn_list[player.id].send(msg_to_client)


def engine():
    while True:
        print("NEW ROUND")
        game_table.update_players_in_round()
        # tutaj pobieramy small i big blinda od odpowiednich osob, ostatnia osoba w liscie jest dealerem
        game_table.add_to_pool(game_table.get_small_blind(), game_table.players[0])
        game_table.add_to_pool(game_table.get_big_blind(), game_table.players[1])
        # na poczatek zawsze rozdajemy karty graczom
        game_table.deal_cards_players()
        sendInfoToPlayers(game_table.players)
        print("DUPA")
        # te petle to te rozdania
        if len(game_table.players_in_round) > 1:
            players_number = len(game_table.players)
            for idx, p in enumerate(itertools.cycle(game_table.players), 1):
                if p in game_table.players_in_round and idx != 1 and idx != 2 and len(game_table.players_in_round) > 1:
                    conn_list[p.id].send("CHOOSE MOVE".encode(FORMAT))
                    conn_list[p.id].send("What you wanna do?".encode(FORMAT))
                    what_to_do = message(conn_list[p.id])
                    print(what_to_do)
                    if what_to_do == "fold":
                        p.fold(game_table)
                    if what_to_do == "raise":  # robienie na stole/allin
                        p.raisee(game_table, 100)
                    if what_to_do == "check":
                        p.check()
                    if what_to_do == "call":
                        p.call(game_table)
                if all(p.tokens_in_pool == game_table.get_biggest_bet() or p.tokens == 0 for p in
                       game_table.players_in_round) and idx >= players_number + 2:
                    break

        game_table.deal_flop()
        print("AFTER FLOP (3karty pokazane na stole)")
        print(game_table.players_in_round)
        if len(game_table.players_in_round) > 1:
            players_number = len(game_table.players)
            for idx, p in enumerate(itertools.cycle(game_table.players), 1):
                if p in game_table.players_in_round and len(game_table.players_in_round) > 1:
                    conn_list[p.id].send("CHOOSE MOVE".encode(FORMAT))
                    conn_list[p.id].send("What you wanna do?".encode(FORMAT))
                    what_to_do = message(conn_list[p.id])
                    if what_to_do == "fold":
                        p.fold(game_table)
                    if what_to_do == "raise":
                        p.raisee(game_table, 100)
                    if what_to_do == "check":
                        p.check()
                    if what_to_do == "call":
                        p.call(game_table)
                if all(p.tokens_in_pool == game_table.get_biggest_bet() or p.tokens == 0 for p in
                       game_table.players_in_round) and idx >= players_number:
                    break
        game_table.deal_turn_river()
        print("AFTER TURN (kolejna karta na stole)")
        if len(game_table.players_in_round) > 1:
            players_number = len(game_table.players)
            for idx, p in enumerate(itertools.cycle(game_table.players), 1):
                if p in game_table.players_in_round and len(game_table.players_in_round) > 1:
                    conn_list[p.id].send("CHOOSE MOVE".encode(FORMAT))
                    conn_list[p.id].send("What you wanna do?".encode(FORMAT))
                    what_to_do = message(conn_list[p.id])
                    if what_to_do == "fold":
                        p.fold(game_table)
                    if what_to_do == "raise":
                        p.raisee(game_table, 100)
                    if what_to_do == "check":
                        p.check()
                    if what_to_do == "call":
                        p.call(game_table)
                if all(p.tokens_in_pool == game_table.get_biggest_bet() or p.tokens == 0 for p in
                       game_table.players_in_round) and idx >= players_number:
                    break
        game_table.deal_turn_river()
        print("AFTER RIVER (kolejna karta na stole)")
        if len(game_table.players_in_round) > 1:
            players_number = len(game_table.players)
            for idx, p in enumerate(itertools.cycle(game_table.players), 1):
                if p in game_table.players_in_round and len(game_table.players_in_round) > 1:
                    conn_list[p.id].send("CHOOSE MOVE".encode(FORMAT))
                    conn_list[p.id].send("What you wanna do?".encode(FORMAT))
                    what_to_do = message(conn_list[p.id])
                    if what_to_do == "fold":
                        p.fold(game_table)
                    if what_to_do == "raise":
                        p.raisee(game_table, 100)
                    if what_to_do == "check":
                        p.check()
                    if what_to_do == "call":
                        p.call(game_table)
                if all(p.tokens_in_pool == game_table.get_biggest_bet() or p.tokens == 0 for p in
                       game_table.players_in_round) and idx >= players_number:
                    break
        print(game_table.tableCards)
        game_table.reveal_winners()
        print(game_table.players)

        game_table.new_round()


print("[STARTING] server is starting...")

start()
engine()
