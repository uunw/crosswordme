import sys
import pygame
import random
import os
from generator import CrosswordGenerator
from crossword import CrosswordBoard
from data_structures import Trie, GuessList
from ui import Button, InputBox

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Crossword Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 30)
        self.grid_letter_font = pygame.font.Font(None, 36)

        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.grid_color = (200, 200, 200)
        self.button_color = (100, 100, 100)
        self.button_hover_color = (150, 150, 150)
        self.hint_button_color = (80, 80, 80)

        # Game state
        self.game_state = "main_menu"
        self.difficulty = "medium"
        self.grid_size = 15
        self.score = 0
        self.timer_duration = 180
        self.start_time = 0
        self.solution_words = {}
        self.pause_time = 0
        self.feedback_text = None
        self.feedback_timer = 0
        self.feedback_duration = 1000
        self.is_pre_win = False
        self.pre_win_timer = 0
        self.pre_win_duration = 1000

        # Main menu buttons
        self.start_button = Button(300, 250, 200, 50, "Start Game", self.button_color, self.button_hover_color)
        self.options_button = Button(300, 320, 200, 50, "Options", self.button_color, self.button_hover_color)
        self.quit_button = Button(300, 390, 200, 50, "Quit", self.button_color, self.button_hover_color)
        self.menu_buttons = [self.start_button, self.options_button, self.quit_button]

        # Options menu buttons
        self.easy_button = Button(300, 200, 200, 50, "Easy", self.button_color, self.button_hover_color)
        self.medium_button = Button(300, 270, 200, 50, "Medium", self.button_color, self.button_hover_color)
        self.hard_button = Button(300, 340, 200, 50, "Hard", self.button_color, self.button_hover_color)
        self.difficulty_back_button = Button(300, 410, 200, 50, "Back", self.button_color, self.button_hover_color)
        self.options_buttons = [self.easy_button, self.medium_button, self.hard_button, self.difficulty_back_button]

        # In-game buttons
        self.hint_button = Button(self.screen_width - 120, 70, 100, 50, "Hint", self.hint_button_color, self.button_hover_color)

        # Pause menu buttons
        self.yes_button = Button(250, 300, 100, 50, "Yes", self.button_color, self.button_hover_color)
        self.no_button = Button(450, 300, 100, 50, "No", self.button_color, self.button_hover_color)
        self.pause_buttons = [self.yes_button, self.no_button]

        # Settings
        self.hint_cost = 5
        self.word_solve_score = 10

        # Settings screen buttons
        self.hint_cost_minus_button = Button(450, 200, 40, 40, "-", self.button_color, self.button_hover_color)
        self.hint_cost_plus_button = Button(550, 200, 40, 40, "+", self.button_color, self.button_hover_color)
        self.word_score_minus_button = Button(450, 270, 40, 40, "-", self.button_color, self.button_hover_color)
        self.word_score_plus_button = Button(550, 270, 40, 40, "+", self.button_color, self.button_hover_color)
        self.timer_minus_button = Button(450, 340, 40, 40, "-", self.button_color, self.button_hover_color)
        self.timer_plus_button = Button(550, 340, 40, 40, "+", self.button_color, self.button_hover_color)
        self.back_button = Button(300, 450, 200, 50, "Back", self.button_color, self.button_hover_color)
        self.settings_buttons = [
            self.hint_cost_minus_button, self.hint_cost_plus_button,
            self.word_score_minus_button, self.word_score_plus_button,
            self.timer_minus_button, self.timer_plus_button,
            self.back_button
        ]


    def main_menu(self):
        while self.game_state == "main_menu":
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.start_button.is_clicked(event):
                    self.game_state = "difficulty_select"
                if self.options_button.is_clicked(event):
                    self.game_state = "options_screen"
                if self.quit_button.is_clicked(event):
                    pygame.quit()
                    sys.exit()
                
                for button in self.menu_buttons:
                    button.is_clicked(event) # Update click state

            self.screen.fill(self.white)
            title_text = self.font.render("Crossword Game", True, self.black)
            self.screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 150))

            for button in self.menu_buttons:
                button.check_hover(mouse_pos)
                button.draw(self.screen, self.button_font)

            pygame.display.flip()

    def _load_words(self, difficulty):
        wordlist_path = os.path.join("src", "wordlists", f"{difficulty}.txt")
        with open(wordlist_path, "r") as f:
            words = [line.strip().upper() for line in f.readlines()]
        # Take a random sample of words to make it more varied
        max_words = 10
        if len(words) > max_words:
            words = random.sample(words, max_words)
        return words

    def start_game(self):
        # Reset win state from previous game
        self.is_pre_win = False
        self.pre_win_timer = 0

        if self.difficulty == "easy":
            self.grid_size = 10
        elif self.difficulty == "medium":
            self.grid_size = 15
        else: # hard
            self.grid_size = 20
            
        words = self._load_words(self.difficulty)
        
        # Keep generating until we have a board with at least 3 words, with a limit
        self.solution_grid, self.solution_words = {}, {}
        attempts = 0
        while len(self.solution_words) < 3 and attempts < 20: # Limit attempts to prevent freezing
            generator = CrosswordGenerator(words, self.grid_size)
            self.solution_grid, self.solution_words = generator.generate()
            attempts += 1

        # Dynamically calculate cell size to fit the grid on screen
        top_margin_ui = 130
        bottom_margin_ui = 80
        side_margin_ui = 50
        
        grid_area_width = self.screen_width - (side_margin_ui * 2)
        grid_area_height = self.screen_height - top_margin_ui - bottom_margin_ui

        if self.grid_size == 0: self.grid_size = 1
        cell_size_w = grid_area_width // self.grid_size
        cell_size_h = grid_area_height // self.grid_size
        self.cell_size = min(cell_size_w, cell_size_h)

        grid_font_size = int(self.cell_size * 0.75)
        self.grid_letter_font = pygame.font.Font(None, grid_font_size)

        grid_pixel_width = self.grid_size * self.cell_size
        grid_pixel_height = self.grid_size * self.cell_size

        self.grid_margin_x = (self.screen_width - grid_pixel_width) // 2
        self.grid_margin_y = top_margin_ui + (grid_area_height - grid_pixel_height) // 2

        self.board = CrosswordBoard(self.grid_size)
        self.word_trie = Trie()
        self.guess_list = GuessList()

        # Reveal a few starting letters
        num_revealed = 0
        if self.solution_words:
            placed_words = list(self.solution_words.keys())
            random.shuffle(placed_words)
            
            revealed_coords = set()

            for word in placed_words:
                if num_revealed >= 3:
                    break
                
                # Try to reveal a letter from this word
                indices = list(range(len(word)))
                random.shuffle(indices)
                
                for char_index in indices:
                    info = self.solution_words[word]
                    row, col, direction = info
                    
                    if direction == 0: # Horizontal
                        reveal_row, reveal_col = row, col + char_index
                    else: # Vertical
                        reveal_row, reveal_col = row + char_index, col

                    if (reveal_row, reveal_col) not in revealed_coords:
                        self.board.grid[reveal_row][reveal_col] = self.solution_grid[reveal_row][reveal_col]
                        revealed_coords.add((reveal_row, reveal_col))
                        num_revealed += 1
                        break # Move to the next word

        for word in self.solution_words.keys():
            self.word_trie.insert(word)

        self.input_box = InputBox(self.screen_width // 2 - 150, self.screen_height - 70, 300, 50)

    def game_loop(self):
        while self.game_state == "playing":
            # Handle pre-win delay
            if self.is_pre_win:
                self.pre_win_timer += 1
                if self.pre_win_timer >= self.pre_win_duration:
                    self.game_state = "win"
                    return # Exit game_loop to transition to win_screen
            
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            remaining_time = self.timer_duration - elapsed_time
            if remaining_time <= 0 and not self.is_pre_win:
                self.game_state = "game_over"

            # Check for words completed on the board (e.g. by hints) and add to guess list
            guessed_words_set = set()
            current = self.guess_list.head
            while current:
                guessed_words_set.add(current.word)
                current = current.next

            for word, (row, col, direction) in self.solution_words.items():
                if word not in guessed_words_set:
                    is_complete = True
                    # Check if the word is now fully on the board
                    for i, char in enumerate(word):
                        if direction == 0:
                            r, c = row, col + i
                        else:
                            r, c = row + i, col
                        
                        if not (0 <= r < self.grid_size and 0 <= c < self.grid_size) or self.board.grid[r][c] != char:
                            is_complete = False
                            break
                    
                    if is_complete:
                        self.guess_list.add_guess(word)
                        guessed_words_set.add(word) # Add to the set for the current frame's win check

            # Check for win condition
            if not self.is_pre_win and set(self.solution_words.keys()).issubset(guessed_words_set):
                self.is_pre_win = True


            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not self.is_pre_win:
                    submitted_word = self.input_box.handle_event(event)
                    if submitted_word:
                        word = submitted_word.upper()

                        if word in guessed_words_set:
                            self.input_box.trigger_error()
                            self.feedback_text = self.font.render("Already found!", True, (255, 165, 0)) # Orange
                            self.feedback_timer = self.feedback_duration
                        elif self.word_trie.search(word) and word in self.solution_words:
                            self.guess_list.add_guess(word)
                            self.score += self.word_solve_score

                            # Reveal the word on the player's board
                            row, col, direction = self.solution_words[word]
                            if direction == 0:
                                for i in range(len(word)):
                                    self.board.grid[row][col + i] = word[i]
                            else:
                                for i in range(len(word)):
                                    self.board.grid[row + i][col] = word[i]
                        else:
                            self.input_box.trigger_error()
                            self.feedback_text = self.font.render("Incorrect!", True, (255, 0, 0))
                            self.feedback_timer = self.feedback_duration

                        self.input_box.text = '' # Clear the input box

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.game_state = "paused"
                            self.pause_time = pygame.time.get_ticks()

                    if self.hint_button.is_clicked(event):
                        if self.score >= self.hint_cost:
                            # Find unguessed words
                            guessed_words = set()
                            current = self.guess_list.head
                            while current:
                                guessed_words.add(current.word)
                                current = current.next
                            
                            unguessed_words = [word for word in self.solution_words.keys() if word not in guessed_words]

                            if unguessed_words:
                                possible_hints = []
                                for word in unguessed_words:
                                    row, col, direction = self.solution_words[word]
                                    for i, char in enumerate(word):
                                        if direction == 0: # Horizontal
                                            r, c = row, col + i
                                        else: # Vertical
                                            r, c = row + i, col
                                        
                                        if self.board.grid[r][c] == ' ':
                                            possible_hints.append((r, c))
                                
                                if possible_hints:
                                    self.score -= self.hint_cost # Deduct score only if a hint is given
                                    
                                    # Pick a random hidden letter to reveal
                                    hint_row, hint_col = random.choice(possible_hints)
                                    self.board.grid[hint_row][hint_col] = self.solution_grid[hint_row][hint_col]

            self.screen.fill(self.white)
            self.draw_grid(self.board, self.grid_size, self.cell_size, self.grid_margin_x, self.grid_margin_y, self.solution_grid)
            self.draw_guesses(self.guess_list)
            self.draw_score()
            self.draw_timer(remaining_time)
            self.draw_difficulty()

            self.hint_button.check_hover(mouse_pos)
            self.hint_button.draw(self.screen, self.button_font)
            self.input_box.update()
            self.input_box.draw(self.screen)

            # Draw feedback message
            if self.feedback_timer > 0:
                self.feedback_timer -= 1
                if self.feedback_text:
                    text_rect = self.feedback_text.get_rect(center=(self.input_box.rect.centerx, self.input_box.rect.y - 30))
                    self.screen.blit(self.feedback_text, text_rect)

            # Draw "You Win!" message during pre-win state
            if self.is_pre_win:
                overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 180)) # White, semi-transparent
                self.screen.blit(overlay, (0, 0))

                win_text = self.font.render("You Win!", True, self.black)
                text_rect = win_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
                self.screen.blit(win_text, text_rect)

            pygame.display.flip()

    def draw_grid(self, board, grid_size, cell_size, grid_margin_x, grid_margin_y, solution_grid):
        for row in range(board.size):
            for col in range(board.size):
                if solution_grid[row][col] != ' ':
                    rect = pygame.Rect(grid_margin_x + col * cell_size, grid_margin_y + row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(self.screen, self.black, rect, 1)
                    if board.grid[row][col] != '?' and board.grid[row][col] != ' ':
                        text = self.grid_letter_font.render(board.grid[row][col], True, self.black)
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)

    def draw_guesses(self, guess_list):
        y_offset = 50
        current = guess_list.head
        while current:
            text = self.font.render(current.word, True, self.black)
            self.screen.blit(text, (50, y_offset))
            y_offset += 30
            current = current.next

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, self.white)
        bg_rect = pygame.Rect(self.screen_width - score_text.get_width() - 40, 10, score_text.get_width() + 20, score_text.get_height() + 10)
        pygame.draw.rect(self.screen, self.button_color, bg_rect)
        self.screen.blit(score_text, (self.screen_width - score_text.get_width() - 30, 15))

    def draw_timer(self, time_left):
        mins = time_left // 60
        secs = time_left % 60
        timer_text = self.font.render(f"Time: {mins:02d}:{secs:02d}", True, self.white)
        bg_rect = pygame.Rect(10, 10, timer_text.get_width() + 20, timer_text.get_height() + 10)
        pygame.draw.rect(self.screen, self.button_color, bg_rect)
        self.screen.blit(timer_text, (20, 15))

    def draw_difficulty(self):
        difficulty_text = self.font.render(self.difficulty.upper(), True, self.black)
        self.screen.blit(difficulty_text, (20, 60))

    def options_menu(self):
        while self.game_state in ["options", "difficulty_select"]:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "main_menu"

                if self.difficulty_back_button.is_clicked(event):
                    self.game_state = "main_menu"

                if self.easy_button.is_clicked(event):
                    self.difficulty = "easy"
                    self.start_game()
                    self.game_state = "playing"
                    self.start_time = pygame.time.get_ticks()
                if self.medium_button.is_clicked(event):
                    self.difficulty = "medium"
                    self.start_game()
                    self.game_state = "playing"
                    self.start_time = pygame.time.get_ticks()
                if self.hard_button.is_clicked(event):
                    self.difficulty = "hard"
                    self.start_game()
                    self.game_state = "playing"
                    self.start_time = pygame.time.get_ticks()

                for button in self.options_buttons:
                    button.is_clicked(event)

            self.screen.fill(self.white)
            options_text = self.font.render("Select Difficulty", True, self.black)
            self.screen.blit(options_text, (self.screen_width // 2 - options_text.get_width() // 2, 120))

            for button in self.options_buttons:
                button.check_hover(mouse_pos)
                button.draw(self.screen, self.button_font)

            pygame.display.flip()
    def options_screen(self):
        while self.game_state == "options_screen":
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.back_button.is_clicked(event):
                    self.game_state = "main_menu"
                
                if self.hint_cost_minus_button.is_clicked(event):
                    self.hint_cost = max(0, self.hint_cost - 1)
                if self.hint_cost_plus_button.is_clicked(event):
                    self.hint_cost += 1
                
                if self.word_score_minus_button.is_clicked(event):
                    self.word_solve_score = max(1, self.word_solve_score - 1)
                if self.word_score_plus_button.is_clicked(event):
                    self.word_solve_score += 1

                if self.timer_minus_button.is_clicked(event):
                    self.timer_duration = max(30, self.timer_duration - 30)
                if self.timer_plus_button.is_clicked(event):
                    self.timer_duration += 30

            self.screen.fill(self.white)
            title_text = self.font.render("Options", True, self.black)
            self.screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))

            # Draw labels and values
            hint_cost_label = self.button_font.render("Hint Cost:", True, self.black)
            self.screen.blit(hint_cost_label, (250, 210))
            hint_cost_value = self.font.render(str(self.hint_cost), True, self.black)
            self.screen.blit(hint_cost_value, (510 - hint_cost_value.get_width() // 2, 205))

            word_score_label = self.button_font.render("Word Score:", True, self.black)
            self.screen.blit(word_score_label, (250, 280))
            word_score_value = self.font.render(str(self.word_solve_score), True, self.black)
            self.screen.blit(word_score_value, (510 - word_score_value.get_width() // 2, 275))

            timer_label = self.button_font.render("Timer (secs):", True, self.black)
            self.screen.blit(timer_label, (250, 350))
            timer_value = self.font.render(str(self.timer_duration), True, self.black)
            self.screen.blit(timer_value, (510 - timer_value.get_width() // 2, 345))

            for button in self.settings_buttons:
                button.check_hover(mouse_pos)
                button.draw(self.screen, self.font)

            pygame.display.flip()

    def game_over_screen(self):
        while self.game_state == "game_over":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_state = "main_menu"

            self.screen.fill(self.white)
            game_over_text = self.font.render("Game Over", True, self.black)
            score_text = self.font.render(f"Final Score: {self.score}", True, self.black)
            restart_text = self.font.render("Press Enter to return to Main Menu", True, self.black)
            self.screen.blit(game_over_text, (self.screen_width // 2 - game_over_text.get_width() // 2, 200))
            self.screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, 250))
            self.screen.blit(restart_text, (self.screen_width // 2 - restart_text.get_width() // 2, 300))
            pygame.display.flip()

    def win_screen(self):
        while self.game_state == "win":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_state = "main_menu"

            self.screen.fill(self.white)
            win_text = self.font.render("You Win!", True, self.black)
            score_text = self.font.render(f"Final Score: {self.score}", True, self.black)
            restart_text = self.font.render("Press Enter to return to Main Menu", True, self.black)
            self.screen.blit(win_text, (self.screen_width // 2 - win_text.get_width() // 2, 200))
            self.screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, 250))
            self.screen.blit(restart_text, (self.screen_width // 2 - restart_text.get_width() // 2, 300))
            pygame.display.flip()

    def pause_menu(self):
        while self.game_state == "paused":
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "playing"
                        self.start_time += pygame.time.get_ticks() - self.pause_time
                
                if self.yes_button.is_clicked(event):
                    self.game_state = "main_menu"
                if self.no_button.is_clicked(event):
                    self.game_state = "playing"
                    self.start_time += pygame.time.get_ticks() - self.pause_time

            self.screen.fill(self.white)
            pause_text = self.font.render("Return to Main Menu?", True, self.black)
            self.screen.blit(pause_text, (self.screen_width // 2 - pause_text.get_width() // 2, 200))

            for button in self.pause_buttons:
                button.check_hover(mouse_pos)
                button.draw(self.screen, self.button_font)

            pygame.display.flip()

    def run(self):
        while True:
            if self.game_state == "main_menu":
                self.main_menu()
            elif self.game_state == "difficulty_select":
                self.options_menu()
            elif self.game_state == "options":
                self.options_menu()
            elif self.game_state == "options_screen":
                self.options_screen()
            elif self.game_state == "playing":
                self.game_loop()
            elif self.game_state == "paused":
                self.pause_menu()
            elif self.game_state == "game_over":
                self.game_over_screen()
            elif self.game_state == "win":
                self.win_screen()

if __name__ == "__main__":
    game = Game()
    game.run()