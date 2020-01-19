import unittest
from blackjack import resolve_game


class ResolveGameTests(unittest.TestCase):
    def test_equal_points_stand_off(self):
        """Stand off when dealer and player have the same score"""
        player = {"cash": 900, "game": {"result": 21, "bet": 100}}
        dealer = {"cash": 1000, "game": {"result": 21}}

        result = resolve_game(player, dealer)
        self.assertEqual("SO", result[0])
        self.assertEqual(1000, player["cash"])
        self.assertEqual(1000, dealer["cash"])

    def test_dealer_busted_player_wins(self):
        """Player wins when he's not busted but dealer is"""
        player = {"cash": 900, "game": {"result": 20, "bet": 100}}
        dealer = {"cash": 1000, "game": {"result": "BS"}}

        result = resolve_game(player, dealer)
        self.assertEqual("PW", result[0])
        self.assertEqual(1100, player["cash"])
        self.assertEqual(900, dealer["cash"])

    def test_player_busted_dealer_wins(self):
        """Dealer wins when player is busted. Even if dealer is busted too."""
        test_data = [
            (
                {"cash": 900, "game": {"result": "BS", "bet": 100}},
                {"cash": 1000, "game": {"result": 10}}
            ),
            (
                {"cash": 900, "game": {"result": "BS", "bet": 100}},
                {"cash": 1000, "game": {"result": "BS"}}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("DW", result[0])
            self.assertEqual(900, player["cash"])
            self.assertEqual(1100, dealer["cash"])

    def test_blackjack_player_wins(self):
        """Player wins if he has got black jack. Except his oponent has
        got blackjack too"""
        test_data = [
            (
                {"cash": 900, "game": {"result": "BJ", "bet": 100}},
                {"cash": 1000, "game": {"result": 17}}
            ),
            (
                {"cash": 900, "game": {"result": "BJ", "bet": 100}},
                {"cash": 1000, "game": {"result": 21}}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("PW", result[0])
            self.assertEqual(1150, player["cash"])
            self.assertEqual(850, dealer["cash"])

    def test_blackjack_dealer_wins(self):
        """Dealer wins if he has got black jack. Except his oponent has
        got blackjack too"""
        test_data = [
            (
                {"cash": 900, "game": {"result": 17, "bet": 100}},
                {"cash": 1000, "game": {"result": "BJ"}}
            ),
            (
                {"cash": 900, "game": {"result": 21, "bet": 100}},
                {"cash": 1000, "game": {"result": "BJ"}}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("DW", result[0])
            self.assertEqual(900, player["cash"])
            self.assertEqual(1100, dealer["cash"])

    def test_higher_score_player_wins(self):
        """Player is's closer to the 21 than delaler"""
        test_data = [
            (
                {"cash": 900, "game": {"result": 20, "bet": 100}},
                {"cash": 1000, "game": {"result": 17}}
            ),
            (
                {"cash": 900, "game": {"result": 21, "bet": 100}},
                {"cash": 1000, "game": {"result": 20}}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("PW", result[0])
            self.assertEqual(1100, player["cash"])
            self.assertEqual(900, dealer["cash"])

    def test_higher_score_dealer_wins(self):
        """Winner is's closer to the 21 than defeated"""
        test_data = [
            (
                {"cash": 900, "game": {"result": 17, "bet": 100}},
                {"cash": 1000, "game": {"result": 20}}
            ),
            (
                {"cash": 900, "game": {"result": 20, "bet": 100}},
                {"cash": 1000, "game": {"result": 21}}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("DW", result[0])
            self.assertEqual(900, player["cash"])
            self.assertEqual(1100, dealer["cash"])

    def test_blackjack_stand_off(self):
        """Stand off when player has got and blackjack as well as dealer"""
        test_data = [
            (
                {"cash": 900, "game": {"result": "BJ", "bet": 100}},
                {"cash": 1000, "game": {"result": "BJ"}}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("SO", result[0])
            self.assertEqual(1000, player["cash"])
            self.assertEqual(1000, dealer["cash"])

    def test_player_surrended(self):
        """If player surrends the dealer wins"""
        test_data = [
            (
                {"cash": 900, "game": {"result": "SR", "bet": 100}},
                {"cash": 1000, "game": {"result": "BJ"}}
            ),
            (
                {"cash": 900, "game": {"result": "SR", "bet": 100}},
                {"cash": 1000, "game": {"result": "BS"}}
            ),
            (
                {"cash": 900, "game": {"result": "SR", "bet": 100}},
                {"cash": 1000, "game": {"result": 21}}
            ),
            (
                {"cash": 900, "game": {"result": "SR", "bet": 100}},
                {"cash": 1000, "game": {"result": 10}}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("DW", result[0])
            self.assertEqual(950, player["cash"])
            self.assertEqual(1050, dealer["cash"])


if __name__ == "__main__":
    unittest.main()
