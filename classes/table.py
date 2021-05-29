from classes.deck import Deck
from classes.player import Player
from classes.card import Card
from classes.game_info import GameInfo
from classes.layouts import *
from typing import List
import math

class Table:
    def __init__(self, game_info):
        self.deck = Deck()
        self.players: List[Player] = []
        self.pool = 0
        self.tableCards: List[Card] = []
        self.players_in_round: List[Player] = []
        self.players_lost: List[Player] = []
        self.game_info: GameInfo = game_info


    def get_small_blind(self):
        return self.game_info.small_blind

    def get_big_blind(self):
        return self.game_info.big_blind

    def get_biggest_bet(self):
        return self.game_info.biggest_bet

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def remove_players(self):
        players_to_disconnect = []
        for p in self.players:
            if p.tokens == 0:
                players_to_disconnect.append(p)
                self.remove_player(p)
        return players_to_disconnect



    #every new round
    def update_players_in_round(self):
        self.players_in_round = self.players.copy()

    def add_to_pool(self, tokens, player: Player):
        self.pool += tokens
        player.remove_tokens(tokens)

    def give_prize_tw(self, winnners: List[Player], curr_pool):
        for winner in winnners:
            tokens_to_add = math.floor((1/len(winnners)) * curr_pool)
            winner.add_tokens(tokens_to_add)
        self.pool -= curr_pool


    def reveal_winners(self):
        winners = []
        while self.pool > 0:
            minimal_bet = min([p.tokens_in_pool for p in self.players_in_round])
            current_pool = 0
            for p in self.players:
                if p.tokens_in_pool > minimal_bet:
                    current_pool += minimal_bet
                    p.tokens_in_pool -= minimal_bet
                else:
                    current_pool += p.tokens_in_pool
                    p.tokens_in_pool = 0
                print(p, current_pool)
            winners += point_the_winner(self.players_in_round, self.tableCards)
            print(winners)
            self.give_prize_tw(winners, current_pool)
            self.players_in_round = [p for p in self.players_in_round if p.tokens_in_pool > 0]
            #print(self.players_in_round)
            #print(self.pool)
        return winners



    def deal_cards_players(self):
        for player in self.players:
            cards = self.deck.pop_cards(2)
            player.add_cards(cards)

    #przy usuwaniu kart trzeba wyzerowac tokens_in_pool
    def remove_cards_players(self):
        for player in self.players:
            player.remove_cards()
            player.tokens_in_pool = 0

    def deal_flop(self):
        self.tableCards.extend(self.deck.pop_cards(3))

    def deal_turn_river(self):
        self.tableCards.append(self.deck.pop_card())

    def remove_cards_table(self):
        self.tableCards.clear()

    def move_dealer(self):
        tmp = self.players.pop(0)
        self.players.append(tmp)

    def new_round(self):
        self.remove_cards_players()
        self.remove_cards_table()
        self.deck.push_cards()
        self.game_info.clear_b_b()
        players_to_disconnect = self.remove_players()
        self.move_dealer()
        return players_to_disconnect





if __name__ == "__main__":
    table = Table()
    p1 = Player(1000, 1, "lolo")
    p2 = Player(1000, 2, "lppl")
    p3 = Player(1000, 3, "fdf")
    table.add_player(p1)
    table.add_player(p2)
    table.add_player(p3)
    table.deal_cards_players()
    table.add_to_pool(10, p1)
    table.add_to_pool(50, p2)
    table.add_to_pool(50,p3)
    print(p1)
    print(p2)
    print(p3)
    table.deal_flop()
    print(table.tableCards)
    table.give_prize_tw([p1,p2])
    print(p1)
    print(p2)
    print(p3)
    print(len(table.deck.deck))

