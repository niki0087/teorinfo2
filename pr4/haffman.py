"""
Module docstring here.
"""

import json
from datetime import datetime
import os
import re
import shutil

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

def delete_folders_by_pattern(base_folder, pattern):
    """
    Delete folders based on the provided pattern.

    Parameters:
    - base_folder: The base folder where deletion will be performed.
    - pattern: The regular expression pattern for matching folder names.
    """
    try:
        for folder_name in os.listdir(base_folder):
            folder_path = os.path.join(base_folder, folder_name)
            if os.path.isdir(folder_path) and re.match(pattern, folder_name):
                shutil.rmtree(folder_path)
    except OSError as e:
        print(f"An error occurred while deleting folders: {e}")

def save_codes_to_json(codes):
    """
    Save Huffman codes to a JSON file.

    Parameters:
    - codes: The Huffman codes to be saved.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    target_folder = "/home/admin/teorinfo2/teorinfo2/pr4"
    delete_folders_by_pattern(target_folder, r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}')
    folder_path = os.path.join(target_folder, timestamp)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "code.json")

    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(codes, json_file, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"An error occurred while saving codes to json: {e}")
