class Card:
    SUITS = {
        0: u"\u2664", #spades/wino
        1: u"\u2663", #clubs/trefl
        2: u"\u2666", #diamond
        3: u"\u2665", #hearts
    }

    RANKS = {
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "10",
        11: "J",
        12: "Q",
        13: "K",
        14: "A"
    }

    def __init__(self, rank, suit):
        if rank not in Card.RANKS:
            raise ValueError("Wrong card rank")
        if suit not in Card.SUITS:
            raise ValueError("Wrong card suit")
        self.val = (rank << 2) + suit

    def __str__(self):
        return "({0} , {1})".format(Card.RANKS[self.val >> 2], Card.SUITS[self.val & 3])

    def __repr__(self):
        return "({0} , {1})".format(Card.RANKS[self.val >> 2], Card.SUITS[self.val & 3])

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.val == other.val

    def get_rank(self):
        return self.val >> 2

    def get_suit(self):
        return self.val & 3

    def get_card_in_int(self):
        return self.val

    def get_rank_to_str(self):
        return self.RANKS[self.get_rank()]

    def get_suit_to_str(self):
        return self.SUITS[self.get_suit()]

