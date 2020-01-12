# Player

Each player is represented by dictionary (see example below).

```python
{
    "name": "John Doe",
    "role": "player",
    "turn": player_turn,
    "cash": 1000,
    "game": {
        "hand": [],
        "result": 12,
        "bet": 0
    }
}
```

Attributes explanation:

*   `name` attribute is for display purposes only.
*   `role` is intended to distinguish different types of player. Actualy this
    attribut has values `player` (i.e. human player) a `dealer` (computer
    driven entity). Some days there could appear value `player_ai` representing
    player driven by some algoritm.
*   `turn` is a reference to function ensuring player actions.
*   `cash` is a amount of money holded by player. When `role=="player"` attribute
    `cash` represents a jackpot.
*   `game` holds status of player in current game. It's just another dictionary
    with keys:

    *   `hand` represents cards held by player. It's a list containing another
        dictionary again - look at chapter "Card"
    *   `result` represents result of player game. It has values `"BJ"`
        (i.e. blackjack), `"BS"` (i.e. busted), `"SR"` (i.e. surrended) and
        numeric variable (i.e. sum of cards values).
    *   `bet` represent a bet of player in current game. When 
        `role=="dealer"` there is not `bet` attribute.

# Card

Each card is represented by dictionary (see example below).

```python
{
    "number": 3,
    "pip": "hearts",
    "name": "3 of hearts",
    "abbr": "3♥",
    "values": (3, )
}
```

Attribute explanation:

*   `number` is number of card. It's either number in range 2..9 or enumeration
    of strings `"Jack"`, `"Queen"`, `"King"` and `"Ace"`
*   `pip` is the "color" of the card. It' one of string enumeration `"hearts"`,
    `"diamonds"`, `"clubs"` and `"spades"`.
*   `name` is textual representation of card, e.g. `"3 of hearts"`
*   `abbr` is abbreviated representation of card, e.g. `"3♥"`.
*   `values` is a tupple of values that this card could have. This is used for
    score of player hand calculation although the choice of appropriate value
    is a responsibility of game engine.
