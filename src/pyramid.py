from src.deck import CardState


class Pyramid:
    def __init__(self, deck):
        self.rows = []
        for i in range(4):
            row = []
            for j in range(i + 1):
                row.append(deck.draw())
            self.rows.append(row)
        self.highlighted_row = 3
        self.highlighted_column = 0
        self.selected_cards = []

    def left(self):
        if self.highlighted_column == 0:
            return
        next_card = self.previous_nonhidden_card(self.highlighted_row, self.highlighted_column)
        if next_card:
            self.highlighted_column = next_card[1]

    def right(self):
        if self.highlighted_column == 3:
            return
        next_card = self.next_nonhidden_card(self.highlighted_row, self.highlighted_column)
        if next_card:
            self.highlighted_column = next_card[1]

    def up(self):
        if self.highlighted_row == 0:
            return
        for row in range(self.highlighted_row - 1, -1, -1):
            next_card = self.next_nonhidden_card(row, -1)
            if next_card:
                self.highlighted_column = next_card[1]
                self.highlighted_row = next_card[0]
                break

    def down(self):
        if self.highlighted_row == 3:
            return
        for row in range(self.highlighted_row + 1, len(self.rows)):
            next_card = self.next_nonhidden_card(row, -1)
            if next_card:
                self.highlighted_column = next_card[1]
                self.highlighted_row = next_card[0]

    def highlighted_card(self):
        return self.rows[self.highlighted_row][self.highlighted_column]

    def clear_card(self, row, column):
        self.rows[row][column] = None

    def clear_highlighted_card(self):
        self.clear_card(self.highlighted_row, self.highlighted_column)
        if (self.highlighted_row, self.highlighted_column) in self.selected_cards:
            self.selected_cards = []

    def card_state_at(self, row, column):
        if not self.rows[row][column]:
            # card doesn't exist
            return None
        if row != 3:
            if self.rows[row + 1][column]:
                return CardState.HIDDEN
            if self.rows[row + 1][column + 1]:
                return CardState.HIDDEN
        if (row, column) in self.selected_cards:
            return CardState.SELECTED
        return CardState.HIGHLIGHTED if row == self.highlighted_row and column == self.highlighted_column else CardState.NORMAL

    def next_nonhidden_card(self, row, starting_col):
        for column in range(starting_col + 1, len(self.rows[row])):
            card_state = self.card_state_at(row, column)
            if card_state and card_state is not CardState.HIDDEN:
                return (row, column)
        return None

    def previous_nonhidden_card(self, row, starting_col):
        for column in range(starting_col - 1, -1, -1):
            card_state = self.card_state_at(row, column)
            if card_state and card_state is not CardState.HIDDEN:
                return (row, column)
        return None
