from math import log2, pi

def calculate_alphabet_power(text):
    return len(set(text.lower()))

def calculate_hartley_entropy(alphabet_power):
    return log2(alphabet_power)

def calculate_shannon_entropy(text, alphabet_power):
    probabilities = [text.lower().count(char) / len(text) for char in set(text.lower())]
    shannon_entropy = -sum(pi * (log2(pi) if pi > 0 else 0) for pi in probabilities)
    return shannon_entropy

def calculate_redundancy(alphabet_power, shannon_entropy):
    hartley_entropy = calculate_hartley_entropy(alphabet_power)
    redundancy = ((hartley_entropy - shannon_entropy) / hartley_entropy) * 100
    return redundancy