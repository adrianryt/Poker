from classes.card import Card

class Player:
    def __init__(self, tokens, id, name):
        if tokens <= 0:
            raise ValueError("Tokens must be greater than 0")
        self._tokens = tokens
        self.tokens_in_pool = 0
        self.id = id
        self.name = name
        self.cards = []

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, new_tokens):
        if new_tokens < 0:
            raise ValueError("Tokens must be positive")
        else:
            self._tokens = new_tokens

    def add_tokens(self, tokens):
        if tokens <= 0:
            raise ValueError("Tokens must be positive")
        self.tokens += tokens

    def remove_tokens(self, tokens):
        if tokens > self.tokens:
            raise ValueError("Can't remove more tokens than you have")
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

    def check(self):
        pass

    def call(self, table):
        tokens_to_add = table.game_info.biggest_bet - self.tokens_in_pool
        table.add_to_pool(tokens_to_add, self)
        return tokens_to_add

    def raisee(self, table, tokens):
        self.call(table)
        table.add_to_pool(tokens, self)
        table.game_info.update_b_b(self.tokens_in_pool)

    def fold(self, table):
        table.players_in_round.remove(self)

    def all_in(self, table):
        self.call(table)
        self.raisee(table, self.tokens)

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

