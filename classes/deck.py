import random
from classes.card import Card


class Deck:
    def __init__(self):
        self.deck = [Card(rank, suit) for rank in range(2, 15) for suit in range(0, 4)]
        self.popped_cards = []
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def pop_card(self):
        card = self.deck.pop()
        self.popped_cards.append(card)
        return card

    def pop_cards(self, n):
        cards = []
        for _ in range(n):
            cards.append(self.pop_card())
        return cards

    def push_cards(self):
        self.deck.extend(self.popped_cards)
        self.popped_cards.clear()
        self.shuffle()



if __name__ == "__main__":
    deck = Deck()
    card = deck.pop_card()
    print(len(deck.deck))
    deck.push_cards()
    print(len(deck.deck))









