class CrosswordBoard:
    """Represents the crossword board."""
    def __init__(self, size):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]

    def display(self):
        """Displays the current state of the crossword board."""
        for row in self.grid:
            print(' '.join(row))

    def can_place_word(self, word, row, col, direction):
        """
        Checks if a word can be placed at a specific location and direction.
        direction: 0 for horizontal, 1 for vertical.
        """
        if direction == 0:  # Horizontal
            if col + len(word) > self.size:
                return False
            for i in range(len(word)):
                if self.grid[row][col + i] != ' ' and self.grid[row][col + i] != word[i]:
                    return False
        elif direction == 1:  # Vertical
            if row + len(word) > self.size:
                return False
            for i in range(len(word)):
                if self.grid[row + i][col] != ' ' and self.grid[row + i][col] != word[i]:
                    return False
        return True

    def place_word(self, word, row, col, direction):
        """
        Places a word on the board without validation.
        Assumes the generator has already validated the placement.
        direction: 0 for horizontal, 1 for vertical.
        """
        if direction == 0:  # Horizontal
            for i in range(len(word)):
                self.grid[row][col + i] = word[i]
        elif direction == 1:  # Vertical
            for i in range(len(word)):
                self.grid[row + i][col] = word[i]