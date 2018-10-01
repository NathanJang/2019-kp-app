from enum import Enum
import itertools
from random import shuffle


class Deck:
    """An object representing the undealt deck of cards."""
    def __init__(self):
        self._stack = [Card(value, suit) for (value, suit) in itertools.product(Value, Suit)]
        shuffle(self._stack)

    def len(self):
        return len(self._stack)

    def draw(self):
        if self.len() == 0:
            return None
        return self._stack.pop()


class Card:
    """An object representing a single card."""
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return "<{} of {}>".format(self.value.value, self.suit.value)

    def __str__(self):
        return "{}{}".format(self.value.value, self.suit.value)


class Value(Enum):
    """An enum for the allowed values of the deck."""
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "⒑"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"

    def is_valid_pair(self, other):
        if self is Value.ACE:
            return other is Value.QUEEN
        elif self is Value.TWO:
            return other is Value.JACK
        elif self is Value.THREE:
            return other is Value.TEN
        elif self is Value.FOUR:
            return other is Value.NINE
        elif self is Value.FIVE:
            return other is Value.EIGHT
        elif self is Value.SIX:
            return other is Value.SEVEN
        elif self is Value.SEVEN:
            return other is Value.SIX
        elif self is Value.EIGHT:
            return other is Value.FIVE
        elif self is Value.NINE:
            return other is Value.FOUR
        elif self is Value.TEN:
            return other is Value.THREE
        elif self is Value.JACK:
            return other is Value.TWO
        elif self is Value.QUEEN:
            return other is Value.ACE
        else:
            return False


class Suit(Enum):
    """An enum for the suits of the deck."""
    DIAMOND = "♦"
    CLUB = "♣︎"
    HEART = "♥︎"
    SPADE = "♠︎"


class CardState(Enum):
    SELECTED = 0
    HIGHLIGHTED = 1
    HIDDEN = 2
    NORMAL = 3
