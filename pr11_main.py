"""_summary_
"""

import queue
import threading
from pr11 import pr11base

def main():
    """_summary_
    """
    input_queue = queue.Queue()
    output_queue = queue.Queue()

    encrypt_thread = threading.Thread(target=pr11base.encrypt_decrypt,
                                      args=(input_queue, output_queue))
    encrypt_thread.daemon = True
    encrypt_thread.start()

    while True:
        print("Выберите действие:")
        print("1. Зашифровать текст")
        print("2. Расшифровать текст")
        print("3. Выход")
        choice = input(" ")

        if choice == "1":
            text = input("Введите текст для шифрования: ")
            key = int(input("Введите ключ шифра: "))
            n = int(input("Введите мощность алфавита (не менее 1104): "))
            input_queue.put((text, key, n, "encrypt"))
            encrypted_text = output_queue.get()
            print("Зашифрованный текст:", encrypted_text)

        elif choice == "2":
            text = input("Введите текст для расшифрования: ")
            key = int(input("Введите ключ шифра: "))
            n = int(input("Введите мощность алфавита (не менее 1104): "))
            input_queue.put((text, key, n, "decrypt"))
            decrypted_text = output_queue.get()
            print("Расшифрованный текст:", decrypted_text)

        elif choice == "3":
            break

        else:
            print("Некорректный выбор. Попробуйте еще раз.")

    input_queue.join()

if __name__ == "__main__":
    main()
