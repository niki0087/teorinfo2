import os
import logging
from pr5.haffman2 import HuffmanTree, Node
from pr6.hemming import Hamming

# Проверка наличия файла logfile.log и его создание, если не существует
if not os.path.exists("logfile.log"):
    with open("logfile.log", "w") as file:
        file.write("Log file created.\n")

# Настройка логгера
logging.basicConfig(filename='logfile.log', level=logging.INFO)

def menu():
    """Отображает главное меню и обрабатывает выбор пользователя."""
    while True:
        print("1. Кодировать")
        print("2. Декодировать")
        print("3. Выход")
        choice = input("Выберите операцию (1/2/3): ")
        if choice == '1':
            data = input("Введите данные для кодирования: ")
            
            # Создаем объект HuffmanTree и строим дерево
            huffman = HuffmanTree(data)
            tree = huffman.build_tree()
            
            # Генерируем коды Хаффмана
            huff_codes = huffman.generate_codes(tree)
            
            # Кодируем данные
            encoded_huffman = Node.compress_data(data, huff_codes)
            print("Закодированные данные Хаффмана:", encoded_huffman)
            
            # Кодируем данные с помощью кода Хэмминга
            hamming = Hamming()
            encoded_hamming = hamming.encode(encoded_huffman)
            print("Закодированные данные Хэмминга:", encoded_hamming)
            
            # Логгирование
            logging.info("Huffman encoding: {}".format(encoded_huffman))
            logging.info("Hamming encoding: {}".format(encoded_hamming))
        elif choice == '2':
            encoded_data = input("Введите закодированные данные: ")
            
            # Декодируем данные с помощью кода Хэмминга
            hamming = Hamming()
            decoded_hamming = hamming.decode(encoded_data)
            print("Декодированные данные Хэмминга:", decoded_hamming)
            
            # Создаем объект HuffmanTree и строим дерево
            huffman = HuffmanTree(decoded_hamming)
            tree = huffman.build_tree()
            
            # Генерируем коды Хаффмана
            huff_codes = huffman.generate_codes(tree)
            
            # Декодируем данные
            decoded_huffman = Node.decompress_data(decoded_hamming, huff_codes)
            print("Декодированные данные Хаффмана:", decoded_huffman)
            
            # Логгирование
            logging.info("Hamming decoding: {}".format(decoded_hamming))
            logging.info("Huffman decoding: {}".format(decoded_huffman))
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор операции.")

if __name__ == "__main__":
    menu()
