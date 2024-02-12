from pr1.morse import morse_code
# функция кодирования из Unicode в Азбуку Морзе
def  coder(text):
    encoded = ''
    # возведение в верхний регистр всех символов в строке
    for char in text.upper():
        if char in morse_code:
            encoded += morse_code[char]
        return encoded
    encoded = ''
    for char in text.upper():
        if char in morse_code:
            encoded += morse_code[char] + " "
    return encoded