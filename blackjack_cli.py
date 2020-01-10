'''Helper module for a blackjack game'''

import re

# TODO: Add support for validation functions
# TODO: Add support for validation messages
def user_input(prompt = "", expected_type = str, pattern = None, min_in = None, min_ex = None, max_in = None, max_ex = None):
    '''Calls for user input from CLI with defined prompt.

    Parameters
    ----------------
    prompt : `str`, optional
        Message to be shown to user.
    expected_type : `class`, optional
        Expected type of return value. User input is accepted only if it is possible to cast it to expected type.
        Default `str`.
    pattern : `str` or `re.Pattern`, optional
        Regex pattern used for user input validation.
        Works only if expected_type param is not set or if `str` is its value.
    min_in : `int` or `float`, optional
        Minimal acceptable value (inclusive) where expected_type is numerical type.
        Works only if expected_type param is `int` or `float`.
    min_ex : `int` or `float`, optional
        Minimal acceptable value (exclusive) where expected_type is numerical type.
        Works only if expected_type param is `int` or `float`.
    max_in : `int` or `float`, optional
        Maximal acceptable value (inclusive) where expected_type is numerical type.
        Works only if expected_type param is `int` or `float`.
    max_ex : `int` or `float`, optional
        Maximal acceptable value (exclusive) where expected_type is numerical type.
        Works only if expected_type param is `int` or `float`.

    Returns
    -------
    `expected_type`
        Value entered by user

    Examples
    --------
    x1 = user_input(prompt="Tell me something: ")

    x2 = user_input(prompt="Tell me something: ", pattern="^a.*$")

    x3 = user_input(prompt="Tell me something: ", expected_type=int)  
    '''
    regex_validation = True if expected_type == str and pattern else False
    type_validation = expected_type != str

    if regex_validation and type(pattern) == str:
        pattern = re.compile(pattern)

    validated = False if (regex_validation or type_validation) else True 
    
    while not validated:
        raw_input = input(prompt)

        if type_validation:
            try:
                raw_input = expected_type(raw_input)
                validated = True

                if (min_in is not None and min_in > raw_input):
                    validated = False
                if min_ex is not None and min_ex >= raw_input:
                    validated = False
                if max_in is not None and max_in < raw_input:
                    validated = False
                if max_ex is not None and max_ex <= raw_input:
                    validated = False
            except Exception:
                pass
        elif regex_validation:
            if pattern.match(raw_input):
                validated = True

        if not validated:
            print("Invalid input. Please answer in correct format.")
    
    return raw_input

def _prepare_options_dictionary(options, case_sensitive = False):
    """Prepares dictionary from list of options. If option is iterable than first value
    if a key and all values (including the first one) are values. 
    
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
            values = [option,]  if case_sensitive else [option.lower(),]
        options_dict[key] = values

    return options_dict

# TODO: Add support for validation messages
def user_choice(options = [("y", "yes"), ("n", "no")], prompt = "", case_sensitive = False):
    """Gets an user choice from options. More different forms of any option
    might be declared. 

    Parameters
    ----------
    options : `list`, optional
        List of options. If any option iterable it acceptes all forms but return first of them.
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
    import doctest
    doctest.testmod()

    # a = user_choice(prompt="Yes or no? ", case_sensitive=False)
    # print("Your choice: {}".format(a))


    
    old_input = input

    v = [10, 11, 12]

    def new_input(*args, **kwargs):
        return v.pop()

    input = new_input

    a = user_input(prompt="Some number: ", expected_type=int,max_in=10)

    print(a)
