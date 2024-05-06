def save_binary_data(code, data):
    """
    Save binary data.
    """
    source_data = ''

    for letter in data:
        source_data += code[letter]

    source_data = source_data + '0' * (8 - (len(source_data) % 8))
    source_data_byte = bytearray([int(source_data[i * 8:i * 8 + 8], 2) for i in range(int(len(source_data) / 8))])
    return source_data_byte

def load_binary_data(code, data):
    """Encrypt data"""
    #read_data = ''.join(['{:0>8}'.format(str(bin(item))[2:]) for item in data])
    result_data = ''

    while data:
        size_before = len(data)

        for k, v in code.items():
            if data[0:len(v)] == v:
                result += k
                data = data[len(v):len(data)]

        if size_before == len(data):
            break

    return result_data