'''Helper module for a blackjack game'''

import re


def validate(value, default_ruleset=[], *additional_rulesets):
    """Validate `value` against given rulesets. Each rulesets consist of
    several single rules

    `Value` is considered to be valid if it's valid against **any** ruleset.
    To be valid against a ruleset the value has to be valid against **all**
    rules of that ruleset.

    Any function with one parameter returning a boolean might be used as a
    rule. It includes standard library functions (e.g. `bool(x)` function)
    as well as user defined function. There exists some pre-defined function
    factories in module `blackjack_cli` (e.g. `rule_greater(x)`). Last but not
    least lambda functions works too.

    Parameters
    ----------
    value
        Value for validation

    default_ruleset
        List of rules. Single rule is a `function` with one parameter returning
        `True` if `value` satisfies the rule condition. Otherwise rule returns
        `False`.

    additional_rulesets
        Another lists of rules. If `default_ruleset` is not satisfied then
        validation against additional_rulesets happens.

    Returns
    -------
    bool
        `True` if any ruleset is satisfied -> value is considered to be valid.

    Examples
    --------
    Without rulesets any value is considered to be valid.

    >>> validate("anything")
    True

    Ruleset consist of several rules. All of them has to be satisfied.

    >>> validate(1, [rule_greater(10), rule_odd()])
    False

    There could be more than one ruleset. It's sufficient if one of them is
    satisfied.

    >>> validate(1, [rule_greater(10), rule_odd()], [rule_lower_equal(1)])
    True

    If there were no suitable pre-defined function then lambda would save our
    live.

    >>> validate(300, [lambda x: x % 100 == 0])
    True

    Standard library function works as well.

    >>> validate(10, [bool])
    True
    """
    all_rulesets = [default_ruleset]
    all_rulesets.extend(list(additional_rulesets))

    val_status = True   # Validation status (result of validation)

    for rules in all_rulesets:
        val_status = True
        for rule in rules:
            if not rule(value):
                val_status = False
                break
        if val_status:   # Current ruleset satisfied -> no need to continue
            break

    return val_status


def rule_odd():
    """Factory for function checking value to be odd.

    Returns
    -------
    `function`
        is_odd(value) -> bool
    """
    def is_odd(value):
        """Returns `True` if value is odd."""
        return value % 2 == 1
    return is_odd


def rule_greater(ref_value):
    """Factory for function checking value to be greater than a reference
    value.

    Parameters
    ----------
    `ref_value`
        Reference value

    Returns
    -------
    `function`
        is_greater(value) -> bool
    """
    def is_greater(value):
        """Returns `True` if value is greater than ref_value."""
        return value > ref_value
    return is_greater


def rule_greater_equal(ref_value):
    """Factory for function checking value to be greater or equal than
    a reference value.

    Parameters
    ----------
    `ref_value`
        Reference value

    Returns
    -------
    `function`
        is_greater_equal(value) -> bool
    """
    def is_greater_equal(value):
        """Returns `True` if value is greater or equal than ref_value."""
        return value >= ref_value
    return is_greater_equal


def rule_lower(ref_value):
    """Factory for function checking value to be lower than a reference value.

    Parameters
    ----------
    `ref_value`
        Reference value

    Returns
    -------
    `function`
        is_lower(value) -> bool
    """
    def is_lower(value):
        """Returns `True` if value is lower than ref_value."""
        return value < ref_value
    return is_lower


def rule_lower_equal(ref_value):
    """Factory for function checking value to be lower or equal than
    a reference value.

    Parameters
    ----------
    `ref_value`
        Reference value

    Returns
    -------
    `function`
        is_lower_equal(value) -> bool
    """
    def is_lower_equal(value):
        """Returns `True` if value is greater or equal than ref_value."""
        return value <= ref_value
    return is_lower_equal


def rule_pattern_match(pattern):
    """Factory for function checking value to match given regex.

    Parameters
    ----------
    `pattern` : `str` or `re.Pattern`, optional
        Regex pattern used for user input validation.

    Returns
    -------
    `function`
        is_pattern_match(value) -> bool
    """
    if type(pattern) == str:
        pattern = re.compile(pattern)

    def is_pattern_match(value):
        return bool(pattern.match(value))

    return is_pattern_match


