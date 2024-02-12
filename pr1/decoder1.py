from pr1.morse import morse_code
# функция декодирования строки на Азбуке Морзе в строку на Unicode
def decoder(morsecode):
    decoded = ''
    # переделывает строку в типо массив через ковычки где ключи это символы юникод а значения - азбука морзе
    morsecode_list = morsecode.split(' ')
    for item in morsecode_list:
        for key, value in morse_code.items():
            if item == value:
                decoded += key
    return decoded