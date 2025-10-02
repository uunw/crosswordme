import random
from crossword import CrosswordBoard

class CrosswordGenerator:
    def __init__(self, words, size):
        self.words = list(words)
        self.size = size
        self.board = CrosswordBoard(size)
        self.solution_words = {}

    def _check_placement(self, word, row, col, direction):
        # 1. Bounds check and check for words sticking together end-to-end
        if direction == 0:  # Horizontal
            if col < 0 or col + len(word) > self.size: return False
            if col > 0 and self.board.grid[row][col - 1] != ' ': return False
            if col + len(word) < self.size and self.board.grid[row][col + len(word)] != ' ': return False
        else:  # Vertical
            if row < 0 or row + len(word) > self.size: return False
            if row > 0 and self.board.grid[row - 1][col] != ' ': return False
            if row + len(word) < self.size and self.board.grid[row + len(word)][col] != ' ': return False

        intersections = 0
        for i in range(len(word)):
            r, c = (row, col + i) if direction == 0 else (row + i, col)

            letter_on_board = self.board.grid[r][c]
            letter_in_word = word[i]

            if letter_on_board == ' ':
                # If cell is empty, perpendicular neighbors must be empty
                if direction == 0: # Placing Horizontal
                    if r > 0 and self.board.grid[r-1][c] != ' ': return False
                    if r < self.size-1 and self.board.grid[r+1][c] != ' ': return False
                else: # Placing Vertical
                    if c > 0 and self.board.grid[r][c-1] != ' ': return False
                    if c < self.size-1 and self.board.grid[r][c+1] != ' ': return False
            else:
                # If cell is not empty, it must be a valid intersection
                if letter_on_board == letter_in_word:
                    # This is an intersection. We must check that we are crossing the other word perpendicularly.
                    if direction == 0: # Placing Horizontal, so existing word must be Vertical
                        is_vertical = (r > 0 and self.board.grid[r-1][c] != ' ') or (r < self.size-1 and self.board.grid[r+1][c] != ' ')
                        if not is_vertical: return False
                    else: # Placing Vertical, so existing word must be Horizontal
                        is_horizontal = (c > 0 and self.board.grid[r][c-1] != ' ') or (c < self.size-1 and self.board.grid[r][c+1] != ' ')
                        if not is_horizontal: return False
                    intersections += 1
                else:
                    return False # Invalid character overlap

        return intersections > 0

    def generate(self):
        if not self.words:
            return self.board.grid, self.solution_words

        # Sort words by length, descending, for a better result
        self.words.sort(key=len, reverse=True)

        # Place the first word in the center
        first_word = self.words.pop(0)
        direction = random.randint(0, 1)
        row = (self.size - (len(first_word) if direction == 1 else 0)) // 2
        col = (self.size - (len(first_word) if direction == 0 else 0)) // 2
        self.board.place_word(first_word, row, col, direction)
        self.solution_words[first_word] = (row, col, direction)

        # Loop until we can't place any more words
        for _ in range(10): # Limit passes to avoid infinite loops
            words_to_place = self.words[:]
            placed_this_round = False
            for word in words_to_place:
                possible_placements = []
                # Find intersections with already placed words
                for placed_word, (p_row, p_col, p_dir) in self.solution_words.items():
                    for i_placed, char_placed in enumerate(placed_word):
                        for i_new, char_new in enumerate(word):
                            if char_placed == char_new:
                                # Potential intersection found
                                if p_dir == 0:  # Placed is horizontal, new must be vertical
                                    new_dir = 1
                                    new_row = p_row - i_new
                                    new_col = p_col + i_placed
                                else:  # Placed is vertical, new must be horizontal
                                    new_dir = 0
                                    new_row = p_row + i_placed
                                    new_col = p_col - i_new

                                if self._check_placement(word, new_row, new_col, new_dir):
                                    possible_placements.append({'r': new_row, 'c': new_col, 'd': new_dir})

                if possible_placements:
                    placement = random.choice(possible_placements)
                    self.board.place_word(word, placement['r'], placement['c'], placement['d'])
                    self.solution_words[word] = (placement['r'], placement['c'], placement['d'])
                    self.words.remove(word)
                    placed_this_round = True

            if not placed_this_round:
                break  # Stop if we can't place any more words in a full pass

        return self.board.grid, self.solution_words
