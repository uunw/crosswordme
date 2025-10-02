class TrieNode:
    """A node in the Trie structure."""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    """Trie structure for storing words."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Inserts a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        """Searches for a word in the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word


class GuessNode:
    """Node to store a guessed word."""
    def __init__(self, word):
        self.word = word
        self.next = None

class GuessList:
    """Linked list to store guessed words."""
    def __init__(self):
        self.head = None

    def add_guess(self, word):
        """Adds a new guess to the list."""
        new_node = GuessNode(word)
        new_node.next = self.head
        self.head = new_node

    def display(self):
        """Prints all the guessed words."""
        current = self.head
        while current:
            print(current.word)
            current = current.next
