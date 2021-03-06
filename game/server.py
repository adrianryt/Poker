import socket
from classes.table import Table
from classes.layouts import *
from classes.game_info import GameInfo
from classes.limited_player import LimitedPlayer
import itertools
import pickle
import time

HEADER = 64
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

TOKENS = 1000
SMALL_BLIND = 10

#podanie danych o rozgrywce
game_info = GameInfo(SMALL_BLIND, 30)
game_table = Table(game_info)
conn_dict = {}
players_to_remove = []

LIMIT = None

def recive(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            idx = None
            p = None
            for key, val in conn_dict.items():
                if val == conn:
                    idx = key
            for player in game_table.players:
                if player.id == idx:
                    p = player
            players_to_remove.append(p)
            return msg
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
            player = Player(TOKENS, idx, nick)
            game_table.add_player(player)
            conn_dict[idx] = conn
        print(f"[ACTIVE CONNECTIONS] {len(conn_dict)}")
        idx += 1
        if len(conn_dict) == LIMIT:
            return


def wrap_message(type, msg):  # string oraz co?? co chcemy do message w??o??y??
    result = (type, msg)
    return result


def send_pickle(player, msg):  # (do kogo, co)
    msg_to_client = pickle.dumps(msg)
    msg_to_client = bytes(f'{len(msg_to_client):<{HEADER}}', "utf-8") + msg_to_client
    conn_dict[player.id].send(msg_to_client)


# wys??anie do graczy jakie karty pojawi??y si?? na stole
def send_table_cards(players):
    for p in players:
        wrapped_msg = wrap_message("CARDS", game_table.table_cards)
        send_pickle(p, wrapped_msg)


# wys??anie ka??demu graczowi informacji o sobie samym
def send_client_data(players):
    for p in players:
        wrapped_msg = wrap_message("YOUR PLAYER", p)
        send_pickle(p, wrapped_msg)


# wys??anie informacji o danym graczu do przeciwnik??w, wysy??any jest LimitedPlayer
def send_data_to_opponents(players, client):
    opponents = [p for p in players if p.id != client.id]
    limited_client = LimitedPlayer(client)
    wrapped_msg = wrap_message("OPPONENT", limited_client)
    for opponent in opponents:
        send_pickle(opponent, wrapped_msg)


def send_who_won(players, winners):
    limited_winners = [LimitedPlayer(winner) for winner in winners]
    for p in players:
        wrapped_msg = wrap_message("WINNERS", limited_winners)
        send_pickle(p, wrapped_msg)


# wys??anie wszystkim graczom informacji o przeciwnikach, wysy??ane jest LimitedPlayer
def send_opponents_data(players):
    limited_players_dict = {player.id: LimitedPlayer(player) for player in players}
    for player in players:
        limited_players_dict.pop(player.id)
        wrapped_msg = wrap_message("OPPONENTS", limited_players_dict)
        send_pickle(player, wrapped_msg)
        limited_players_dict[player.id] = LimitedPlayer(player)


# po ostatniej rundzie wysy??amy do ka??dego gracza kt??ry jest przy stole, PELNE informacje o graczach ktorzy dotrwali to ostatniej rundy
def send_players_last_round(all_players, active_players):
    if len(active_players) > 1:
        for all_p in all_players:
            for p_a in active_players:
                if p_a != all_p:
                    wrapped_msg = wrap_message("OPPONENT", p_a)
                    send_pickle(all_p, wrapped_msg)


def send_game_info(all_players, info, tokens_pool):
    game_info = wrap_message("GAME INFO", info)
    pool = wrap_message("POOL", tokens_pool)
    for p in all_players:
        send_pickle(p, game_info)
        send_pickle(p, pool)


def round_action(p): #p - player
    wrapped_msg = wrap_message("CHOOSE MOVE", p)
    send_pickle(p, wrapped_msg)
    # on tutaj czeka na odpowiedz - czyli na klikniecie buttona
    what_to_do = recive(conn_dict[p.id])
    if what_to_do == "fold":
        p.fold(game_table)
    elif what_to_do.startswith("raise"):
        tokens = what_to_do[5:]
        p.raisee(game_table, int(tokens))
    elif what_to_do == "check":
        p.check()
    elif what_to_do == "call":
        p.call(game_table)
    elif what_to_do == "allin":
        p.all_in(game_table)
    else:  # to dla !DISCONNECT
        p.fold(game_table)

    send_client_data([p])  # po to zeby klient mial pewnosc co zrobil, znikna mu wtedy zetony np.
    send_data_to_opponents(game_table.players, p)


def make_round():
    players_number = len(game_table.players)
    for idx, p in enumerate(itertools.cycle(game_table.players), 1):
        if p in game_table.players_in_round and len(game_table.players_in_round) > 1:
            round_action(p)
            send_game_info(game_table.players, game_table.game_info, game_table.pool)
        if all(p.tokens_in_pool == game_table.get_biggest_bet() or p.tokens == 0 for p in
               game_table.players_in_round) and idx >= players_number:
            break


def update_game_players():
    global players_to_remove
    for p in players_to_remove:
        wrapped_msg = wrap_message(DISCONNECT_MESSAGE, None)
        send_pickle(p, wrapped_msg)
        if p in game_table.players:
            game_table.remove_player(p)
        conn = conn_dict.pop(p.id)
        conn.close()
    players_to_remove = []


def engine():
    global players_to_remove
    global conn_dict
    send_game_info(game_table.players, game_table.game_info, game_table.pool)
    while True:
        send_client_data(game_table.players)
        if len(game_table.players) <= 1:
            players_to_remove += game_table.players
            update_game_players()
            break
        print("NEW ROUND")
        game_table.update_players_in_round()
        # tutaj pobieramy small i big blinda od odpowiednich osob, ostatnia osoba w liscie jest dealerem
        game_table.add_to_pool(game_table.get_small_blind(), game_table.players[0])
        game_table.add_to_pool(game_table.get_big_blind(), game_table.players[1])
        # na poczatek zawsze rozdajemy karty graczom
        game_table.deal_cards_players()
        send_client_data(game_table.players)
        send_opponents_data(game_table.players)
        send_game_info(game_table.players, game_table.game_info, game_table.pool)

        if len(game_table.players_in_round) > 1:
            players_number = len(game_table.players)
            for idx, p in enumerate(itertools.cycle(game_table.players), 1):
                if p in game_table.players_in_round and idx != 1 and idx != 2 and len(game_table.players_in_round) > 1:
                    round_action(p)
                    send_game_info(game_table.players, game_table.game_info, game_table.pool)
                if all(p.tokens_in_pool == game_table.get_biggest_bet() or p.tokens == 0 for p in
                       game_table.players_in_round) and idx >= players_number + 2:
                    break

        game_table.deal_flop()
        send_table_cards(game_table.players)
        time.sleep(3)
        if len(game_table.players_in_round) > 1 and any(p.tokens > 0 for p in game_table.players_in_round):
            make_round()

        game_table.deal_turn_river()
        send_table_cards(game_table.players)
        time.sleep(3)
        if len(game_table.players_in_round) > 1 and any(p.tokens > 0 for p in game_table.players_in_round):
            make_round()

        game_table.deal_turn_river()
        send_table_cards(game_table.players)
        time.sleep(3)
        if len(game_table.players_in_round) > 1 and any(p.tokens > 0 for p in game_table.players_in_round):
            make_round()

        send_players_last_round(game_table.players, game_table.players_in_round)
        time.sleep(10)
        winners = game_table.reveal_winners()
        send_who_won(game_table.players, winners)
        # tu nam zwraca liste graczy ktorzy przegrali, tj maja 0 zetonow
        players_to_dc = game_table.new_round()
        players_to_remove += players_to_dc
        update_game_players()

if __name__ == "__main__":
    print("[STARTING] server is starting...")
    LIMIT = int(input("Enter the number of players "))
    start()
    engine()
