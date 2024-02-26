from pr1.morse import morse_code

def decoder(morsecode):
    """
    Декодирование строки на Азбуке Морзе в строку на Unicode.

    Args:
        morsecode (str): Строка на Азбуке Морзе.

    Returns:
        str: Раскодированная строка на Unicode.
    """
    decoded = ''
    morsecode_list = morsecode.split(' ')
    for item in morsecode_list:
        for key, value in morse_code.items():
            if item == value:
                decoded += key
    return decoded