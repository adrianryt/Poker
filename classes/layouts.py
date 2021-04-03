from classes.card import Card
from classes.player import Player



def evel_hand(hand):  #7-cards
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
    poker_counter = 1
    res_cards = []
    suits = [[] for _ in range(4)]
    for i in range(0, len(sorted_cards)):
        tmp = suits[sorted_cards[i].get_suit()] # tmp - tablica kart o tym samym kolorze
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


    #looking for Quads
    quads_counter = 1
    res_cards = [sorted_cards[0]]
    quads_value = sorted_cards[0].get_rank()
    for i in range(1, len(sorted_cards)):
        if sorted_cards[i].get_rank() == sorted_cards[i-1].get_rank():
            quads_value = sorted_cards[i].get_rank()
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
            quads_value = sorted_cards[i].get_rank()


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
    suits = [[] for i in range(4)]
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


def solve_draw_straight_flush(players, same_hand_weight_list, players_hands):
    maks_card = -1
    for i in same_hand_weight_list:
        if players_hands[i][0].get_rank() > maks_card:
            maks_card = players_hands[i][0].get_rank()

    return [players[i] for i in same_hand_weight_list if players_hands[i][0].get_rank() == maks_card]

def solve_draw_quads(players, same_hand_weight_list, players_hands):
    maks_card = -1 #ostatnia karta sie liczy
    for i in same_hand_weight_list:
        if players_hands[i][4].get_rank() > maks_card:
            maks_card = players_hands[i][4].get_rank()


    return [players[i] for i in same_hand_weight_list if players_hands[i][4].get_rank() == maks_card]

def solve_draw_full_house(players, same_hand_weight_list, players_hands):
    maks_three_card = -1
    maks_pair_card = -1
    for i in same_hand_weight_list:
        if players_hands[i][0].get_rank() > maks_three_card:
            maks_three_card = players_hands[i][0].get_rank()
            maks_pair_card = players_hands[i][3].get_rank()
        elif players_hands[i][0].get_rank() == maks_three_card:
            if players_hands[i][3].get_rank() > maks_pair_card:
                maks_pair_card = players_hands[i][3].get_rank()

    return [players[i] for i in same_hand_weight_list if players_hands[i][0].get_rank() == maks_three_card and players_hands[i][3].get_rank() == maks_pair_card]

def solve_draw_flush(players, same_hand_weight_list, players_hands):
    maks_card = -1  # ostatnia karta sie liczy
    for i in same_hand_weight_list:
        if players_hands[i][0].get_rank() > maks_card:
            maks_card = players_hands[i][0].get_rank()

    return [players[i] for i in same_hand_weight_list if players_hands[i][0].get_rank() == maks_card]

def solve_draw_straight(players, same_hand_weight_list, players_hands):
    maks_card = -1  #ostatnia karta sie liczy
    for i in same_hand_weight_list:
        if players_hands[i][0].get_rank() > maks_card:
            maks_card = players_hands[i][0].get_rank()

    return [players[i] for i in same_hand_weight_list if players_hands[i][0].get_rank() == maks_card]

def solve_draw_Trips(players, same_hand_weight_list, players_hands):
    maks_tripe_card = -1
    maks_first_greater_card = -1
    maks_second_greater_card = -1
    for i in same_hand_weight_list:
        if players_hands[i][0].get_rank() > maks_tripe_card:
            maks_tripe_card = players_hands[i][0].get_rank()
            maks_first_greater_card = players_hands[i][3].get_rank()
            maks_second_greater_card = players_hands[i][4].get_rank()
        elif players_hands[i][0].get_rank() == maks_tripe_card:
            if players_hands[i][3].get_rank() > maks_first_greater_card:
                maks_first_greater_card = players_hands[i][3].get_rank()
                maks_second_greater_card = players_hands[i][4].get_rank()
            elif players_hands[i][3].get_rank() == maks_first_greater_card:
                if players_hands[i][4].get_rank() > maks_second_greater_card:
                    maks_second_greater_card = players_hands[i][4].get_rank()
    return [players[i] for i in same_hand_weight_list if players_hands[i][0].get_rank() == maks_tripe_card and
            players_hands[i][3].get_rank() == maks_first_greater_card and
            players_hands[i][4].get_rank() == maks_second_greater_card]

def solve_draw_Two_Pairs(players, same_hand_weight_list, players_hands):
    maks_first_pair_card = -1
    maks_second_pair_card = -1
    maks_kicker_card = -1
    for i in same_hand_weight_list:
        if players_hands[i][0].get_rank() > maks_first_pair_card:
            maks_first_pair_card = players_hands[i][0].get_rank()
            maks_second_pair_card = players_hands[i][2].get_rank()
            maks_kicker_card = players_hands[i][4].get_rank()
        elif players_hands[i][0].get_rank() == maks_first_pair_card:
            if players_hands[i][2].get_rank() > maks_second_pair_card:
                maks_second_pair_card = players_hands[i][2].get_rank()
                maks_kicker_card = players_hands[i][4].get_rank()
            elif players_hands[i][2].get_rank() == maks_second_pair_card:
                if players_hands[i][4].get_rank() > maks_kicker_card:
                    maks_kicker_card = players_hands[i][4].get_rank()

    return [players[i] for i in same_hand_weight_list if players_hands[i][0].get_rank() == maks_first_pair_card and
            players_hands[i][3].get_rank() == maks_second_pair_card and
            players_hands[i][4].get_rank() == maks_kicker_card]

