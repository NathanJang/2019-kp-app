from src.deck import Deck, Suit, Value, CardState
from src.pyramid import Pyramid
from enum import Enum


class Game:
    """An object describing the game state."""
    def __init__(self, terminal):
        self._terminal = terminal
        self._deck = Deck()
        self._pyramid = Pyramid(self._deck)
        self._revealed_cards = [self._deck.draw()]
        self._game_state = GameState.RUNNING

    def run(self):
        """Runs the game."""
        with self._terminal.fullscreen():
            self.render()
            with self._terminal.cbreak():
                key = ""
                while key.lower() != 'q':
                    key = self._terminal.inkey()
                    self.handle_key(key)

    def handle_key(self, key):
        has_changes = False
        if key.name == "KEY_LEFT":
            self._pyramid.left()
            has_changes = True
        elif key.name == "KEY_RIGHT":
            self._pyramid.right()
            has_changes = True
        elif key.name == "KEY_UP":
            self._pyramid.up()
            has_changes = True
        elif key.name == "KEY_DOWN":
            self._pyramid.down()
            has_changes = True
        elif key.lower() == "d":
            has_changes = self.handle_draw()
        elif key.name == "KEY_ENTER":
            has_changes = self.handle_enter()
            if has_changes:
                print(self._terminal.clear())
        elif key.lower() == " ":
            has_changes = self.handle_space()
            if has_changes:
                print(self._terminal.clear())

        if has_changes:
            self.render()

    def render(self):
        self.render_undealt()
        self.render_pyramid()
        self.render_revealed()
        self.render_instructions()

    def render_instructions(self):
        term = self._terminal
        with term.location(0, 8):
            print("See {term.bold}README.md{term.normal} for rules!".format(term=term))
        with term.location(0, 10):
            print("• {term.bold}'D'{term.normal} to draw a card".format(term=term))
        with term.location(0, 11):
            print("• {term.bold}Space{term.normal} to select two cards".format(term=term))
        with term.location(0, 12):
            print("• {term.bold}Enter{term.normal} to clear with drawn card".format(term=term))
        with term.location(0, 13):
            print("• {term.bold}Arrows{term.normal} to move around".format(term=term))
        with term.location(0, 14):
            print("• {term.bold}'Q'{term.normal} to quit".format(term=term))

        if self._game_state is not GameState.RUNNING:
            with term.location(0, term.height - 2):
                print("You've won!" if self._game_state is GameState.WON else "You've lost! You must clear the pyramid before going through the deck next time.")

    def render_undealt(self):
        term = self._terminal
        number_remaining = self._deck.len()
        formatted_remaining = (" " if number_remaining < 10 else "") + str(number_remaining)
        with term.location(1, 0):
            print("{}┌──────┐{}".format(term.blue + term.on_white, term.normal))
        with term.location(1, 1):
            print("{}│      │{}".format(term.blue + term.on_white, term.normal))
        with term.location(1, 2):
            print("{}│  {}  │{}".format(term.blue + term.on_white, formatted_remaining, term.normal))
        with term.location(1, 3):
            print("{}│      │{}".format(term.blue + term.on_white, term.normal))
        with term.location(1, 4):
            print("{}└──────┘{}".format(term.blue + term.on_white, term.normal))
        with term.location(0, 5):
            print(term.normal + "cards left")

    def render_card(self, card, column, row, card_state):
        term = self._terminal

        if card:
            suit = card.suit
            if card_state is CardState.HIDDEN:
                color = term.blue
            elif card_state is CardState.SELECTED:
                color = term.green
            elif card_state is CardState.HIGHLIGHTED:
                color = term.cyan + term.bold
            else:
                color = term.black if suit is Suit.CLUB or suit is Suit.SPADE else term.red

            with term.location(column, row + 0):
                print("{}┌──────┐{}".format(color + term.on_white, term.normal))
            with term.location(column, row + 1):
                print("{}│      │{}".format(color + term.on_white, term.normal))
            with term.location(column, row + 2):
                print("{}│  {}  │{}".format(color + term.on_white, str(card) if card_state is not CardState.HIDDEN else "  ", term.normal))
            with term.location(column, row + 3):
                print("{}│      │{}".format(color + term.on_white, term.normal))
            with term.location(column, row + 4):
                print("{}└──────┘{}".format(color + term.on_white, term.normal) + term.normal)

    def render_pyramid(self):
        term = self._terminal
        dimensions = (34, 12)
        origin = (int((term.width - 8) / 2), term.height - dimensions[1] - 1)
        for (row, cards) in enumerate(self._pyramid.rows):
            row_h_offset = int((dimensions[0] - len(cards) * 9) / 2)
            row_v_offset = row * 2
            for (card_index, card) in enumerate(cards):
                card_h_offset = row_h_offset + 9 * card_index
                self.render_card(card, origin[0] + card_h_offset, origin[1] + row_v_offset, self._pyramid.card_state_at(row, card_index))

    def render_revealed(self):
        term = self._terminal
        for (i, card) in enumerate(self._revealed_cards):
            with term.location(0, 20):
                self.render_card(card, 20 + i, 0, CardState.HIDDEN if i != len(self._revealed_cards) - 1 else CardState.NORMAL)
        with term.location(20, 5):
            print("↑ drawn cards")

    def handle_draw(self):
            card = self._deck.draw()
            if card:
                self._revealed_cards.append(card)
            else:
                self._game_state = GameState.LOST

            return True

    def handle_enter(self):
        highlighted_card = self._pyramid.highlighted_card()
        if highlighted_card.value is Value.KING:
            self._pyramid.clear_highlighted_card()
            if (self._pyramid.highlighted_row, self._pyramid.highlighted_column) == (0, 0):
                self._game_state = GameState.WON
            return True

        top_revealed = self._revealed_cards.pop()
        if top_revealed.value.is_valid_pair(highlighted_card.value):
            self._pyramid.clear_highlighted_card()
            if (self._pyramid.highlighted_row, self._pyramid.highlighted_column) == (0, 0):
                self._game_state = GameState.WON
            return True
        else:
            # reappend
            self._revealed_cards.append(top_revealed)
            return False

    def handle_space(self):
        if len(self._pyramid.selected_cards) > 1:
            return False
        if not self._pyramid.selected_cards:
            self._pyramid.selected_cards.append((self._pyramid.highlighted_row, self._pyramid.highlighted_column))
            return True

        card1 = self._pyramid.selected_cards[0]
        card2 = (self._pyramid.highlighted_row, self._pyramid.highlighted_column)
        if card1 == card2:
            self._pyramid.selected_cards = []
            return True
        if self._pyramid.rows[card1[0]][card1[1]].value.is_valid_pair(self._pyramid.rows[card2[0]][card2[1]].value):
            self._pyramid.clear_card(card1[0], card1[1])
            self._pyramid.clear_card(card2[0], card2[1])
            self._pyramid.selected_cards = []
            if card1 == (0, 0) or card2 == (0, 0):
                self._game_state = GameState.WON
            return True
        else:
            return False


class GameState(Enum):
    RUNNING = 0
    WON = 1
    LOST = 2
