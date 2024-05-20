class Hamming:
    ...

    def encode(self, data):
        """Кодирует данные методом Хэмминга.

        Args:
            data (str): Данные для кодирования.

        Returns:
            str: Закодированные данные.
        """
        data = list(data)
        m = len(data)
        r = 0
        while (2**r < m + r + 1):
            r += 1

        hamming_code = ['0'] * (m + r)

        j = 0
        for i in range(1, len(hamming_code) + 1):
            if (i & (i - 1)) == 0:
                hamming_code[i - 1] = '0'
            else:
                hamming_code[i - 1] = data[j]
                j += 1

        for i in range(r):
            x = 2**i
            parity = 0
            for j in range(x - 1, len(hamming_code), 2 * x):
                parity ^= sum(int(bit) for bit in hamming_code[j:j + x])
            hamming_code[x - 1] = str(parity % 2)

        return ''.join(hamming_code)