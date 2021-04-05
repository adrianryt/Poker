from classes.table import Table
from classes.player import Player
from classes.layouts import *
import itertools
import time

#zawsze potrzebny jest stol
game_room = Table()
#moze dodac te dane do table jako osobna klase
time_in_round = 30
small_blind = 5
big_blind = small_blind * 2
biggest_bet = big_blind
#pierw łaczenie, wymagane 3 graczy aby rozpoczac, wstepne zalozenie, id teraz sa od góry ustawione
p1 = Player(1000, 0, "lolo")
p2 = Player(1000, 1, "koko")
p3 = Player(1000, 2, "soso")
p4 = Player(1000, 3, "soso")

game_room.add_player(p1)
game_room.add_player(p2)
game_room.add_player(p3)
game_room.add_player(p4)

def check(player):
    global biggest_bet
    game_room.add_to_pool(biggest_bet - player.tokens_in_pool, player)


def raisee(player):
    global biggest_bet
    #narazie na sztywno podbicie jest zawsze o 10
    game_room.add_to_pool(10, player)
    biggest_bet += 10


def fold(player, players_left):
    players_left.remove(player)
    return players_left

def main():
    global biggest_bet
    #start gry, głowna petla odpowiada za rundy
    for i in range(4):
        print("NEW ROUND")
        players_left_in_round = game_room.players.copy()
        #tutaj pobieramy small i big blinda od odpowiednich osob, ostatnia osoba w liscie jest dealerem
        game_room.add_to_pool(small_blind, game_room.players[0])
        game_room.add_to_pool(big_blind, game_room.players[1])
        #na poczatek zawsze rozdajemy karty graczom
        game_room.deal_cards_players()
        #te petle to te rozdania
        if len(players_left_in_round) > 1:
            players_number = len(players_left_in_round)
            for idx, p in enumerate(itertools.cycle(game_room.players), 1):
                if p in players_left_in_round and idx != 1 and idx != 2:
                    print(p)
                    print(p.tokens_in_pool)
                    what_to_do = input()
                    if what_to_do == "fold":
                        players_left_in_round = fold(p, players_left_in_round)
                    if what_to_do == "raise":
                        raisee(p)
                    if what_to_do == "check":
                        check(p)
                if all(p.tokens_in_pool == biggest_bet for p in players_left_in_round) and idx >= players_number+2:
                    break

        game_room.deal_flop()
        print("AFTER FLOP (3karty pokazane na stole)")
        if len(players_left_in_round) > 1:
            players_number = len(players_left_in_round)
            for idx, p in enumerate(itertools.cycle(game_room.players), 1):
                if p in players_left_in_round:
                    print(p)
                    print(p.tokens_in_pool)
                    what_to_do = input()
                    if what_to_do == "fold":
                        players_left_in_round = fold(p, players_left_in_round)
                    if what_to_do == "raise":
                        raisee(p)
                    if what_to_do == "check":
                        check(p)
                if all(p.tokens_in_pool == biggest_bet for p in players_left_in_round) and idx >= players_number:
                    break
        game_room.deal_turn_river()
        print("AFTER TURN (kolejna karta na stole)")
        print(players_left_in_round)
        if len(players_left_in_round) > 1:
            players_number = len(players_left_in_round)
            for idx, p in enumerate(itertools.cycle(game_room.players), 1):
                if p in players_left_in_round:
                    print(p)
                    print(p.tokens_in_pool)
                    what_to_do = input()
                    if what_to_do == "fold":
                        players_left_in_round = fold(p, players_left_in_round)
                    if what_to_do == "raise":
                        raisee(p)
                    if what_to_do == "check":
                        check(p)
                if all(p.tokens_in_pool == biggest_bet for p in players_left_in_round) and idx >= players_number:
                    break
        game_room.deal_turn_river()
        print("AFTER RIVER (kolejna karta na stole)")
        if len(players_left_in_round) > 1:
            players_number = len(players_left_in_round)
            for idx, p in enumerate(itertools.cycle(game_room.players), 1):
                if p in players_left_in_round:
                    print(p)
                    print(p.tokens_in_pool)
                    what_to_do = input()
                    if what_to_do == "fold":
                        players_left_in_round = fold(p, players_left_in_round)
                    if what_to_do == "raise":
                        raisee(p)
                    if what_to_do == "check":
                        check(p)
                if all(p.tokens_in_pool == biggest_bet for p in players_left_in_round) and idx >= players_number:
                    break
        for p in players_left_in_round:
            print(p)

        winners = point_the_winner(players_left_in_round, game_room.tableCards)
        game_room.give_prize_tw(winners)
        print("--------------")
        print(winners)


        #po ustaleniu zwyciezcy wszyscy gracze zwracaja karty, ze stolu tez znikaja
        #ta funkcja usuwa karty i zetony z puli kazdego gracza
        game_room.remove_cards_players()
        game_room.remove_cards_table()
        game_room.deck.push_cards()
        biggest_bet = big_blind
        #tu kod na usuniecie z gry
        game_room.move_dealer()



main()