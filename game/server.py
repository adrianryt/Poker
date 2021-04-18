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
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        idx+=1
        if len(conn_dict) == LIMIT:
            return


def sendToAllPlayers():
    for conn in conn_dict:
        conn.send("Msg to all".encode(FORMAT))

def sendCardsOnTable(players):
    for p in players:
        send(conn_dict[p.id], "CARDS")
        bin = recive(conn_dict[p.id])
        msg_to_client = pickle.dumps(game_table.tableCards)
        msg_to_client = bytes(f'{len(msg_to_client):<{HEADER}}', "utf-8") + msg_to_client
        conn_dict[p.id].send(msg_to_client)

def sendClientData(players):
    for player in players:
        send(conn_dict[player.id], "YOUR PLAYER")
        bin = recive(conn_dict[player.id])
        msg_to_client = pickle.dumps(player)
        msg_to_client = bytes(f'{len(msg_to_client):<{HEADER}}', "utf-8") + msg_to_client
        conn_dict[player.id].send(msg_to_client)


def sendDataToRivals(players, client):
    rivals = [p for p in players if p.id != client.id]
    for r in rivals:
        send(conn_dict[r.id], "OPPONENT")
        bin = recive(conn_dict[r.id])
        #powinnismy wysylac tylko info dotyczace nazwy gracza, jego zetonow, i zetonow w puli
        #narazie wysylam wszystkie informacje o graczu
        msg_to_client = pickle.dumps(client)
        msg_to_client = bytes(f'{len(msg_to_client):<{HEADER}}', "utf-8") + msg_to_client
        conn_dict[r.id].send(msg_to_client)


def sendWhoWon(players, winners):
    for p in players:
        send(conn_dict[p.id], "WINNERS")
        bin = recive(conn_dict[p.id])
        # powinnismy wysylac tylko info dotyczace nazwy gracza, jego zetonow, i zetonow w puli
        # narazie wysylam wszystkie informacje o graczu
        msg_to_client = pickle.dumps(winners)
        msg_to_client = bytes(f'{len(msg_to_client):<{HEADER}}', "utf-8") + msg_to_client
        conn_dict[p.id].send(msg_to_client)

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
                    send(conn_dict[p.id], "CHOOSE MOVE")
                    what_to_do = recive(conn_dict[p.id])
                    print(what_to_do)
                    if what_to_do == "fold":
                        p.fold(game_table)
                    if what_to_do == "raise":  # robienie na stole/allin
                        p.raisee(game_table, 100)
                    if what_to_do == "check":
                        p.check()
                    if what_to_do == "call":
                        p.call(game_table)
                    sendClientData([p]) #po to zeby klient mial pewnosc co zrobil, znikna mu wtedy zetony np.
                    sendDataToRivals(game_table.players, p)
                if all(p.tokens_in_pool == game_table.get_biggest_bet() or p.tokens == 0 for p in
                       game_table.players_in_round) and idx >= players_number + 2:
                    break

        game_table.deal_flop()
        print("AFTER FLOP (3karty pokazane na stole)")
        sendCardsOnTable(game_table.players)
        print(game_table.players_in_round)
        if len(game_table.players_in_round) > 1:
            players_number = len(game_table.players)
            for idx, p in enumerate(itertools.cycle(game_table.players), 1):
                if p in game_table.players_in_round and len(game_table.players_in_round) > 1:
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
                    sendClientData([p])  # po to zeby klient mial pewnosc co zrobil, znikna mu wtedy zetony np.
                    sendDataToRivals(game_table.players, p)
                if all(p.tokens_in_pool == game_table.get_biggest_bet() or p.tokens == 0 for p in
                       game_table.players_in_round) and idx >= players_number:
                    break
        game_table.deal_turn_river()
        sendCardsOnTable(game_table.players)
        print("AFTER TURN (kolejna karta na stole)")
        if len(game_table.players_in_round) > 1:
            players_number = len(game_table.players)
            for idx, p in enumerate(itertools.cycle(game_table.players), 1):
                if p in game_table.players_in_round and len(game_table.players_in_round) > 1:
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
                    sendClientData([p])  # po to zeby klient mial pewnosc co zrobil, znikna mu wtedy zetony np.
                    sendDataToRivals(game_table.players, p)
                if all(p.tokens_in_pool == game_table.get_biggest_bet() or p.tokens == 0 for p in
                       game_table.players_in_round) and idx >= players_number:
                    break
        game_table.deal_turn_river()
        sendCardsOnTable(game_table.players)
        print("AFTER RIVER (kolejna karta na stole)")
        if len(game_table.players_in_round) > 1:
            players_number = len(game_table.players)
            for idx, p in enumerate(itertools.cycle(game_table.players), 1):
                if p in game_table.players_in_round and len(game_table.players_in_round) > 1:
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
                    sendClientData([p])  # po to zeby klient mial pewnosc co zrobil, znikna mu wtedy zetony np.
                    sendDataToRivals(game_table.players, p)
                if all(p.tokens_in_pool == game_table.get_biggest_bet() or p.tokens == 0 for p in
                       game_table.players_in_round) and idx >= players_number:
                    break
        winners = game_table.reveal_winners()
        sendWhoWon(game_table.players, winners)
        game_table.new_round()


if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()
    engine()
