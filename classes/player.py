from classes.card import Card


class Player:
    def __init__(self, tokens, id, name):
        self.tokens = tokens
        self.tokens_in_pool = 0
        self.id = id
        self.name = name
        self.cards = []

    def add_tokens(self, tokens):
        self.tokens += tokens

    def remove_tokens(self, tokens):
        self.tokens -= tokens
        self.tokens_in_pool += tokens

    def add_cards(self, cards):
        self.cards.extend(cards)

    def remove_cards(self):
        self.cards.clear()

    def get_cards(self):
        if len(self.cards) == 1:
            return self.cards[0], "None"
        if len(self.cards) < 2:
            return "None", "None"
        return self.cards[0], self.cards[1]

    def __repr__(self):
        return "(Name: {0}, Id: {1}, Tokens: {2}, Cards: {3} {4})".format(self.name, self.id, self.tokens,
                                                                           self.get_cards()[0], self.get_cards()[1])
    def __str__(self):
        return "(Name: {0}, Id: {1}, Tokens: {2}, Cards: {3} {4})".format(self.name, self.id, self.tokens,
                                                                           self.get_cards()[0], self.get_cards()[1])


if __name__ == "__main__":
    player1 = Player(1000, 1, "lololo")
    player1.add_cards([Card(5, 2)])
    print(player1)

