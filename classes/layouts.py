from classes.card import Card
from classes.player import Player


# strit od asa do 5 w kolorze
def straight_flush_A_5(hand):
    suits = [[] for _ in range(4)]
    for c in hand:
        suits[c.get_suit()].append(c)
    for suited_cards in suits:
        if len(suited_cards) >= 5 and straight_A_5(suited_cards):
            return straight_A_5(suited_cards)
    return False


# strit od asa do 5
def straight_A_5(hand):
    ranks = [x.get_rank() for x in hand]
    if 5 in ranks and 4 in ranks and 3 in ranks and 2 in ranks and 14 in ranks:
        result = [card for card in hand if card.get_rank() == 5 or card.get_rank() == 4 or card.get_rank() == 3
                  or card.get_rank() == 2 or card.get_rank() == 14]
        result = list({card.get_rank(): card for card in result}.values())
        result = sorted([cards for cards in result], key=lambda cards: cards.get_rank(), reverse=True)
        ace = result.pop(0)
        result.append(ace)
        return result
    return False

def evaluate_hand(hand):  #7-cards
    NO_PAIR = 0
    PAIR = 1
    TWO_PAIR = 2
    TRIPS = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    QUADS = 7
    STRAIGHT_FLUSH = 8
    sorted_cards = sorted([cards for cards in hand], key=lambda cards: cards.get_suit(), reverse=True)
    sorted_cards = sorted([cards for cards in sorted_cards], key=lambda cards: cards.get_rank(), reverse=True)
    values = sorted([c.get_rank() for c in hand], reverse=True)

    #looking for poker
    res_cards = []
    suits = [[] for _ in range(4)]
    for i in range(0, len(sorted_cards)):
        tmp = suits[sorted_cards[i].get_suit()] #tmp - tablica kart o tym samym kolorze
        tmp.append(sorted_cards[i])
        if len(tmp) >= 5:
            res_cards = [tmp[0]]
            for j in range(1, len(suits[sorted_cards[i].get_suit()])):
                if tmp[j].get_rank() == tmp[j - 1].get_rank() - 1:
                    res_cards.append(tmp[j])
                    if len(res_cards) == 5:
                        return STRAIGHT_FLUSH, res_cards
                elif tmp[j].get_rank() != tmp[j - 1].get_rank():
                    res_cards = [suits[sorted_cards[i].get_suit()][j]]

    #looking for straight_flush from 5 to A
    if straight_flush_A_5(sorted_cards):
        return STRAIGHT_FLUSH, straight_flush_A_5(sorted_cards)

    #looking for Quads
    quads_counter = 1
    res_cards = [sorted_cards[0]]
    for i in range(1, len(sorted_cards)):
        if sorted_cards[i].get_rank() == sorted_cards[i-1].get_rank():
            quads_counter+=1
            res_cards.append(sorted_cards[i])
            if(quads_counter == 4):
                for card in sorted_cards:
                    if card not in res_cards:
                        res_cards.append(card)
                        break
                return QUADS, res_cards
        else:
            quads_counter = 1
            res_cards = [sorted_cards[i]]

    pairs = []
    three_same_valued_cards = False
    value_of_three = None
    value_set = sorted(set(values), reverse=True)
    for v in value_set:
        if values.count(v) == 3 and not three_same_valued_cards:
            three_same_valued_cards = True
            value_of_three = v
        elif values.count(v) >= 2:
            pairs.append(v)

    #looking for full
    if three_same_valued_cards and len(pairs) > 0:
        res_cards = []
        for card in sorted_cards:
            if card.get_rank() == value_of_three:
                res_cards.append(card)
        for card in sorted_cards:
            if card.get_rank() == max(pairs) and len(res_cards)<5:
                res_cards.append(card)

        return FULL_HOUSE, res_cards

    # looking for flush
    suits = [[] for _ in range(4)]
    for c in sorted_cards:
        suits[c.get_suit()].append(c)
        if len(suits[c.get_suit()]) == 5:
            return FLUSH, suits[c.get_suit()]

    # looking for straight
    straight_counter = 1
    res_cards = [sorted_cards[0]]
    for i in range(1, len(sorted_cards)):
        if sorted_cards[i].get_rank() == sorted_cards[i-1].get_rank() - 1:
            straight_counter += 1
            res_cards.append(sorted_cards[i])
            if straight_counter == 5:
                return STRAIGHT, res_cards
        elif sorted_cards[i].get_rank() != sorted_cards[i-1].get_rank():
            straight_counter = 1
            res_cards = [sorted_cards[i]]

    if straight_A_5(sorted_cards):
        return STRAIGHT, straight_A_5(sorted_cards)

    #looking for TRIPS
    if three_same_valued_cards:
        res_cards = []
        for card in sorted_cards:
            if card.get_rank() == value_of_three:
                res_cards.append(card)
        for card in sorted_cards:
            if card not in res_cards:
                res_cards.append(card)
                if len(res_cards) == 5: break
        return TRIPS, res_cards

    if len(pairs) >= 2:
        res_cards = []
        for card in sorted_cards:
            if card.get_rank() == pairs[0]:
                res_cards.append(card)
        for card in sorted_cards:
            if card.get_rank() == pairs[1]:
                res_cards.append(card)
        for card in sorted_cards:
            if card not in res_cards:
                res_cards.append(card)
                break
        return TWO_PAIR, res_cards

    if len(pairs) == 1:
        res_cards = []
        for card in sorted_cards:
            if card.get_rank() == pairs[0]:
                res_cards.append(card)
        for card in sorted_cards:
            if card not in res_cards:
                res_cards.append(card)
                if(len(res_cards) == 5): break
        return PAIR, res_cards

    return NO_PAIR, [x for x in sorted_cards[0:5]]

