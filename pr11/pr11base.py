"""_summary_"""

def text_transform(text, key, n):
    """_summary_

    Args:
        text (_type_): _description_
        key (_type_): _description_
        n (_type_): _description_

    Returns:
        _type_: _description_
    """
    result = ""
    for char in text:
        if char.isalpha():
            shift = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift + key) % n + shift)
        else:
            result += char
    return result

def encrypt_decrypt(input_queue, output_queue):
    """_summary_

    Args:
        input_queue (_type_): _description_
        output_queue (_type_): _description_
    """
    while True:
        text, key, n, action = input_queue.get()
        if action == "encrypt":
            result = text_transform(text, key, n)
        elif action == "decrypt":
            result = text_transform(text, -key, n)
        output_queue.put(result)
        input_queue.task_done()
