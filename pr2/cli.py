from information_metrics import (
    calculate_alphabet_power,
    calculate_shannon_entropy,
    calculate_redundancy,
    calculate_hartley_entropy
)

def main():
    file_name = input("Введите имя файла с текстом: ")
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Файл {file_name} не найден.")
        return

    alphabet_power = calculate_alphabet_power(text)
    shannon_entropy = calculate_shannon_entropy(text, alphabet_power)
    redundancy = calculate_redundancy(alphabet_power, shannon_entropy)

    print(f"Мощность алфавита: {alphabet_power}")
    print(f"Информационная энтропия (Хартли): {calculate_hartley_entropy(alphabet_power)}")
    print(f"Информационная энтропия (Шеннон): {shannon_entropy}")
    print(f"Избыточность алфавита: {redundancy:.2f}%")

if __name__ == "__main__":
    main()
