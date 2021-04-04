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

game_room.add_player(p1)
game_room.add_player(p2)
game_room.add_player(p3)


#start gry, głowna petla odpowiada za rundy
for i in range(4):
    print("NEW ROUND")
    players_left_in_round = game_room.players.copy()
    #tutaj pobieramy small i big blinda od odpowiednich osob
    game_room.add_to_pool(small_blind, game_room.players[-2])
    game_room.add_to_pool(big_blind, game_room.players[-1])
    #na poczatek zawsze rozdajemy karty graczom
    game_room.deal_cards_players()
    #te petle to te rozdania
    # while len(players_left_in_round) > 1:
    #     pass
    game_room.deal_flop()
    # while len(players_left_in_round) > 1:
    #     pass
    game_room.deal_turn_river()
    # while len(players_left_in_round) > 1:
    #     pass
    game_room.deal_turn_river()
    # while len(players_left_in_round) > 1:
    #     pass
    for p in game_room.players:
        print(p)
    winners = point_the_winner(players_left_in_round, game_room.tableCards)
    game_room.give_prize_tw(winners)
    print("--------------")
    print(winners)
    for p in game_room.players:
        print(p)

    # players_in_round = game_room.players.copy()
    # for idx, element in enumerate(itertools.cycle(game_room.players)):
    #     if element in players_in_round:
    #         print(idx, element)
    #         print(players_in_round)
    #         if idx == 5: players_in_round.pop()
    #         time.sleep(1)

    #po ustaleniu zwyciezcy wszyscy gracze zwracaja karty, ze stolu tez znikaja
    game_room.remove_cards_players()
    game_room.remove_cards_table()
    game_room.deck.push_cards()
    biggest_bet = big_blind
    #tu kod na usuniecie z gry
    game_room.move_dealer()

    time.sleep(5)
