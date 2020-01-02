'''Helper module for a blackjack game'''

def user_input(**kwargs):
    '''Calls for user input from CLI with defined prompt.

    It is possible to adjust to actual need by set of optional keywords (look at Other parameters section.)

    `print(user_input(prompt="Neco mi rekni:", accept_values=['yes', 'no'], case_sensitive=True))`

    Other parameters
    ----------------
    prompt : `str`, optional
        Message to be shown to user.
    accept_values : `list`, optional
        List of values to be accepted. If not specified any input is accepted. Default `[]`
    case_sensitive : `bool`, optional
        If `True` then uppercase and lowercase letters are treated as distinct. Default `False`

    Returns
    -------
    str
        Text entered by user
    '''

    accept_values = kwargs.get("accept_values", [])
    prompt = kwargs.get("prompt", "Give me some input please:")
    case_sensitive = kwargs.get("case_sensitive", False)

    if accept_values:     # Empty list is evaluated as False
        prompt.format("/".join(accept_values))
    if not case_sensitive:
        accept_values = [av.lower() for av in accept_values]

    raw_input = input(prompt) if case_sensitive else input(prompt).lower()
    
    while accept_values and raw_input not in accept_values:   # Check user input against accepted values
        print("I'm sorry I don't understand. Please answer {}:".format("/".join(accept_values)))
        raw_input = input(prompt) if case_sensitive else input(prompt).lower()
    
    return raw_input

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
    a = user_input(prompt="Neco mi rekni:", accept_values=['yes', 'no'], case_sensitive=True)

    label_print("You said " + a)