def get_biggest_rank(players_hands, n):
    res = -1
    for hand in players_hands:
        if res < hand[n].get_rank():
            res = hand[n].get_rank()
    return res

def solve_draw(players, players_hands):
    winning_players = players.copy()
    winning_hands = players_hands.copy()
    for i in range(5):
        biggest_rank = get_biggest_rank(players_hands, i)
        for player, hand in list(zip(winning_players, winning_hands)):
            if hand[i].get_rank() != biggest_rank:
                players_hands.remove(hand)
                players.remove(player)
        winning_hands = players_hands.copy()
        winning_players = players.copy()
    return winning_players

def point_the_winner(players, table_cards):
    n = len(players)
    players_hand_value = []
    players_hands = []

    for j in range(n):
        tmp = evaluate_hand(table_cards + players[j].cards)
        players_hands.append(tmp[1])
        players_hand_value.append(tmp[0])
    maks_value = max(players_hand_value)

    if players_hand_value.count(maks_value) == 1:
        return [players[players_hand_value.index(maks_value)]]
    else:
        same_hand_weight_list = []
        #find list of idexes of the list "players" that have the same hand weight
        for i in range(len(players_hand_value)):
            if players_hand_value[i] == maks_value:
                same_hand_weight_list.append(i)

        players_same_weight = []
        players_hands_same_weight = []
        for i in same_hand_weight_list:
            players_same_weight.append(players[i])
            players_hands_same_weight.append(players_hands[i])

        return solve_draw(players_same_weight, players_hands_same_weight)

if __name__ == "__main__":
    card1 = Card(14, 1)
    card2 = Card(2, 1)
    card3 = Card(3, 1)
    card4 = Card(9, 1)
    card5 = Card(2, 2)

    card6 = Card(4, 1)
    card7 = Card(5, 1)
    card8 = Card(4,3)
    card9 = Card(5,2)
    player1 = Player(100, 0, "lolo")
    player2 = Player(100, 1, "soso")

    player1.add_cards([card6, card7])
    player2.add_cards([card8, card9])
    players = [player1,player2]
    table = []
    table.append(card1)
    table.append(card2)
    table.append(card3)
    table.append(card4)
    table.append(card5)
    print(evaluate_hand(players[0].cards + table))
    print(evaluate_hand(players[1].cards + table))

    res1 = evaluate_hand(players[0].cards + table)
    res = point_the_winner(players, table)
    for i in range(len(res)):
        print(res[i])





