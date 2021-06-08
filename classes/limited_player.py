from classes.player import Player

class LimitedPlayer:
    def __init__(self, player):
        self.tokens = player.tokens
        self.tokens_in_pool = player.tokens_in_pool
        self.id = player.id
        self.name = player.name

    def __repr__(self):
        return "(Name: {0}, Id: {1}, Tokens: {2})".format(self.name, self.id, self.tokens)
    def __str__(self):
        return "(Name: {0}, Id: {1}, Tokens: {2})".format(self.name, self.id, self.tokens)

if __name__ == "__main__":
    player1 = Player(1000, 1, "lololo")
    player2 = LimitedPlayer(player1)
    print(player2)