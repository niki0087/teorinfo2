from pr1.coder import coder
from pr1.decoder import decoder

def main():
    while True:
        print("Выберите действие:")
        print("1. Кодирование текста в азбуку Морзе")
        print("2. Декодирование азбуки Морзе в текст")
        print("3. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            text = input("Введите текст для кодирования: ")
            encoded = coder(text)
            print(f"Закодированный текст: {encoded}")
        elif choice == "2":
            morsecode = input("Введите код азбуки Морзе для декодирования: ")
            decoded = decoder(morsecode)
            print(f"Раскодированный текст: {decoded}")
        elif choice == "3":
            print("Программа завершена.")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

main()