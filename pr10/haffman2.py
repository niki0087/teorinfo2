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

    @staticmethod
    def compress_data(text, huff_codes):
        """
        Compress data using Huffman coding.

        Args:
            text (str): The input text to compress.
            huff_codes (dict): The Huffman codes.

        Returns:
            str: The compressed data.
        """
        compressed_data = ""
        for char in text:
            compressed_data += huff_codes[char]
        return compressed_data

    @staticmethod
    def decompress_data(compressed_data, huff_codes):
        """
        Декодирует бинарные данные с использованием Huffman-кодирования.

        Args:
            compressed_data (str): Бинарные данные для декодирования.
            huff_codes (dict): Словарь, содержащий коды Хаффмана.

        Returns:
            str: Раскодированные данные.
        """
        decoded_data = ""
        current_code = ""

        for bit in compressed_data:
            current_code += str(bit)
            if current_code in huff_codes.values():
                decoded_data += next(symbol for symbol, code in huff_codes.items() if code == current_code)
                current_code = ""

        return decoded_data


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


def save_codes_to_json(data):
    """
    Save Huffman codes and compressed text to a JSON file.

    Parameters:
    - data: The data to be saved, including Huffman codes and compressed text.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    target_folder = "/home/admin/teorinfo2/teorinfo2/pr5"
    delete_folders_by_pattern(target_folder, r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}')
    folder_path = os.path.join(target_folder, timestamp)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "code.json")

    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)
    except OSError as e:
        print(f"An error occurred while saving data to json: {e}")


def create_text_file(decoded_data):
    """
    Create a text file with decoded data in the specified directory.

    Parameters:
    - decoded_data: The decoded text data.

    """
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    target_folder = "/home/admin/teorinfo2/teorinfo2/pr5"
    delete_folders_by_pattern(target_folder, r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}')
    folder_path = os.path.join(target_folder, timestamp)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "decode.txt")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(decoded_data)
    except OSError as e:
        print(f"An error occurred while saving decoded text to file: {e}")


def save_binary_data(source_data, file_path):
    """
    Save binary data to a file.

    Args:
        source_data (str): The source data to save.
        file_path (str): The file path to save the data to.
    """
    source_data = source_data + '0' * (8 - (len(source_data) % 8))
    source_data_byte = bytearray([int(source_data[i * 8:i * 8 + 8], 2) for i in range(int(len(source_data) / 8))])
    with open(file_path, 'wb') as file:
        file.write(source_data_byte)


def load_binary_data(file_path):
    """
    Load binary data from a file.

    Args:
        file_path (str): The file path to load the data from.

    Returns:
        str: The loaded binary data.
    """
    with open(file_path, 'rb') as file:
        result_data_byte = file.read()
    result_data = ''.join(['{:08b}'.format(byte) for byte in result_data_byte])
    return result_data
