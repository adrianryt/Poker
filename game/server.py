import socket
import threading
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

game_info = GameInfo(10,30)
game_table = Table(game_info)
conn_dict = {}
players_to_remove = []

LIMIT = int(input("Podaj liczbe graczy"))

def recive(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            #conn.send("Leaving message".encode(FORMAT))
            # print("Server: Dostałem DISCONNECT message od: ",conn)
            #przydolby sie usuwac z dicta rozlaczonego gracza
            idx = None
            p = None
            for key, val in conn_dict.items():
                if(val == conn):
                    idx = key
                    print("IDX TO REMOVE: ", idx)
            for player in game_table.players:
                if player.id == idx:
                    p = player
            print("Player to remove: ", p)
            players_to_remove.append(p)
            print("players to remove: ", players_to_remove)
            #game_table.players_in_round.remove(p)
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


def wrap_message(type, msg): #string oraz coś co chcemy do message włożyć
    result = (type, msg)
    return result

def send_pickle(player,msg): #(do kogo, co)
    #bin = recive(conn_dict[player.id])
    msg_to_client = pickle.dumps(msg)
    msg_to_client = bytes(f'{len(msg_to_client):<{HEADER}}', "utf-8") + msg_to_client
    conn_dict[player.id].send(msg_to_client)

def sendCardsOnTable(players):
    for p in players:
        #send(conn_dict[p.id], "CARDS")
        #send_pickle(p,game_table.tableCards) #do kogo oraz co wysyłamy
        wrapped_msg = wrap_message("CARDS", game_table.tableCards)
        send_pickle(p, wrapped_msg)

def sendClientData(players):
    for p in players:
        #send(conn_dict[p.id], "YOUR PLAYER")
        #send_pickle(p, p)
        wrapped_msg = wrap_message("YOUR PLAYER", p)
        send_pickle(p, wrapped_msg)

def sendDataToRivals(players, client):
    rivals = [p for p in players if p.id != client.id]
    for r in rivals:
        #send(conn_dict[r.id], "OPPONENT")
        tmp = LimitedPlayer(client)
        wrapped_msg = wrap_message("OPPONENT", tmp)
        #send_pickle(r,tmp)
        send_pickle(r, wrapped_msg)

#TODO chyba nie jest to potrzebne
def sendWhoWon(players, winners):
    tmp =[]
    for winner in winners:
        tmp.append(LimitedPlayer(winner))
    for p in players:
        wrapped_msg = wrap_message("WINNERS", tmp)
        send_pickle(p, wrapped_msg)

def sendRivalsData(players):
    players_dict = {}
    for player in players:
        players_dict[player.id] = LimitedPlayer(player)

    for player in players:
        players_dict.pop(player.id)
        wrapped_msg = wrap_message("OPPONENTS",players_dict)
        send_pickle(player, wrapped_msg)
        players_dict[player.id] = LimitedPlayer(player)

#TODO zmienic nazwe narazie nie mam pomyslu, to wysylamy po ostatniej rundzie
def sendPlayersLastRound(allPlayers, playersActive):
    if len(playersActive) > 1:
        for all_p in allPlayers:
            for p_a in playersActive:
                if p_a != all_p:

                    wrapped_msg = wrap_message("OPPONENT", p_a)
                    send_pickle(all_p, wrapped_msg)

def send_game_info(all_players,info, tokens_pool):
    game_info = wrap_message("GAME INFO", info)
    pool = wrap_message("POOL", tokens_pool)
    for p in all_players:
        send_pickle(p, game_info)
        send_pickle(p, pool)

def round_action(p):
    #send(conn_dict[p.id], "CHOOSE MOVE")
    wrapped_msg = wrap_message("CHOOSE MOVE", p)
    send_pickle(p, wrapped_msg)
    #on tutaj czeka na odpowiedz - czyli na klikniecie buttona
    # print("CONN_DICT ID:",conn_dict[p.id])
    what_to_do = recive(conn_dict[p.id])
    # print("What to do",what_to_do)
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
    else: #to dla !DISCONNECT
        p.fold(game_table)

    sendClientData([p])  # po to zeby klient mial pewnosc co zrobil, znikna mu wtedy zetony np.
    sendDataToRivals(game_table.players, p)

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
    print(conn_dict)
    print("USUWAM GRACZY Z LISTY")
    for p in players_to_remove:
        wrapped_msg = wrap_message(DISCONNECT_MESSAGE, None)
        send_pickle(p, wrapped_msg)
        if p in game_table.players:
            game_table.remove_player(p)
        conn = conn_dict.pop(p.id)
        conn.close()
        print(p)
    players_to_remove = []

def engine():
    #TODO te globale to wywalic trzeba, latwiej bedzie chyba na klase to jebnac, lub przekazywac odpowiedznie dane do funkcji bo chuj wi co sie dzieje
    global players_to_remove
    global conn_dict
    send_game_info(game_table.players, game_table.game_info, game_table.pool)
    while True:
        sendClientData(game_table.players)
        if(len(game_table.players) <= 1):
            #TODO TUTAJ JAK ZOSTANIE JEDNA OSOBA TO TRZEBA JA ROZLACZYC
            for p in game_table.players:
                wrapped_msg = wrap_message("GAME ENDED", None)
                send_pickle(p, wrapped_msg)
                conn = conn_dict.pop(p.id)
                conn.close()
            break
        print("NEW ROUND")
        game_table.update_players_in_round()
        # tutaj pobieramy small i big blinda od odpowiednich osob, ostatnia osoba w liscie jest dealerem
        game_table.add_to_pool(game_table.get_small_blind(), game_table.players[0])
        game_table.add_to_pool(game_table.get_big_blind(), game_table.players[1])
        # na poczatek zawsze rozdajemy karty graczom
        game_table.deal_cards_players()
        sendClientData(game_table.players)
        sendRivalsData(game_table.players)
        send_game_info(game_table.players, game_table.game_info, game_table.pool)
        # te petle to te rozdania
        if len(game_table.players_in_round) > 1:
            players_number = len(game_table.players)
            for idx, p in enumerate(itertools.cycle(game_table.players), 1):
                if p in game_table.players_in_round and idx != 1 and idx != 2 and len(game_table.players_in_round) > 1:
                   round_action(p)
                   send_game_info(game_table.players, game_table.game_info, game_table.pool)
                if all(p.tokens_in_pool == game_table.get_biggest_bet() or p.tokens == 0 for p in
                       game_table.players_in_round) and idx >= players_number + 2:
                    break


        # print("AFTER FLOP (3karty pokazane na stole)")
        game_table.deal_flop()
        sendCardsOnTable(game_table.players)
        time.sleep(3)
        # print(game_table.players_in_round)
        if len(game_table.players_in_round) > 1 and any(p.tokens > 0 for p in game_table.players_in_round):
            make_round()

        # print("AFTER TURN (kolejna karta na stole)")
        game_table.deal_turn_river()
        sendCardsOnTable(game_table.players)
        time.sleep(3)
        if len(game_table.players_in_round) > 1 and any(p.tokens > 0 for p in game_table.players_in_round):
           make_round()

        # print("AFTER RIVER (kolejna karta na stole)")
        game_table.deal_turn_river()
        sendCardsOnTable(game_table.players)
        time.sleep(3)
        if len(game_table.players_in_round) > 1 and any(p.tokens > 0 for p in game_table.players_in_round):
            make_round()

        sendPlayersLastRound(game_table.players, game_table.players_in_round)
        time.sleep(5)
        winners = game_table.reveal_winners()
        # print(winners, "DDDDDDD")
        sendWhoWon(game_table.players, winners)
        #TODO delete this
        time.sleep(4)
        #tu nam zwraca liste graczy ktorzy przegrali, tj maja 0 zetonow
        players_to_dc = game_table.new_round()
        print(game_table.players, "PLAYERS")
        ##TODO stworzyc z tego funkcje
        for p in players_to_dc:
            wrapped_msg = wrap_message("GAME ENDED", None)
            send_pickle(p, wrapped_msg)
            conn = conn_dict.pop(p.id)
            conn.close()
        update_game_players()



if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()
    engine()
