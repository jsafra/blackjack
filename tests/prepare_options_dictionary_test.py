import unittest
from blackjack_cli import _prepare_options_dictionary

class PrepareOptionsDictionaryTest(unittest.TestCase):
    def test_options_from_string(self):
        test_values = [
            (
                ["a", "b", "c"],
                {"a" : ["a"], "b" : ["b"], "c" : ["c"]},
                False
            ),
            (
                ["ahoj", "bye", "ciao"],
                {"a": ["a", "h", "o", "j"], "b" : ["b", "y", "e"], "c" : ["c", "i", "a", "o"]},
                False
            ),
            (
                ["ahoj", "BYE"],
                {"a": ["a", "h", "o", "j"], "b" : ["b", "y", "e"]},
                False
            ),
            (
                ["ahoj", "BYE"],
                {"a": ["a", "h", "o", "j"], "B" : ["B", "Y", "E"]},
                True
            )
        ]
        for opt_list, opt_dict, opt_case_sensitive in test_values:
            self.assertEqual(opt_dict, _prepare_options_dictionary(opt_list, opt_case_sensitive))

    def test_options_from_tupple(self):
        test_values = [
            (
                [("y", "yes"), ("n", "no")],
                {"y" : ["y", "yes"], "n" : ["n", "no"]}
            ),
            (
                ["y", ("n", "no")],
                {"y" : ["y"], "n" : ["n", "no"]}
            )
        ]
        for opt_list, opt_dict in test_values:
            self.assertEqual(opt_dict, _prepare_options_dictionary(opt_list))

if __name__ == "__main__":
    unittest.main()