class Node:
    """
    Class docstring here.
    """
    def __init__(self, left, right):
        """
        Initialize a new instance of the Node class.

        Parameters:
        - left: The left child node.
        - right: The right child node.
        """
        self.left = left
        self.right = right

class HuffmanTree:
    """
    Class docstring here.
    """
    def __init__(self, text):
        """
        Initialize a new instance of the HuffmanTree class.

        Parameters:
        - text: The input text for Huffman coding.
        """
        self.text = text
        self.letters = set(text)
        self.frequencies = [(text.count(letter), letter) for letter in self.letters]

    def build_tree(self):
        """
        Build Huffman tree.
        """
        while len(self.frequencies) > 1:
            self.frequencies = sorted(self.frequencies, key=lambda x: x[0], reverse=True)
            first = self.frequencies.pop()
            second = self.frequencies.pop()
            freq = first[0] + second[0]
            self.frequencies.append((freq, Node(first[1], second[1])))
        return self.frequencies[0][1]

    def generate_codes(self, node, path='', code=None):
        """
        Generate Huffman codes.
        """
        if code is None:
            code = {}
        if isinstance(node, str):
            code[node] = path
            return code
        code = self.generate_codes(node.left, path + '0', code)
        code = self.generate_codes(node.right, path + '1', code)
        return code