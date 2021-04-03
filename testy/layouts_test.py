import unittest
from classes.card import Card
from classes.layouts import evel_hand


class MyTestCase(unittest.TestCase):
    def test_straight_flush(self):
        cards = [Card(14, 3), Card(10, 1), Card(11, 1), Card(12, 1), Card(13, 1), Card(14, 1), Card(5, 2)]
        hand = [c for c in cards]
        self.assertEqual((8, [cards[5], cards[4], cards[3], cards[2], cards[1]]), evel_hand(hand))

        cards = [Card(14, 3), Card(10, 1), Card(11, 1), Card(12, 1), Card(13, 1), Card(14, 1), Card(10, 2)]
        hand = [c for c in cards]
        self.assertEqual((8, [cards[5], cards[4], cards[3], cards[2], cards[1]]), evel_hand(hand))

        cards = [Card(14, 3), Card(10, 1), Card(11, 1), Card(12, 1), Card(13, 1), Card(9, 1), Card(5, 2)]
        hand = [c for c in cards]
        self.assertEqual((8, [cards[4], cards[3], cards[2], cards[1], cards[5]]), evel_hand(hand))

        cards = [Card(14, 3), Card(10, 1), Card(11, 1), Card(12, 1), Card(13, 1), Card(9, 1), Card(5, 2)]
        hand = [c for c in cards]
        self.assertEqual((8, [cards[4], cards[3], cards[2], cards[1], cards[5]]), evel_hand(hand))

        cards = [Card(14, 1), Card(10, 1), Card(11, 1), Card(12, 1), Card(13, 1), Card(9, 1), Card(11, 2)]
        hand = [c for c in cards]
        self.assertEqual((8, [cards[0], cards[4], cards[3], cards[2], cards[1]]), evel_hand(hand))

    def test_quads(self):
        cards = [Card(14, 3), Card(14, 1), Card(14, 2), Card(14, 0), Card(13, 1), Card(13, 2), Card(5, 2)]
        hand = [c for c in cards]
        self.assertEqual((7, [cards[0], cards[2], cards[1], cards[3], cards[5]]), evel_hand(hand))

        cards = [Card(13, 3), Card(14, 1), Card(14, 2), Card(13, 0), Card(13, 1), Card(13, 2), Card(5, 2)]
        hand = [c for c in cards]
        self.assertEqual((7, [cards[0], cards[5], cards[4], cards[3], cards[2]]), evel_hand(hand))

        cards = [Card(2, 3), Card(14, 1), Card(14, 2), Card(2, 0), Card(2, 1), Card(2, 2), Card(5, 2)]
        hand = [c for c in cards]
        self.assertEqual((7, [cards[0], cards[5], cards[4], cards[3], cards[2]]), evel_hand(hand))

        cards = [Card(13, 3), Card(14, 1), Card(14, 2), Card(13, 0), Card(13, 1), Card(13, 2), Card(5, 2)]
        hand = [c for c in cards]
        self.assertEqual((7, [cards[0], cards[5], cards[4], cards[3], cards[2]]), evel_hand(hand))

        cards = [Card(10, 3), Card(2, 1), Card(2, 2), Card(10, 0), Card(10, 1), Card(10, 2), Card(2, 3)]
        hand = [c for c in cards]
        self.assertEqual((7, [cards[0], cards[5], cards[4], cards[3], cards[6]]), evel_hand(hand))

    def test_full(self):
        cards = [Card(13, 3), Card(14, 1), Card(14, 2), Card(13, 0), Card(13, 1), Card(5, 2), Card(5, 1)]
        hand = [c for c in cards]
        self.assertEqual((6, [cards[0], cards[4], cards[3], cards[2], cards[1]]), evel_hand(hand))

        cards = [Card(13, 3), Card(14, 1), Card(14, 2), Card(13, 0), Card(13, 1), Card(14, 0), Card(5, 1)]
        hand = [c for c in cards]
        self.assertEqual((6, [cards[2], cards[1], cards[5], cards[0], cards[4]]), evel_hand(hand))

    def test_flush(self):
        cards = [Card(13, 1), Card(14, 1), Card(7, 1), Card(6, 1), Card(10, 1), Card(8, 1), Card(5, 1)]
        hand = [c for c in cards]
        self.assertEqual((5, [cards[1], cards[0], cards[4], cards[5], cards[2]]), evel_hand(hand))

        cards = [Card(13, 1), Card(14, 1), Card(7, 1), Card(6, 2), Card(10, 2), Card(8, 1), Card(5, 1)]
        hand = [c for c in cards]
        self.assertEqual((5, [cards[1], cards[0], cards[5], cards[2], cards[6]]), evel_hand(hand))

        cards = [Card(13, 1), Card(14, 1), Card(7, 1), Card(14, 2), Card(10, 2), Card(8, 1), Card(5, 1)]
        hand = [c for c in cards]
        self.assertEqual((5, [cards[1], cards[0], cards[5], cards[2], cards[6]]), evel_hand(hand))

    def test_straight(self):
        cards = [Card(13, 1), Card(14, 1), Card(12, 3), Card(11, 2), Card(10, 2), Card(8, 1), Card(5, 1)]
        hand = [c for c in cards]
        self.assertEqual((4, [cards[1], cards[0], cards[2], cards[3], cards[4]]), evel_hand(hand))

        cards = [Card(13, 3), Card(14, 2), Card(12, 3), Card(11, 2), Card(10, 2), Card(8, 1), Card(13, 1)]
        hand = [c for c in cards]
        self.assertEqual((4, [cards[1], cards[0], cards[2], cards[3], cards[4]]), evel_hand(hand))

        cards = [Card(13, 3), Card(14, 2), Card(12, 3), Card(11, 2), Card(10, 2), Card(9, 1), Card(13, 1)]
        hand = [c for c in cards]
        self.assertEqual((4, [cards[1], cards[0], cards[2], cards[3], cards[4]]), evel_hand(hand))

    def test_trips(self):
        cards = [Card(13, 3), Card(13, 2), Card(13, 1), Card(11, 2), Card(10, 2), Card(9, 1), Card(6, 1)]
        hand = [c for c in cards]
        self.assertEqual((3, [cards[0], cards[1], cards[2], cards[3], cards[4]]), evel_hand(hand))

        cards = [Card(2, 3), Card(2, 2), Card(2, 1), Card(11, 2), Card(10, 2), Card(9, 1), Card(12, 1)]
        hand = [c for c in cards]
        self.assertEqual((3, [cards[0], cards[1], cards[2], cards[6], cards[3]]), evel_hand(hand))

    def test_pair_2(self):
        cards = [Card(13, 3), Card(13, 2), Card(11, 2), Card(11, 1), Card(10, 2), Card(9, 1), Card(6, 1)]
        hand = [c for c in cards]
        self.assertEqual((2, [cards[0], cards[1], cards[2], cards[3], cards[4]]), evel_hand(hand))

    def test_pair(self):
        cards = [Card(13, 3), Card(13, 2), Card(11, 2), Card(10, 1), Card(8, 2), Card(5, 1), Card(6, 1)]
        hand = [c for c in cards]
        self.assertEqual((1, [cards[0], cards[1], cards[2], cards[3], cards[4]]), evel_hand(hand))

    def test_high(self):
        cards = [Card(13, 3), Card(11, 2), Card(9, 2), Card(8, 1), Card(6, 2), Card(5, 1), Card(2, 1)]
        hand = [c for c in cards]
        self.assertEqual((0, [cards[0], cards[1], cards[2], cards[3], cards[4]]), evel_hand(hand))

if __name__ == '__main__':
    unittest.main()
