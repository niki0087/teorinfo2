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

def compress_data(text, huff_codes):
    """

    Args:
        text (_type_): _description_
        huff_codes (_type_): _description_

    Returns:
        _type_: _description_
    """
    compressed_data = ""
    for char in text:
        compressed_data += huff_codes[char]
    return compressed_data

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

def decompress_data(file_path, huff_codes):
    """
    Декодирует бинарные данные с использованием Huffman-кодирования.

    Args:
        file_path (str): Путь к бинарному файлу для декодирования.
        huff_codes (dict): Словарь, содержащий коды Хаффмана.

    Returns:
        str: Раскодированные данные.
    """
    with open(file_path, 'rb') as file:
        compressed_text = file.read()
    compressed_bits = ''.join(format(byte, '08b') for byte in compressed_text)

    decoded_data = ""
    temp_code = ""
    
    for bit in compressed_bits:
        temp_code += bit
        if temp_code in huff_codes:
            decoded_data += huff_codes[temp_code]
            temp_code = ""

    return decoded_data


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
    Args:
        source_data (_type_): _description_
        file_path (_type_): _description_
    """
    source_data = source_data + '0' * (8 - (len(source_data) % 8))
    source_data_byte = bytearray([int(source_data[i * 8:i * 8 + 8], 2) for i in range(int(len(source_data) / 8))])
    with open(file_path, 'wb') as file:
        file.write(source_data_byte)

def load_binary_data(file_path):
    """

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(file_path, 'rb') as file:
        result_data_byte = file.read()
    result_data = ''.join(['{:0>8}'.format(str(bin(item))[2:]) for item in result_data_byte])
    return result_data