def solve_draw_One_Pair(players, same_hand_weight_list, players_hands):
    maks_pair_card = -1
    maks_first_kicker = -1
    maks_second_kicker = -1
    maks_third_kicker = -1
    for i in same_hand_weight_list:
        if players_hands[i][0].get_rank() > maks_pair_card:
            maks_pair_card = players_hands[i][0].get_rank()
            maks_first_kicker = players_hands[i][2].get_rank()
            maks_second_kicker = players_hands[i][3].get_rank()
            maks_third_kicker = players_hands[i][4].get_rank()
        elif players_hands[i][0].get_rank() == maks_pair_card:
            if players_hands[i][2].get_rank() > maks_first_kicker:
                maks_first_kicker = players_hands[i][2].get_rank()
                maks_second_kicker = players_hands[i][3].get_rank()
                maks_third_kicker = players_hands[i][4].get_rank()
            elif players_hands[i][2].get_rank() == maks_first_kicker:
                if players_hands[i][3].get_rank() > maks_second_kicker:
                    maks_second_kicker = players_hands[i][3].get_rank()
                    maks_third_kicker = players_hands[i][4].get_rank()
                elif players_hands[i][3].get_rank() == maks_second_kicker:
                    if players_hands[i][4].get_rank() > maks_third_kicker:
                        maks_third_kicker = players_hands[i][4].get_rank()

    return [players[i] for i in same_hand_weight_list if players_hands[i][0].get_rank() == maks_pair_card and
            players_hands[i][2].get_rank() == maks_first_kicker and
            players_hands[i][3].get_rank() == maks_second_kicker and
            players_hands[i][4].get_rank() == maks_third_kicker]

def get_biggest(same_hand_weight_list, players_hands,n):
    res = -1
    for i in same_hand_weight_list:
        if res < players_hands[i][n].get_rank():
            res = players_hands[i][n].get_rank()
    return res

def solve_draw_biggest_card(players,same_hand_weight_list, players_hands):
    for _ in range(0,5):
        biggest_card = get_biggest(same_hand_weight_list, players_hands, _)
        for i in same_hand_weight_list:
            if players_hands[i][_].get_rank() != biggest_card:
                same_hand_weight_list.remove(i)
    return [players[i] for i in same_hand_weight_list]

def point_the_winner(players, table_cards): #lista graczy(do ich kart odwolujemy sie poprzez player.cards oraz player.get_cards,
    #oraz table_cards - to już jest gotowa lista 3 kart ktore sa na stole czyli działamy na 2 listach

    players_hand_value = []
    players_hands = []
    maks_value = -1

    #print(table_cards + players[j].cards) sprawdzic czy dziala
    for j in range(len(players)):
        tmp = evel_hand(table_cards + players[j].cards)
        players_hands.append(tmp[1])
        players_hand_value.append(tmp[0])

    maks_value = max(players_hand_value)

    if players_hand_value.count(maks_value) == 1:
        return [players[players_hand_value.index(maks_value)]]
    else:
        same_hand_weight_list = []
        #find list of idexes of the list "players" that have the same hand weight
        for _ in range(len(players_hand_value)):
            if players_hand_value[_] == maks_value:
                same_hand_weight_list.append(_)


        #STRAIGHT_FLUSH
        if maks_value == 8:
            return solve_draw_straight_flush(players, same_hand_weight_list, players_hands)

        #quads:
        if maks_value == 7:
            return solve_draw_quads(players, same_hand_weight_list, players_hands)

        #full_house:
        if maks_value == 6:
            return solve_draw_full_house(players, same_hand_weight_list, players_hands)

        #Flush
        if maks_value == 5:
            return solve_draw_flush(players, same_hand_weight_list, players_hands)

        #streight:
        if maks_value == 4:
            return solve_draw_straight(players, same_hand_weight_list, players_hands)

        #Trips
        if maks_value == 3:
            return solve_draw_Trips(players, same_hand_weight_list, players_hands)


        #Double pair
        if maks_value == 2:
            return solve_draw_Two_Pairs(players,same_hand_weight_list,players_hands)


        #pair
        if maks_value == 1:
            return solve_draw_One_Pair(players, same_hand_weight_list, players_hands)

        # biggest card
        if maks_value == 0:
            return solve_draw_biggest_card(players,same_hand_weight_list, players_hands)



if __name__ == "__main__":

    card1 = Card(14, 1)
    card2 = Card(13, 0)
    card3 = Card(11, 3)
    card4 = Card(8, 1)
    card5 = Card(10, 2)


    card6 = Card(6, 1)
    card7 = Card(2, 2)
    card8 = Card(6,1)
    card9 = Card(9,2)
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
    print(evel_hand(players[0].cards + table))
    print(evel_hand(players[1].cards + table))

    res1 = evel_hand(players[0].cards + table)
    res = point_the_winner(players, table)
    for i in range(len(res)):
        print(res[i])

    #poker(players[1].cards + table)

