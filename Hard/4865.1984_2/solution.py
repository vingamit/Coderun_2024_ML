class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, text):
        node = self.root
        for i in range(len(text)):
            current_node = node
            for j in range(i, len(text)):
                if text[j] in current_node.children:
                    current_node = current_node.children[text[j]]
                    if current_node.is_end_of_word:
                        return True
                else:
                    break
        return False

def main():
    n, m = map(int, input().split())
    
    trie = Trie()
    for _ in range(n):
        stop_word = input().strip()
        trie.insert(stop_word)
    
    for _ in range(m):
        message = input().strip()
        if trie.search(message):
            print("DELETE")
        else:
            print("KEEP")

if __name__ == "__main__":
    main()