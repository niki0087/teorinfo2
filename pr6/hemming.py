import random

class Hemming:
    """
    Hemming encoding and decoding class.
    """
    def encode(self, data):
        """
        Encode data using Hemming code.

        Args:
            data (str): The input data.

        Returns:
            str: The encoded data.
        """
        m = len(data)
        r = 1
        while 2 ** r <= m + r + 1:
            r += 1

        encoded_data = ['0'] * (m + r)

        j = 0
        for i in range(1, m + r + 1):
            if i & (i - 1) != 0:
                encoded_data[i - 1] = str(data[j])  # Convert to string
                j += 1

        for i in range(r):
            parity_pos = 2 ** i - 1
            parity = 0
            for j in range(parity_pos, m + r, 2 ** (i + 1)):
                for k in range(parity_pos, min(parity_pos + 2 ** i, m + r), 1):
                    if k < m + r:
                        parity ^= int(encoded_data[k])

            encoded_data[parity_pos] = str(parity)

        return ''.join(encoded_data)

    def decode(self, encoded_data):
        """
        Decode data using Hemming code.

        Args:
            encoded_data (str): The encoded data.

        Returns:
            str: The decoded data.
        """
        r = 1
        while 2 ** r <= len(encoded_data):
            r += 1

        syndrome = 0
        for i in range(r):
            parity_pos = 2 ** i - 1
            parity = 0
            for _ in range(parity_pos, len(encoded_data), 2 ** (i + 1)):
                for k in range(parity_pos, min(parity_pos + 2 ** i, len(encoded_data)), 1):
                    if k < len(encoded_data) and encoded_data[k].isdigit():  # Check if it's a digit
                        parity ^= int(encoded_data[k])

            syndrome += parity * (2 ** i)

        if syndrome == 0:
            return encoded_data[:-r]

        index = syndrome - 1
        corrected_encoded_data = list(encoded_data)
        corrected_encoded_data[index] = str(1 - int(corrected_encoded_data[index]))
        return ''.join(corrected_encoded_data)

    def noise(self, data, error_count):
        """
        Introduce errors into the data.

        Args:
            data (str): The input data.
            error_count (int): The number of errors to introduce.

        Returns:
            str: The data with introduced errors.
        """
        indices = random.sample(range(len(data)), error_count)
        noisy_data = list(data)
        for index in indices:
            noisy_data[index] = str(1 - int(noisy_data[index]))
        return ''.join(noisy_data)
