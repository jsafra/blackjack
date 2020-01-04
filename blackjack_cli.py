'''Helper module for a blackjack game'''

import re

def user_input(prompt = "", pattern = None, expected_type = str):
    '''Calls for user input from CLI with defined prompt.

    Parameters
    ----------------
    prompt : `str`, optional
        Message to be shown to user.
    pattern : `str` or `re.Pattern`, optional
        Regex pattern used for user input validation.
        Works only if expected_type param is not set or if `str` is its value.
    expected_type : `class`, optional
        Expected type of return value. User input is accepted only if it is possible to cast it to expected type.
        Default `str`.

    Returns
    -------
    `expected_type`
        Value entered by user

    Examples
    --------
        x1 = user_input(prompt="Tell me something: ")

        x2 = user_input(prompt="Tell me something: ", pattern="^a.*$")

        x3 = user_input(prompt="Tell me something: ", expected_type=float)  
    '''
    regex_validation = True if expected_type == str and pattern else False
    type_validation = expected_type != str

    if regex_validation and type(pattern) == str:
        pattern = re.compile(pattern)

    while regex_validation or type_validation:
        raw_input = input(prompt)
        if type_validation:
            try:
                raw_input = expected_type(raw_input)
                return raw_input
            except Exception:
                pass
        elif regex_validation:
            if pattern.match(raw_input):
                return raw_input
        print("Invalid input. Please answer in correct format.")

def label_print(message, decoration = "-", extra_line = True):
    '''Prints a message in an ascii frame.

    Parameters
    ----------
    message : `str`
        Message to be printed.
    decoration: `char`
        Character to be used for frame building. Default '-'.
    extra_line: `bool`
        If `True` then an additional empty lines is added before and after message. Default `True`
    '''
    if extra_line:
        print()
    print(decoration*len(message))
    print(message)
    print(decoration*len(message))
    if extra_line:
        print()

if __name__ == "__main__":
    a = user_input(prompt="Tell me something: ", pattern="^a.*$", expected_type=float)
    label_print("You said {} and it is {}".format(a, type(a))) 
