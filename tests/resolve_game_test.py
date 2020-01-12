import unittest
from blackjack import resolve_game


class ResolveGameTests(unittest.TestCase):
    def test_equal_points_stand_off(self):
        """Stand off when dealer and player have the same score"""
        player = {"game": {"result": 21}}
        dealer = {"game": {"result": 21}}

        result = resolve_game(player, dealer)
        self.assertEqual("SO", result[0])

    def test_dealer_busted_player_wins(self):
        """Player wins when he's not busted but dealer is"""
        player = {"game": {"result": 20}}
        dealer = {"game": {"result": "BS"}}

        result = resolve_game(player, dealer)
        self.assertEqual("PW", result[0])

    def test_player_busted_dealer_wins(self):
        """Dealer wins when player is busted. Even if dealer is busted too."""
        test_data = [
            (
                {"game": {"result": "BS"}},
                {"game": {"result": 10}}
            ),
            (
                {"game": {"result": "BS"}},
                {"game": {"result": "BS"}}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("DW", result[0])

    def test_blackjack_wins(self):
        """Player wins if he has got black jack. Except his oponent has got blackjack too"""
        test_data = [
            (
                {"game": {"result": "BJ"}},
                {"game": {"result": 17}}
            ),
            (
                {"game": {"result": "BJ"}},
                {"game": {"result": 21}}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("PW", result[0])

        for dealer, player in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("DW", result[0])

    def test_higher_score_wins(self):
        """Winner is's closer to the 21 than defeated"""
        test_data = [
            (
                {"game": {"result": 20}},
                {"game": {"result": 17}}
            ),
            (
                {"game": {"result": 21}},
                {"game": {"result": 20}}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("PW", result[0])

        for dealer, player in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("DW", result[0])

    def test_blackjack_stand_off(self):
        """Stand off when player has got and blackjack as well as dealer"""
        test_data = [
            (
                {"game": {"result": "BJ"}},
                {"game": {"result": "BJ"}}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("SO", result[0])

        for dealer, player in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("SO", result[0])

    def test_player_surrended(self):
        """If player surrends the dealer wins"""
        test_data = [
            (
                {"game": {"result": "SR"}},
                {"game": {"result": "BJ"}}
            ),
            (
                {"game": {"result": "SR"}},
                {"game": {"result": "BS"}}
            ),
            (
                {"game": {"result": "SR"}},
                {"game": {"result": 21}}
            ),
            (
                {"game": {"result": "SR"}},
                {"game": {"result": 10}}
            )
        ]

        for player, dealer in test_data:
            result = resolve_game(player, dealer)
            self.assertEqual("DW", result[0])


if __name__ == "__main__":
    unittest.main()