def rule_sum(*refs):
    """Factory for function checking value to be equal to sum of reference
    values.

    Parameters
    ----------
    `*refs`
        Reference values

    Returns
    -------
    `function`
        is_sum(value) -> bool
    """
    def is_sum(value):
        """Return `True` if values is sum of *refs (reference values)"""
        ref_sum = sum(refs)
        return value == ref_sum
    return is_sum


# TODO: Add support for validation messages
def user_input(prompt="", expected_type=str, *rulesets):
    '''Calls for user input from CLI with defined prompt.

    Parameters
    ----------------
    prompt : `str`, optional
        Message to be shown to user.
    expected_type : `class`, optional
        Expected type of return value. User input is accepted only if it is
        possible to cast it to expected type.
        Default `str`.
    rulesets : `list` of rules
        Rulesets to be applied for input value validation.

    Returns
    -------
    `expected_type`
        Value entered by user

    Examples
    --------
    x1 = user_input("Tell me anything: ")

    x2 = user_input("Give me some integer: ", int)

    x3 = user_input("Tell me something starting with 'a': ", str,
                    [is_pattern_match("^a.*$")])

    See also
    --------
    Docstring of `validate` method for more details about validation rulesets.
    '''
    while True:
        raw_input = input(prompt)

        try:
            raw_input = expected_type(raw_input)
            if validate(raw_input, *rulesets):
                break
        except Exception:
            pass

        print("Invalid input. Please answer in correct format.")

    return raw_input


def _prepare_options_dictionary(options, case_sensitive=False):
    """Prepares dictionary from list of options. If option is iterable than
    first value if a key and all values (including the first one) are values.

    Remember: `str` is  iterable too :-)

    For internal use in `user_choice` function.

    Parameters
    ----------
    options : collection of options

    case_sensitive : `bool`
        If `False` then all strings are lowercased.

    Returns
    -------
    `dict`

    Examples
    --------
    >>> _prepare_options_dictionary(["blah"])
    {'b': ['b', 'l', 'a', 'h']}
    """

    options_dict = {}
    for option in options:
        try:
            values = []
            for opt in iter(option):
                if case_sensitive:
                    values.append(opt)
                else:
                    values.append(opt.lower())
            key = option[0] if case_sensitive else option[0].lower()
        except TypeError:
            key = option if case_sensitive else option.lower()
            values = [option, ] if case_sensitive else [option.lower(), ]
        options_dict[key] = values

    return options_dict


# TODO: Add support for validation messages
def user_choice(options=[("y", "yes"), ("n", "no")], prompt="",
                case_sensitive=False):
    """Gets an user choice from options. More different forms of any option
    might be declared.

    Parameters
    ----------
    options : `list`, optional
        List of options. If any option iterable it acceptes all forms but
        return first of them.
        Default `[("y", "yes"), ("n", "no")]` -- accepts y[es] or n[o] answer.
    prompt : `str`, optional
        Message to be shown to user.
    case_sensitive : `bool`
        If `True` then uppercase and lowercase letters are treated as distinct.
        Default `False`

    Returns
    -------
    user choice

    Examples
    --------
    a = user_choice([("y", "yes"), ("n", "no")], "Yes or no? ")

        If user write "y" or "yes" then fuction returns "y".
        If user write "n" or "no" then function returns "n"

    a = user_choice(prompt = "Yes or no?)

        The same as previous example
    """
    options = _prepare_options_dictionary(options)

    while True:
        raw_input = input(prompt) if case_sensitive else input(prompt).lower()
        for key, values in options.items():
            if raw_input in values:
                return key
        print("Incorrect value. Try it again.")


def label_print(message, decoration="-", extra_line=True):
    '''Prints a message in an ascii frame.

    Parameters
    ----------
    message : `str`
        Message to be printed.
    decoration: `char`
        Character to be used for frame building. Default '-'.
    extra_line: `bool`
        If `True` then an additional empty lines is added before and after
        message. Default `True`
    '''
    if extra_line:
        print()
    print(decoration*len(message))
    print(message)
    print(decoration*len(message))
    if extra_line:
        print()


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    x = user_input("Say 'hi': ", str, [rule_pattern_match("^[hH]i .*")])

    x = user_input("Give me some money: ", int,
                   [rule_greater(0), lambda x: x % 100 == 0],
                   [lambda x: x == -1])
