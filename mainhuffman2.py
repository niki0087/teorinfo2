"""
Основной модуль программы для кодирования и декодирования Хаффмана.
"""
from pr5.haffman2 import HuffmanTree, save_codes_to_json

def compress_data(text, huff_codes):
    """
    Сжимает текст, используя коды Хаффмана.

    Parameters:
    - text: Текст, который нужно сжать.
    - huff_codes: Словарь с кодами Хаффмана для символов.

    Returns:
    - compressed_data: Сжатый текст.
    """
    compressed_data = ""
    for char in text:
        compressed_data += huff_codes[char]
    return compressed_data

if __name__ == "__main__":
    while True:
        file_name = input("Введите имя файла с текстом (или введите 'exit' для завершения): ")

        if file_name.lower() == 'exit':
            print("Программа завершена.")
            break

        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                text_content = file.read()
        except FileNotFoundError:
            print(f"Файл {file_name} не найден.")
        else:
            huffman_tree = HuffmanTree(text_content)
            root_node = huffman_tree.build_tree()
            huffman_codes = huffman_tree.generate_codes(root_node)

            # Интеграция compress_data
            compressed_text = compress_data(text_content, huffman_codes)

            # Сохранение кодов Хаффмана и сжатого текста в JSON файл
            save_data = {
                "huffman_tree": huffman_codes,
                "compressed_text": compressed_text
            }

            save_codes_to_json(save_data)
            print("Код Хаффмана и сжатый текст сохранены в json файле.")
            