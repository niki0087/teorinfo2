"""
Основной модуль программы для кодирования и декодирования Хаффмана.
"""
import os
import json
from pr5.haffman2 import HuffmanTree, save_codes_to_json, create_text_file, compress_data, load_binary_data, decompress_data
from pr2.information_metrics import calculate_alphabet_power, calculate_hartley_entropy, calculate_shannon_entropy
from pr5.haffman2 import save_binary_data
def display_menu():
    """

    Returns:
        _type_: _description_
    """

    print("Выберите действие:")
    print("1. Кодировать текст")
    print("2. Декодировать текст")
    print("3. Выйти")
    choice = input("Введите номер выбранного действия: ")
    return choice

if __name__ == "__main__":
    while True:
        choice = display_menu()

        if choice == '1':
            file_name = input("Введите имя файла с текстом: ")
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    text_content = file.read()
            except FileNotFoundError:
                print(f"Файл {file_name} не найден.")
                continue

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
            save_binary_data(compressed_text, 'result.bin')
            save_codes_to_json(save_data)
            alphabet_power = calculate_alphabet_power(text_content)
            shannon_entropy = calculate_shannon_entropy(text_content, alphabet_power)
            print("Код Хаффмана и сжатый текст сохранены в json файле.")
            #print(f"Мощность алфавита: {alphabet_power}")
            print(f"Информационная энтропия (Хартли): {calculate_hartley_entropy(alphabet_power)}")
            print(f"Информационная энтропия (Шеннон): {shannon_entropy}")
            print("Размер исходного файла:", os.stat("example.txt").st_size)
            print("Размер закодированного файла:", os.stat("result.bin").st_size)
            print("Степень сжатия:", ((os.stat("example.txt").st_size)/(os.stat("result.bin").st_size)))
            print("среднее кол-во бит на символ: ", ((len(compressed_text))/(len(text_content))))

        elif choice == '2':
            file_path = input("Введите имя файла с зашифрованным текстом: ")
            try:
                with open("code.json", 'r') as json_file:
                    huff_codes = json.load(json_file)

                with open(file_path, 'rb') as file:
                    compresset_data = file.read()
                
                uncompressed_data = load_binary_data(file_path)
                decoded_text= decompress_data(uncompressed_data, huffman_codes)
                create_text_file(decoded_text)
                print("Текст успешно декодирован и сохранен.")
            except FileNotFoundError as e:
                print(f"Ошибка: {e}. Проверьте пути к файлам.")
            except Exception as e:
                print(f"Ошибка при декодировании файла: {e}")

        elif choice == '3':
            print("Программа завершена.")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")
