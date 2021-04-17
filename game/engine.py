from classes.table import Table
from classes.player import Player
from classes.layouts import *
from classes.game_info import GameInfo
import itertools
import time

#zawsze potrzebny jest stol
game_info = GameInfo(5, 30)
game_room = Table(game_info)
#pierw łaczenie, wymagane 3 graczy aby rozpoczac, wstepne zalozenie, id teraz sa od góry ustawione
p1 = Player(1000, 0, "lolo")
p2 = Player(1000, 1, "koko")
p3 = Player(100, 2, "soso")
p4 = Player(1000, 3, "soso")

game_room.add_player(p1)
game_room.add_player(p2)
game_room.add_player(p3)
game_room.add_player(p4)

def main():
    #start gry, głowna petla odpowiada za rundy
    for i in range(4):
        print("NEW ROUND")
        game_room.update_players_in_round()
        #tutaj pobieramy small i big blinda od odpowiednich osob, ostatnia osoba w liscie jest dealerem
        game_room.add_to_pool(game_room.get_small_blind(), game_room.players[0])
        game_room.add_to_pool(game_room.get_big_blind(), game_room.players[1])
        #na poczatek zawsze rozdajemy karty graczom
        game_room.deal_cards_players()
        #te petle to te rozdania
        if len(game_room.players_in_round) > 1:
            players_number = len(game_room.players)
            for idx, p in enumerate(itertools.cycle(game_room.players), 1):
                if p in game_room.players_in_round and idx != 1 and idx != 2 and len(game_room.players_in_round) > 1:
                    print(p)
                    print(p.tokens_in_pool)
                    what_to_do = input()
                    if what_to_do == "fold":
                        p.fold(game_room)
                    if what_to_do == "raise": #robienie na stole/allin
                        p.raisee(game_room, 100)
                    if what_to_do == "check":
                        p.check()
                    if what_to_do == "call":
                        p.call(game_room)
                if all(p.tokens_in_pool == game_room.get_biggest_bet() or p.tokens == 0 for p in game_room.players_in_round) and idx >= players_number+2:
                    break

        game_room.deal_flop()
        print("AFTER FLOP (3karty pokazane na stole)")
        print(game_room.players_in_round)
        if len(game_room.players_in_round) > 1:
            players_number = len(game_room.players)
            for idx, p in enumerate(itertools.cycle(game_room.players), 1):
                if p in game_room.players_in_round and len(game_room.players_in_round) > 1:
                    print(p)
                    print(p.tokens_in_pool)
                    what_to_do = input()
                    if what_to_do == "fold":
                        p.fold(game_room)
                    if what_to_do == "raise":
                        p.raisee(game_room, 100)
                    if what_to_do == "check":
                        p.check()
                    if what_to_do == "call":
                        p.call(game_room)
                if all(p.tokens_in_pool == game_room.get_biggest_bet() or p.tokens == 0 for p in game_room.players_in_round) and idx >= players_number:
                    break
        game_room.deal_turn_river()
        print("AFTER TURN (kolejna karta na stole)")
        if len(game_room.players_in_round) > 1:
            players_number = len(game_room.players)
            for idx, p in enumerate(itertools.cycle(game_room.players), 1):
                if p in game_room.players_in_round and len(game_room.players_in_round) > 1:
                    print(p)
                    print(p.tokens_in_pool)
                    what_to_do = input()
                    if what_to_do == "fold":
                        p.fold(game_room)
                    if what_to_do == "raise":
                        p.raisee(game_room, 100)
                    if what_to_do == "check":
                        p.check()
                    if what_to_do == "call":
                        p.call(game_room)
                if all(p.tokens_in_pool == game_room.get_biggest_bet() or p.tokens == 0 for p in
                       game_room.players_in_round) and idx >= players_number:
                    break
        game_room.deal_turn_river()
        print("AFTER RIVER (kolejna karta na stole)")
        if len(game_room.players_in_round) > 1:
            players_number = len(game_room.players)
            for idx, p in enumerate(itertools.cycle(game_room.players), 1):
                if p in game_room.players_in_round and len(game_room.players_in_round) > 1:
                    print(p)
                    print(p.tokens_in_pool)
                    what_to_do = input()
                    if what_to_do == "fold":
                        p.fold(game_room)
                    if what_to_do == "raise":
                        p.raisee(game_room, 100)
                    if what_to_do == "check":
                        p.check()
                    if what_to_do == "call":
                        p.call(game_room)
                if all(p.tokens_in_pool == game_room.get_biggest_bet() or p.tokens == 0 for p in
                       game_room.players_in_round) and idx >= players_number:
                    break
        print(game_room.tableCards)
        game_room.reveal_winners()
        print(game_room.players)


        game_room.new_round()



main()