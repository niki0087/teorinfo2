"""
Docsrting modul.
"""
from pr4.haffman import HuffmanTree
from pr4.haffman import save_codes_to_json

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

            save_codes_to_json(huffman_codes)
            print("Код Хаффмана сохранен в json файле.")