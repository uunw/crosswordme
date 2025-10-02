# Crossword Puzzle Game

This is a crossword puzzle game built with Python and Pygame.

## Project Structure

- **`src/`**: Contains all the Python source code.
  - [`main.py`](src/main.py): The main game engine.
  - [`generator.py`](src/generator.py): The crossword generation logic.
  - [`crossword.py`](src/crossword.py): The `CrosswordBoard` class.
  - [`data_structures.py`](src/data_structures.py): The `Trie` and `GuessList` classes.
  - [`ui.py`](src/ui.py): The `Button` and `InputBox` classes.
  - [`layouts.py`](src/layouts.py): Contains the word lists for the different difficulty levels.
  - [`layouts.json`](src/layouts.json): Contains the pre-generated crossword layouts.
  - **`wordlists/`**: Contains the word lists for different difficulty levels.
    - [`easy.txt`](src/wordlists/easy.txt)
    - [`medium.txt`](src/wordlists/medium.txt)
    - [`hard.txt`](src/wordlists/hard.txt)
- [`generate_layouts.py`](generate_layouts.py): A script to pre-generate the crossword layouts.
- [`README.md`](README.md): This file.
- [`pyproject.toml`](pyproject.toml): Project configuration file.
- [`uv.lock`](uv.lock): Lock file for the `uv` package manager.
- [`.gitignore`](.gitignore): Specifies which files to ignore in Git.
- [`.python-version`](.python-version): Specifies the Python version for the project.

## How to Run

To run the game, execute the following command in your terminal:

```bash
uv run python src/main.py
```

## Game Logic

The game is built around a `Game` class in [`main.py`](src/main.py) that manages the game state and the main game loop. The game has several states:

- `main_menu`: The initial screen with options to start, view options, or quit.
- `difficulty_select`: A screen to choose the difficulty level (Easy, Medium, or Hard).
- `options`: A placeholder for a future options screen.
- `playing`: The main game screen where the crossword is displayed and the player can input words.
- `paused`: A screen that appears when the game is paused, with options to resume or return to the main menu.
- `game_over`: A screen that appears when the timer runs out.
- `win`: A screen that appears when the player correctly guesses all the words.

### Crossword Generation

The game uses a `CrosswordGenerator` class in [`generator.py`](src/generator.py) to create the crossword puzzles. To avoid performance issues and crashes, the crossword layouts are pre-generated and saved to [`layouts.json`](src/layouts.json). The `generate_layouts.py` script is used to create this file.

The generator takes a list of words and a grid size, and it places the words on the grid in a simple intersecting pattern.

### Data Structures

The game uses the following data structures:

- **Trie:** A `Trie` (from [`data_structures.py`](src/data_structures.py)) is used to store the dictionary of valid words for each difficulty level. This allows for efficient searching and validation of the player's guesses.
- **Linked List:** A `GuessList` (from [`data_structures.py`](src/data_structures.py)) is used to store the words that the player has correctly guessed.
- **Array:** A 2D array is used to represent the crossword grid.

### UI

The UI is built with Pygame and consists of several components:

- **Buttons:** The `Button` class in [`ui.py`](src/ui.py) is used to create clickable buttons for the menus.
- **Input Box:** The `InputBox` class in [`ui.py`](src/ui.py) provides a text input field for the player to enter their guesses. It includes a blinking cursor for a better user experience.
