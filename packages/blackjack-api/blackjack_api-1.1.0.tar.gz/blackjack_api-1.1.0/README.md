# blackjack-api

A 1-on-1 blackjack game library for simulating games, usable for any blackjack needs.

View [here](https://pypi.org/project/blackjack-api/) on PyPI.

## Actual Library

### blackjack.py

The BlackJack class constructor takes several optional 
parameters:
- The number of decks to use
- The win ratio
- Whether the dealer hits on a soft 17
- Whether to use the 5-Card Charlie rule

The class automatically starts a round and hand. However, after completing a hand,
the driver program must call `BlackJack.start_hand()` to start a new hand. The class
boolean `BlackJack.hand_running` specifies whether a hand is running. As such, a
while loop may be helpful for running multiple hands programatically. When the
last hand terminates (Ex. when a player stands after being dealt their first hand),
the BlackJack class will automatically terminate the round as well. New
rounds can be started with `BlackJack.start_round()` and can be monitored with
`BlackJack.round_running`.

When both a round and hand are running, the player may be able to play the
following:
- `BlackJack.hit()`
- `BlackJack.stand()`
- `BlackJack.double()`
- `BlackJack.surrender()`
- `BlackJack.insurance(bet = .5)`

Of course, a player cannot surrender if they have already hit or split during
the round. However, all of these actions (with the exception of insurance)
can potentially terminate the hand. For example, standing will guarantee the hand
terminates, but hitting will only terminate the hand if the hand busts.

> [!WARNING]
> A hand does not automatically terminate when the player reaches a score of 21.
> This means the driver program still has to make a decision in this situation.

When a round does terminate, the dealer will play until their hand terminates. The
BlackJack class then computes the rewards for the player. Since a player can have 
multiple hands if they split, the `BlackJack.rewards` are stored as a variable,
where each reward correspond to the player's hand at the same index.

`BlackJack.hilo` tracks the *running* count of the deck and can be referenced
for advanced decision making in your driver programs.

### cli.py

Wraps the BlackJack class with a console interface. To see how to use the CLI
class, simply call `CLI.loop()`.

### Class Architecture

BlackJack stores the dealer as a Hand class and the player as a Player class.
The Player class is merely a list of Hand objects. However, each Hand class
is a list of Card objects.

The main highlights of the Hand class are the `Hand.count()` and `Hand.is_soft()` 
functions. The first gets the highest legal value of the hand—a return value of over
21 means the hand has busted! The latter function returns whether the highest legal
value of the hand counts an ace as an 11 instead of a 1.

The Card class is much simpler and has three values:
- The card name
- The value of the card (an ace's value is stored as `tuple([1, 11])`)
- The suit of the card (Ex. a spade has a suit of `'S'`)

The BlackJack class also uses a couple Deck objects to keep track of the deck
and discard pile. Whenever the deck empties, the discard pile will be used to
refill the deck.

## Tests

There are five different test files which demonstrate the library:

File | Description
-- | --
`basic_debug.py` | Run an individual game using basic strategy
`basic.py` | Run many games using basic strategy and plot the results
`double.py` | Run many games where the player only doubles down
`loop.py` | Run the premade console interface
`stand.py` | Run many games where the player only stand

### Notes to myself

To build the project yourself, simply run the following command:
```
python -m build
```
