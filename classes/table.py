from Poker.classes.deck import Deck
from Poker.classes.player import Player
from Poker.classes.card import Card
from typing import List
import math

class Table:
    def __init__(self):
        self.deck = Deck()
        self.players: List[Player] = []
        self.pool = 0
        self.tableCards: List[Card] = []

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def add_to_pool(self, tokens, player: Player):
        self.pool += tokens
        player.remove_tokens(tokens)

    def give_prize_tw(self, winnners: List[Player]):
        n = len(winnners)
        tokens_added_bw = sum(winner.tokens_in_pool for winner in winnners)
        for winner in winnners:
            tokens_to_add = math.floor((winner.tokens_in_pool / tokens_added_bw) * self.pool)
            winner.add_tokens(tokens_to_add)

    def deal_cards_players(self):
        for player in self.players:
            cards = self.deck.pop_cards(2)
            player.add_cards(cards)

    def deal_flop(self):
        self.tableCards.extend(self.deck.pop_cards(3))

    def deal_turn_river(self):
        self.tableCards.append(self.deck.pop_card())





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

