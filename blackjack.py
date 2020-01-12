#!/usr/bin/python
'''blackJack.py let's user play a game of Black Jack against a dealer'''

import random
import logging
from blackjack_cli import user_input, user_choice, label_print

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(level=logging.CRITICAL)


def generate_cards():
    '''Generation of all existing playing cards. Problably reading from config
    file could be better but it doesn't matter for this moment.

    One playing card will be represented by dictionary {number, pip, name,
    abbr, (values,)}.

    No input
    Output: List of playing cards - reusable in repeating games.

    >>> c = generate_cards()
    >>> len(c)
    52
    >>> c[1]['abbr']
    '3♥'
    >>> c[11]['values']
    (10,)
    >>> c[12]['values']
    (11, 1)
    '''

    all_cards = []
    colors = [('hearts', '♥'), ('diamonds', '♦'), ('spades', '♣'),
              ('clubs', '♠')]
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']

    for color in colors:
        for card in cards:
            # TODO: This is quick and dirty! Make it nicer some day :-)
            if type(card) is int:
                values = (card, )
            elif card in ('Jack', 'Queen', 'King'):
                values = (10, )
            else:
                values = (11, 1)

            new_card = {
                "number": str(card),
                "pip": color[0],
                "name": str(card) + ' of ' + color[0],
                "abbr": (str(card) if type(card) is int else card[0]) + color[1],
                "values": values
            }
            all_cards.append(new_card)
    return all_cards


def prepare_deck(all_cards):
    '''Prepare a new deck for a game and shuffle cards. Repeating generation of
    cards doesn't occur anymore.

    Input: list cards for playing
    Output: a deck of cards
    '''
    deck = []
    deck.extend(all_cards)
    random.shuffle(deck)

    return deck


def draw_card(deck):
    '''
    Draws a card from a deck
    Input: a deck of cards (list)
    Output: one card from the deck (string)

    >>> test_deck = [{'abbr': 'a'}, {'abbr' :'b'}, {'abbr': 'c'}]
    >>> draw_card(test_deck)['abbr']
    'c'
    >>> draw_card(test_deck)['abbr']
    'b'
    '''
    # get and remove last card of a list (this has been already shuffled)
    drawn_card = deck.pop()
    logging.debug("'{}' have been drawn and scratched from the deck".format(drawn_card['abbr']))
    return drawn_card


def hand_value(hand):
    '''Counts total value of all cards in hand.

    Parameters
    ----------
    hand : `list`
        List of all cards in a hand. Every card is represented by `dict` -
        for more details look at `generate_cards` function.

    Returns
    -------
    int
        Total number of points in a hand (integer)

    Examples
    --------
    >>> hand_value([{"values": (10,)}, {"values": (8,)}])
    18

    For more examples look at related unittests.
    '''
    sum = 0

    for card in sorted(hand, key=lambda c: len(c['values'])):
        s_value = card['values'][0]
        # for one-valued card result of slice is an empty tuple
        # thus for cycle is skipped
        for value in card['values'][1:]:
            if sum + s_value > 21:
                s_value = value
        sum += s_value

    return sum


def hand_status(player):
    '''Returns a text message with cards and total points.

    Parameters
    ----------
    player : dictionary

    Returns
    -------
    string
        Human readable string to be displayed to player.
    '''
    if player['role'] == "player":
        status = "You have {} in your hand which makes a {}-point hand."
    else:
        status = "The dealer has {} in his hand which makes a {}-point hand."
    status = status.format([c["abbr"] for c in player["game"]["hand"]],
                           hand_value(player["game"]["hand"]))
    return status


def show_results(players):
    '''
    Prints out a result of a single game of blackjack. Uses function
    'resolve_game' in the process.
    Input: two final hands to be resulted (lists)
    Output: prints out value a player's and banker's hand.
    '''

    label_print("** GAME RESULTS **", decoration="*")

    for player in players[:-1]:
        print(hand_status(players[-1]))
        print(hand_status(player))
        result = resolve_game(players[0], players[1])
        print(result[1])

    print()


def resolve_game(player, dealer):
    '''Decides the result of a single game.

    Works upon result of player and dealer.

    Parameters
    ----------
    player : dict
        Dictionary representing a player
    dealer : dict
        Dictionary representing a dealer

    Returns
    -------
    resultCode
        Text code representing a result of a game.
        Values: PW (= player wins), DW (= dealer wins), SO (= stand off)
    resultText
        Text message with a game result.
    '''
    player_result = player["game"]["result"]
    dealer_result = dealer["game"]["result"]

    if player_result == "BS":
        return ("DW", "Sorry, you are busted.")

    if player_result == "SR":
        return ("DW", "Sorry, you surrended.")

    elif dealer_result == "BS":
        return ("PW", "You win - dealer is busted.")

    # checks for straight blackjack and if so ends the game
    elif player_result == "BJ" != dealer_result:
        return ("PW", "Blackjack, you win!")

    elif player_result != "BJ" == dealer_result:
        return ("DW", "Dealer has got a blackjack, you lose this game!")

    elif player_result > dealer_result:
        return ("PW", "Congratulations, you win.")

    elif dealer_result > player_result:
        return ("DW", "Bad luck, you lose this time.")

    elif player_result == dealer_result:
        return ("SO", "Stand off - neither dealer nor player win.")

    else:
        raise NotImplementedError("Something's wrong. Developer didn't think",
                                  "about some specific situation :-)")


