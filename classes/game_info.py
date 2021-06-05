class GameInfo:
    def __init__(self, small_blind, decision_time):
        self.small_blind = small_blind
        self.big_blind = 2 * small_blind
        self.biggest_bet = self.big_blind
        self.decision_time = decision_time

    def increase_blinds(self, new_val):
        self.small_blind = new_val
        self.big_blind = 2 * self.small_blind

    # new_b_b - new_biggest_blind
    def update_b_b(self, new_b_b):
        if new_b_b > self.biggest_bet:
            self.biggest_bet = new_b_b

    def clear_b_b(self):
        self.biggest_bet = self.big_blind
