from pr1.recoder1 import coder
from pr1.decoder1 import decoder

def read_text_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print("Файл не найден.")
        return None

def morse_code_converter():
    while True:
        print("Выберите действие:")
        print("1. Кодирование текста в азбуку Морзе")
        print("2. Декодирование азбуки Морзе в текст")
        print("3. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            while True:
                choice_input = input("Выберите способ ввода текста:\n 1. Ввести текст вручную\n 2. Загрузить текст из файла\nВведите номер: ")
                if choice_input == "1":
                    text = input("Введите текст: ")
                    encoded = coder(text)
                    print(f"Закодированный текст: {encoded}")
                    break
                elif choice_input == "2":
                    file_name = input("Введите название файла: ")
                    text = read_text_from_file(file_name)
                    if text:
                        encoded = coder(text)
                        print(f"Закодированный текст: {encoded}")
                        break
                else:
                    print("Некорректный ввод. Попробуйте снова.")

        elif choice == "2":
            while True:
                choice_input = input("Выберите способ ввода текста:\n 1. Ввести текст вручную\n 2. Загрузить текст из файла\nВведите номер: ")
                if choice_input == "1":
                    text = input("Введите текст: ")
                    decoded = decoder(text)
                    print(f"Раскодированный текст: {decoded}")
                    break
                elif choice_input == "2":
                    file_name = input("Введите название файла: ")
                    text = read_text_from_file(file_name)
                    if text:
                        decoded = decoder(text)
                        print(f"Раскодированный текст: {decoded}")
                        break
                else:
                    print("Некорректный ввод. Попробуйте снова.")

        elif choice == "3":
            print("Программа завершена.")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

if __name__ == '__main__':
    morse_code_converter()