def resolve_player(player):
    """Set a status of player game according his cards.

    Parameters
    ----------
    player : dictionary
        Dictionary representing player entity.

    Returns
    -------
    None

    See also
    --------
    See doc/objects.md for more details about player representation.
    """
    if player["game"]["result"] is None:
        player_score = hand_value(player["game"]["hand"])
        player_blackjack = player_score == 21 and \
            len(player["game"]["hand"]) == 2

        if player_blackjack:
            player["game"]["result"] = "BJ"
        else:
            player["game"]["result"] = player_score if player_score <= 21 \
                else "BS"


def player_turn(player, deck):
    '''Encapsulates a player actions

    Parameters
    ----------
    player : `dict`
        Dictionary representing player. Presence of 'hand' key is expected.
    deck : `dict`
        List of cards. Every card is represented as a dictionary, this
        function expect presence of 'abbr' key and 'value' consequently.

    Returns
    -------
    `None`
    '''
    logging.debug("This is as player turn")

    print(hand_status(player))
    player_answer = ''

    # keep playing until player doesn't stay or has 21 or more points
    while hand_value(player["game"]["hand"]) < 21 \
            and player_answer not in ("s", "d", "r"):
        player_answer = user_choice(
            options=[
                ("h", "hit"), ("s", "stay"), ("d", "double"), ("r", "surrend")
            ],
            prompt="What would you like to do? (hit, stay, double, surrend): "
        )

        if player_answer == "h":  # hit -> draw a card
            player["game"]["hand"].append(draw_card(deck))
            print(hand_status(player))
        elif player_answer == "d":  # double
            # TODO: increase the bet here
            player["game"]["hand"].append(draw_card(deck))
        elif player_answer == "r":  # surrender
            # TODO: give one half of bet to dealer and return second half
            player["game"]["result"] = "SR"


def dealer_turn(dealer, deck, soft17_draw=False):
    '''Encapsulates dealer actions.

    Implements rules for dealer turn. When dealer has less than 17 points
    he must draw a card. When dealer has 17 and more points he mustn't
    draw card.

    Parameters
    ----------
    dealer : `dict`
        Dictionary representing player. Presence of 'hand' key is expected.
    deck : `list`
        List of cards. Every card is represented as a dictionary, this
        function expect presence of 'abbr' key and 'value' consequently.
    soft17_draw : `Bool`, optional
        If `True` then dealer draw a new card when having soft-17 (i.e. 17
        point with one Ace)

    Returns
    -------
    `None`
    '''
    logging.debug("This is as dealer turn")

    # TODO: Implement soft17_draw logic
    while hand_value(dealer["game"]["hand"]) < 17:
        logging.debug(hand_status(dealer))
        logging.debug("Dealer has less than 17 points - he must draw a card")
        dealer["game"]["hand"].append(draw_card(deck))

    logging.debug(hand_status(dealer))
    logging.debug("Dealer has 17 points or more - he must stand up")


def play_game(players, all_cards):
    '''Plays a single round of blackjack. Uses all the functions above.
    Input: User input according to the instructions printed out
    Output: Let's user play a single round of blackjack
    '''

    # NOTE: Blackjack is played with 1-8 decks of card. It should be easy to
    # implement this now.
    deck = prepare_deck(all_cards)

    for player in players:
        player["game"] = {"hand": [], "result": None, "bet": 0}

    for _ in range(0, 2):
        for player in players:
            # NOTE: In some variations of blackjack dealer gets only first card
            # at the start of a game or distinguish 'up card' and 'hole card'
            # and so on
            player["game"]["hand"].append(draw_card(deck))

    for player in players:
        player['turn'](player, deck)
        resolve_player(player)

    show_results(players)


if __name__ == "__main__":
    # some automated tests before playing a game
    import doctest
    doctest.testmod()

    # let's go play
    all_cards = generate_cards()

    # Represent players as a dictionary. May be the hand shouldn't be part of
    # this dictionary?
    # TODO: dynamic number of players with various names. But ensure that
    # dealer is the last one and only one !!
    players = [
        {
            "name": "John Doe",
            "role": "player",
            "turn": player_turn,
            "cash": 1000,
            "game": {"hand": [], "result": None, "bet": 0}
        },
        {
            "name": "Anonymous Dealer",
            "role": "dealer",
            "turn": dealer_turn,
            "cash": 1000,
            "game": {"hand": [], "result": None}
        }
    ]

    while True:
        one_more_game = user_choice(
            prompt="Hi, are you up for a game of blackjack? If so just say" +
                   "'yes' otherwise say 'no': "
        )
        if one_more_game == "y":
            label_print("This is a new game - enjoy it.")
            play_game(players, all_cards)
        else:
            break

    print('Thanks for the game(s), see you soon.')
