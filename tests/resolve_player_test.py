import unittest

from blackjack import resolve_player


class ResolvePlayerTest(unittest.TestCase):
    def test_resolve_player_blackjack(self):
        test_player = {
            "game": {
                "hand": [{"values": (10, )}, {"values": (11, 1)}],
                "result": None
            }
        }
        resolve_player(test_player)
        self.assertEqual("BJ", test_player["game"]["result"])

    def test_resolve_player_busted(self):
        test_player = {
            "game": {
                "hand": [
                    {"values": (10, )}, {"values": (9, )}, {"values": (5, )}
                ],
                "result": None
            }
        }
        resolve_player(test_player)
        self.assertEqual("BS", test_player["game"]["result"])

    def test_resolve_player_score(self):
        test_player = {
            "game": {
                "hand": [
                    {"values": (10, )}, {"values": (9, )}
                ],
                "result": None
            }
        }
        resolve_player(test_player)
        self.assertEqual(19, test_player["game"]["result"])


if __name__ == "__main__":
    unittest.main()
