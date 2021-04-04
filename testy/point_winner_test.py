import unittest
from classes.card import Card
from classes.layouts import *


class MyTestCase(unittest.TestCase):
    def test_winners(self):
        table = [Card(7,3), Card(6,1), Card(6,2), Card(3,1), Card(2,1)]
        player1 = Player(100, 0, "lolo")
        player2 = Player(100, 1, "soso")
        player3 = Player(100, 2, "koko")
        players = [player1, player2, player3]

        player1.add_cards([Card(11,1), Card(7,2)])
        player2.add_cards([Card(14,1), Card(7,3)])

        self.assertEqual([player2], point_the_winner([player1,player2], table))
        for p in players: p.remove_cards()
        #best hand on table, available for everyone
        table = [Card(14, 1), Card(13, 1), Card(12, 1), Card(11, 1), Card(10, 1)]
        player1.add_cards([Card(11, 2), Card(7, 2)])
        player2.add_cards([Card(14, 2), Card(7, 3)])
        player3.add_cards([Card(11, 3), Card(7, 0)])
        self.assertEqual([player1, player2, player3], point_the_winner([player1, player2, player3], table))
        for p in players: p.remove_cards()

        #player3 - flush, everyone got straight
        table = [Card(14, 3), Card(13, 1), Card(12, 1), Card(11, 1), Card(10, 1)]
        player1.add_cards([Card(11, 2), Card(7, 2)])
        player2.add_cards([Card(14, 2), Card(7, 3)])
        player3.add_cards([Card(11, 3), Card(7, 1)])
        self.assertEqual([player3], point_the_winner([player1, player2, player3], table))
        for p in players: p.remove_cards()

        table = [Card(12, 1), Card(4, 1), Card(7, 1), Card(5, 1), Card(8, 2)]
        player1.add_cards([Card(10, 1), Card(11, 1)])
        player2.add_cards([Card(2, 1), Card(8, 1)])
        player3.add_cards([Card(12, 3), Card(12, 2)])
        self.assertEqual([player1], point_the_winner([player1, player2, player3], table))
        for p in players: p.remove_cards()

        table = [Card(11, 3), Card(11, 0), Card(9, 0), Card(14, 3), Card(2, 3)]
        player1.add_cards([Card(7, 0), Card(8, 3)])
        player2.add_cards([Card(13, 2), Card(4, 1)])
        player3.add_cards([Card(14, 1), Card(10, 2)])
        self.assertEqual([player3], point_the_winner([player1, player2, player3], table))
        for p in players: p.remove_cards()

        table = [Card(14, 3), Card(13, 3), Card(12, 3), Card(11, 3), Card(10, 3)]
        player1.add_cards([Card(2, 0), Card(3, 0)])
        player2.add_cards([Card(2, 1), Card(3, 1)])
        player3.add_cards([Card(2, 2), Card(3, 2)])
        self.assertEqual([player1, player2, player3], point_the_winner([player1, player2, player3], table))
        for p in players: p.remove_cards()

        table = [Card(2, 1), Card(2, 2), Card(5, 2), Card(14, 0), Card(10, 3)]
        player1.add_cards([Card(5, 0), Card(5, 3)])
        player2.add_cards([Card(14, 1), Card(14, 2)])
        player3.add_cards([Card(9, 2), Card(10, 2)])
        self.assertEqual([player2], point_the_winner([player1, player2, player3], table))
        for p in players: p.remove_cards()

        table = [Card(10, 0), Card(14, 0), Card(13, 2), Card(8, 1), Card(2, 2)]
        player1.add_cards([Card(13, 3), Card(14, 3)])
        player2.add_cards([Card(10, 1), Card(10, 2)])
        player3.add_cards([Card(7, 2), Card(7, 1)])
        self.assertEqual([player2], point_the_winner([player1, player2, player3], table))
        for p in players: p.remove_cards()

        table = [Card(10, 0), Card(14, 3), Card(5, 3), Card(8, 1), Card(2, 2)]
        player1.add_cards([Card(13, 3), Card(14, 2)])
        player2.add_cards([Card(10, 1), Card(10, 2)])
        player3.add_cards([Card(4, 3), Card(3, 3)])
        self.assertEqual([player3], point_the_winner([player1, player2, player3], table))
        for p in players: p.remove_cards()

        table = [Card(14, 3), Card(4, 1), Card(5, 2), Card(11, 3), Card(10, 2)]
        player1.add_cards([Card(2, 1), Card(3, 2)])
        player2.add_cards([Card(13, 0), Card(12, 0)])
        player3.add_cards([Card(6, 3), Card(4, 3)])
        self.assertEqual([player2], point_the_winner([player1, player2, player3], table))
        for p in players: p.remove_cards()







if __name__ == '__main__':
    unittest.main()
