import unittest
from blackjack import hand_value

class HandValueTest(unittest.TestCase):
    def test_hand_value(self):
        test_data = [
            (
                [{"values": (10,)}, {"values": (8,)}],
                18
            ),
            (
                [{"values": (10,)}, {"values": (8,)}, {"values": (3, )}],
                21
            ),
            (
                [{"values": (10,)}, {"values": (11, 1)}],
                21
            ),
            (
                [{"values": (11, 1)}, {"values": (11, 1)}],
                12
            ),
            (
                [{"values": (10,)}, {"values": (8,)}, {"values": (11, 1)}],
                19
            ),
            (
                [{"values": (10,)}, {"values": (8,)}, {"values": (5, )}],
                23
            ),
            (
                [{"values": (11, 1)}, {"values": (8,)}, {"values": (5, )}, {"values": (10, )}],
                24
            ),
            (
                [{"values": (11, 1)}, {"values": (9,)}, {"values": (11, 1)}],
                21
            )
        ]

        for cards, expected_value in test_data:
            computed_value = hand_value(cards)
            self.assertEqual(expected_value, computed_value)

if __name__ == "__main__":
    unittest.main()
