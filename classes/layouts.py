from classes.card import Card


def evel_hand(hand):  #7-cards
    NO_PAIR = 0
    PAIR = 1
    TWO_PAIR = 2
    TRIPS = 3
    STRAIGHT = 4
    FULL_HOUSE = 5
    FLUSH = 6
    QUADS = 7
    STRAIGHT_FLUSH = 8
    values = sorted([c.get_rank() for c in hand], reverse=True)
    suits = [c.get_suit() for c in hand]
    #looking for straight
    straight = False
    straight_counter = 1
    straight_max_value = values[0]
    for i in range(1, len(values)):
        if values[i] == values[i - 1] - 1:
            straight_counter +=1
            if straight_counter == 5:
                straight = True
        elif values[i] != values[i - 1]:
            straight_counter = 1
            straight_max_value = values[i]

    #looing for flush




    flush = all(s == suits[0] for s in suits)

    if straight and flush:
        print("poker")
        return STRAIGHT_FLUSH, max(values), suits[0]

    pairs = []
    three_same_valued_cards = False
    pair_present = False
    value_of_three = None
    for v in set(values):
        if values.count(v) == 4:
            print("kareta")
            return QUADS, values[0]
        if values.count(v) == 3:
            three_same_valued_cards = True
            value_of_three = v
        if values.count(v) == 2:
            pair_present = True
            pairs.append(v)
    if three_same_valued_cards and pair_present: # we found FULL_HOUSE
        print("FULL")
        return FULL_HOUSE, value_of_three, pairs[0] # zwraca wage FULL_HOUSE, wage trojki oraz wage pary
    if flush:
        print("KOLOR")
        return FLUSH # nie opcji na 2 różno kolorowe flushe
    if straight:
        print("STRIT")
        return STRAIGHT, values[0] #zwraca wage STRAIGHT oraz najwyższa wartość
    if three_same_valued_cards:
        print("TRÓJKA")
        return TRIPS, value_of_three
    if len(pairs) == 2:
        print("DWIE PARY")
        return TWO_PAIR, pairs[1], pairs[0] #zwraca wage podwójnej pary, wagę karty większej pary oraz wagę karty mniejszej pary, ewentualnie zamiast max i min dać pairs[0] i pairs[1] bo są posortowane chyba
    if len(pairs) == 1:
        print("PARA")
        return PAIR, pairs[0]

    print("NAJWIEKSZA KARTA")
    return NO_PAIR, values[0]



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

        # tutaj trzeba teraz ogarnac ify w zależnosci od maks value, bo każdy hand inaczej sie sprawdza
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
    card1 = Card(10, 3)
    card2 = Card(10, 3)
    card3 = Card(10, 2)
    card4 = Card(10, 0)
    card5 = Card(11, 1)
    hand = []
    hand.append(card1)
    hand.append(card2)
    hand.append(card3)
    hand.append(card4)
    hand.append(card5)
    print(evel_hand(hand)[0])
