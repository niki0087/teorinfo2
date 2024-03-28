
from configparser import ConfigParser
from pr6 import haaffman
from pr6 import bitecoder
from pr6 import hemming
from pr6.logger import Logger

# Создаем объект класса Logger
logger = Logger('logfile.log')

# Сохраняем сообщение об ошибке
logger.error('This is an error message.')

# Сохраняем информационное сообщение
logger.info('This is an info message.')

def read_settings():
    """
    Read settings from settings.ini file.
    """
    config = ConfigParser()
    config.read('settings.ini')
    return config

def main():
    """
    Main function to run the program.
    """
    config = read_settings()
    word_size = config.getint('Settings', 'word_size')

    while True:
        print("\nРежим работы:\n1) С текстом;\n2) Выход.\n\nВвод: ", end='')
        try:
            mode = int(input())
        except ValueError:
            print("\nНеверный тип данных.")
            continue

        if mode == 2:
            break

        print("Введите текст: ", end='')
        text = input()
        source_length = len(text)

        # Huffman coding
        huffman_tree = haaffman.HuffmanTree(text)
        root = huffman_tree.build_tree()
        codes = huffman_tree.generate_codes(root)
        encoded_data_byte = bitecoder.save_binary_data(codes, text)

        # Hemming encoding
        hemming_instance = hemming.Hemming()
        encoded_hemming = hemming_instance.encode(encoded_data_byte)


        # Displaying encoded data
        print("\nЗакодированные данные:", encoded_hemming)

        # Adding errors
        print("\nВведите количество ошибок: ", end='')
        try:
            error_count = int(input())
        except ValueError:
            print("\nНеверный тип данных.")
            continue

        encoded_hemming_with_errors = hemming_instance.noise(encoded_hemming, error_count)

        # Decoding Hemming
        decoded_hemming = hemming_instance.decode(encoded_hemming_with_errors)

        # Decoding Huffman
        decoded_data = bitecoder.load_binary_data(codes, decoded_hemming)

        # Displaying decoded data
        print("\nРаскодированный текст:", decoded_data)

        # Logging
        logger.info(f"Исходная длина текста: {source_length}")
        logger.info(f"Длина закодированных данных: {len(encoded_hemming)}")
        logger.info(f"Количество внесенных ошибок: {error_count}")

if __name__ == "__main__":
    main()
