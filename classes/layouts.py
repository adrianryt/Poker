from classes.card import Card


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

    sorted_cards = sorted([cards for cards in hand], key=lambda cards: cards.get_rank(), reverse=True)
    values = sorted([c.get_rank() for c in hand], reverse=True)

    #looking for poker
    poker_counter = 1
    res_cards = [sorted_cards[0]]
    for i in range(1, len(sorted_cards)):
        if sorted_cards[i].get_rank() == sorted_cards[i-1].get_rank() -1 and sorted_cards[i].get_suit() == sorted_cards[i-1].get_suit():
            poker_counter += 1
            res_cards.append(sorted_cards[i])
            if poker_counter == 5:
                return STRAIGHT_FLUSH, res_cards
        elif sorted_cards[i].get_rank() != sorted_cards[i-1].get_rank():
            poker_counter = 1
            res_cards = [sorted_cards[i]]

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
        print("FULL")
        res_cards = []
        for card in sorted_cards:
            if card.get_rank() == value_of_three:
                res_cards.append(card)
        for card in sorted_cards:
            if card.get_rank() == max(pairs):
                res_cards.append(card)

        return FULL_HOUSE, res_cards

    # looking for flush
    suits = [[] for i in range(4)]
    for c in sorted_cards:
        suits[c.get_suit()].append(c)
    for s in suits:
        if len(s) == 5:
            return FLUSH, s

    # looking for straight
    straight_counter = 1
    res_cards = [sorted_cards[0]]
    straight_max_value = values[0]
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



def point_the_winner(players, table_cards): #lista graczy(do ich kart odwolujemy sie poprzez player.cards oraz player.get_cards,
    #oraz table_cards - to już jest gotowa lista 3 kart ktore sa na stole czyli działamy na 2 listach

    players_hand_value = []
    maks_value = -1

    #print(table_cards + players[j].cards) sprawdzic czy dziala
    for j in range(len(players)):
        players_hand_value.append(evel_hand(table_cards + players[j].cards)[0])

    maks_value = max(players_hand_value)

    if(players_hand_value.count(maks_value) == 1):
        return players[players_hand_value.index(maks_value)]
    else:
        same_hand_weight_list = []
        #find list of idexes of the list "players" that have the same hand weight
        for _ in range(len(players_hand_value)):
            if players_hand_value(_) == maks_value:
                same_hand_weight_list.append(_)


        #STRAIGHT_FLUSH
        if maks_value == 7:
            winner = None
            maks_card = -1

        #quads:
        if maks_value == 7:
            winner = None
            maks_card = -1
            for i in same_hand_weight_list:
                if evel_hand(players[i].cards + table_cards)[1] > maks_card:
                    maks_card = evel_hand(players[i].cards + table_cards)[1]
                    winner = i
            res = []
            res.append(players[winner])
            return res

        #flush:
        if maks_value == 6:
            res = []
            for i in same_hand_weight_list:
                res.append(players[i])
            return res

        #Full House
        if maks_value == 5:
            winner = None
            maks_three_card = -1
            maks_pair_card = -1
            for i in same_hand_weight_list:
                if evel_hand(players[i].cards + table_cards)[1] > maks_three_card:
                    maks_three_card = evel_hand(players[i].cards + table_cards)[1]
                    maks_pair_card = evel_hand(players[i].cards + table_cards)[2]
                    winner = i
                elif evel_hand(players[i].cards + table_cards)[1] == maks_three_card:
                    if evel_hand(players[i].cards + table_cards)[2] > maks_pair_card:
                        maks_pair_card = evel_hand(players[i].cards + table_cards)[2]
                        winner = i
            res = []
            res.append(players[winner])
            return res
            return players[winner].id

        #streight: #NIE ZROBIONE DO KONCA
        if maks_value == 4:
            winner = None
            maks_card = -1
            for i in same_hand_weight_list:
                if evel_hand(players[i].cards + table_cards)[1] > maks_card:
                    maks_card = evel_hand(players[i].cards + table_cards)[1]
                    winner = i
            return players[winner].id
        #Trips #Nie zrobione do końca
        if maks_value == 3:
            winner = None
            maks_card = -1
            for i in same_hand_weight_list:
                if evel_hand(players[i].cards + table_cards)[1] > maks_card:
                    maks_card = evel_hand(players[i].cards + table_cards)[1]
                    winner = i
            return players[winner].id

        #Double pair #Nie zrobione do Końca
        if maks_value == 2:
            winner = None
            maks_stronger_pair = -1
            maks_weaker_pair = -1
            for i in same_hand_weight_list:
                if evel_hand(players[i].cards + table_cards)[1] > maks_stronger_pair:
                    maks_stronger_pair = evel_hand(players[i].cards + table_cards)[1]
                    maks_weaker_pair = evel_hand(players[i].cards + table_cards)[2]
                    winner = i
                elif evel_hand(players[i].cards + table_cards)[1] == maks_stronger_pair:
                    if evel_hand(players[i].cards + table_cards)[2] > maks_weaker_pair:
                        maks_weaker_pair = evel_hand(players[i].cards + table_cards)[2]
                        winner = i
            return players[winner].id

        #pair
        if maks_value == 1:
            winner = None
            maks_card = -1
            for i in same_hand_weight_list:
                if evel_hand(players[i].cards + table_cards)[1] > maks_card:
                    maks_card = evel_hand(players[i].cards + table_cards)[1]
                    winner = i
            return players[winner].id

        # biggest card
        if maks_value == 0:
            winner = None
            maks_card = -1
            for i in same_hand_weight_list:
                if evel_hand(players[i].cards + table_cards)[1] > maks_card:
                    maks_card = evel_hand(players[i].cards + table_cards)[1]
                    winner = i
            return players[winner].id



if __name__ == "__main__":
    card1 = Card(13, 1)
    card2 = Card(3, 1)
    card3 = Card(7, 0)
    card4 = Card(9, 2)
    card5 = Card(10, 1)
    card6 = Card(2, 2)
    card7 = Card(12, 3)
    hand = []
    table = []
    hand.append(card1)
    hand.append(card2)
    hand.append(card3)
    hand.append(card4)
    hand.append(card5)
    hand.append(card6)
    hand.append(card7)
    res = evel_hand(hand)
    print(res[0])
    for c in res[1]:
        print(c)

