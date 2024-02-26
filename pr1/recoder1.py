from pr1.morse import morse_code

def coder(text):
    """
    Кодирование строки на Unicode в строку на Азбуке Морзе.

    Args:
        text (str): Строка на Unicode.

    Returns:
        str: Закодированная строка на Азбуке Морзе.
    """
    encoded = ''
    for char in text.upper():
        if char in morse_code:
            encoded += morse_code[char] + " "
    return encoded
