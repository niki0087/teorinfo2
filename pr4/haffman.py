class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class HuffmanTree:
    def __init__(self, text):
        self.text = text
        self.letters = set(text)
        self.frequencies = [(text.count(letter), letter) for letter in self.letters]

    def build_tree(self):
        while len(self.frequencies) > 1:
            self.frequencies = sorted(self.frequencies, key=lambda x: x[0], reverse=True)
            first = self.frequencies.pop()
            second = self.frequencies.pop()
            freq = first[0] + second[0]
            self.frequencies.append((freq, Node(first[1], second[1])))
        return self.frequencies[0][1]

    def generate_codes(self, node, path='', code=None):
        if code is None:
            code = {}
        if isinstance(node, str):
            code[node] = path
            return code
        code = self.generate_codes(node.left, path + '0', code)
        code = self.generate_codes(node.right, path + '1', code)
        return code

if __name__ == "__main__":
    file_name = input("Введите имя файла: ")

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Файл {file_name} не найден.")
    else:
        huffman_tree = HuffmanTree(text)
        root_node = huffman_tree.build_tree()
        codes = huffman_tree.generate_codes(root_node)

        print(codes)