import unittest
from blackjack_cli import validate, rule_odd, rule_greater_equal


class ValidateTest(unittest.TestCase):
    def test_no_ruleset_validation(self):
        """If no ruleset is given then anything is valid"""
        result = validate("Anything")
        self.assertEqual(True, result)

    def test_one_ruleset_validation(self):
        """Validation should works with exactly one ruleset"""
        test_dataset = [
            (   # One ruleset with one rule
                [lambda x: x >= 0],   # Ruleset
                [(-1, False), (0, True), (1, True)]   # Test values
            ),
            (   # One ruleset with three rules
                [lambda x: x >= 0, lambda x: x < 10, lambda x: x % 2 == 0],
                [(-1, False), (0, True), (1, False), (12, False)]
            )
        ]

        for ruleset, test_data in test_dataset:
            for value, expected_result in test_data:
                result = validate(value, ruleset)
                self.assertEqual(expected_result, result)

    def test_two_rulesets_validation(self):
        """Validation should works with more rulesets"""
        test_dataset = [
            (   # Two rulesets with one rule in each of them
                [
                    [lambda x: x >= 0],
                    [lambda x: x < -10]
                ],
                [(-1, False), (0, True), (1, True), (-12, True)]
            ),
            (   # One ruleset with three rules and one ruleset with two rules
                [
                    [lambda x: x >= 0, lambda x: x < 10, lambda x: x % 2 == 0],
                    [lambda x: x < 0, lambda x: x % 2 == 1]
                ],
                [
                    (0, True), (1, False), (10, False), (12, False),
                    (-1, True), (-2, False)
                ]
            )
        ]

        for rulesets, test_data in test_dataset:
            for value, expected_result in test_data:
                result = validate(value, *rulesets)
                self.assertEqual(expected_result, result)

    def test_rule_odd(self):
        """Almost useless test principle of factored function"""
        is_odd = rule_odd()
        self.assertEqual(True, is_odd(1))
        self.assertEqual(False, is_odd(2))

    def test_rule_greater_equal(self):
        """Almost useless test principle of factored function"""
        is_greater_equal = rule_greater_equal(5)
        self.assertEqual(False, is_greater_equal(4))
        self.assertEqual(True, is_greater_equal(5))
        self.assertEqual(True, is_greater_equal(6))


if __name__ == "__main__":
    unittest.main()
