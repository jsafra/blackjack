import unittest
from blackjack import resolve_game

class ResolveGameTests(unittest.TestCase):
    def test_equal_points_stand_off(self):
        """Stand off when dealer and player have the same score"""
        player = {"hand": [{"values": (10, )}, {"values" : (8, )}]}
        dealer = {"hand": [{"values": (9, )}, {"values" : (5, )}, {"values" : (4, )}]}

        result = resolve_game(player, dealer)
        self.assertEqual("SO", result[0])

    def test_dealer_busted_player_wins(self):
        """Player wins when he's not busted but dealer is"""
        player = {"hand": [{"values": (10, )}, {"values" : (8, )}]}
        dealer = {"hand": [{"values": (9, )}, {"values" : (5, )}, {"values" : (8, )}]}

        result = resolve_game(player, dealer)
        self.assertEqual("PW", result[0])

    def test_player_busted_dealer_wins(self):
        """Dealer wins when player is busted. Even if dealer is busted too."""
        test_data = [
            (
                {"hand": [{"values": (10, )}, {"values" : (8, )}, {"values" : (5, )}]},
                {"hand": [{"values": (9, )}, {"values" : (8, )}]}
            ),
            (
                {"hand": [{"values": (10, )}, {"values" : (8, )}, {"values" : (5, )}]},
                {"hand": [{"values": (9, )}, {"values" : (8, )}, {"values" : (8, )}]}
            )            
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("DW", result[0])

    def test_blackjack_player_wins(self):
        """Player wins if he has got black jack."""
        test_data = [
            (
                {"hand": [{"values": (11, 1)}, {"values" : (10, )}]},
                {"hand": [{"values": (9, )}, {"values" : (8, )}]}
            ),
            (
                {"hand": [{"values": (10, )}, {"values" : (11, 1)}]},
                {"hand": [{"values": (9, )}, {"values" : (8, )}]}
            ),
            (
                {"hand": [{"values": (11, 1)}, {"values" : (10, )}]},
                {"hand": [{"values": (9, )}, {"values" : (8, )}, {"values" : (4, )}]}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("PW", result[0])

    def test_higher_score_wins(self):
        """Winner is's closer to the 21 than defeated"""
        test_data = [
            (
                {"hand": [{"values": (10, )}, {"values" : (10, )}]},
                {"hand": [{"values": (9, )}, {"values" : (8, )}]}
            ),
            (
                {"hand": [{"values": (8, )}, {"values" : (10, )}, {"values" : (3, )}]},
                {"hand": [{"values": (10, )}, {"values" : (10, )}]}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("PW", result[0])
        for dealer, player in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("DW", result[0])

if __name__ == "__main__":
    unittest.main()