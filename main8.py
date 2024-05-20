import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
from pr8.haffm8 import HuffmanTree, save_codes_to_json, create_text_file, compress_data, load_binary_data, decompress_data, save_binary_data
from pr2.information_metrics import calculate_alphabet_power, calculate_hartley_entropy, calculate_shannon_entropy


class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Coding")

        self.create_widgets()

    def create_widgets(self):
        self.encode_button = tk.Button(self.root, text="Кодировать текст", command=self.encode_text)
        self.encode_button.grid(row=0, column=0, padx=10, pady=10)

        self.decode_button = tk.Button(self.root, text="Декодировать текст", command=self.decode_text)
        self.decode_button.grid(row=0, column=1, padx=10, pady=10)

        self.info_label = tk.Label(self.root, text="Информация о файле")
        self.info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.info_text = tk.Text(self.root, height=15, width=60)
        self.info_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def encode_text(self):
        file_path = filedialog.askopenfilename(title="Выберите файл с текстом")
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл {file_path} не найден.")
            return

        huffman_tree = HuffmanTree(text_content)
        root_node = huffman_tree.build_tree()
        huffman_codes = huffman_tree.generate_codes(root_node)

        compressed_text = compress_data(text_content, huffman_codes)

        save_data = {
            "huffman_tree": huffman_codes,
            "compressed_text": compressed_text
        }
        save_binary_data(compressed_text, 'result.bin')
        save_codes_to_json(save_data)

        alphabet_power = calculate_alphabet_power(text_content)
        shannon_entropy = calculate_shannon_entropy(text_content, alphabet_power)
        hartley_entropy = calculate_hartley_entropy(alphabet_power)

        original_size = os.stat(file_path).st_size
        compressed_size = os.stat("result.bin").st_size
        compression_ratio = original_size / compressed_size
        avg_bits_per_symbol = len(compressed_text) / len(text_content)

        info = (
            f"Размер исходного файла: {original_size} байт\n"
            f"Размер закодированного файла: {compressed_size} байт\n"
            f"Информационная энтропия (Хартли): {hartley_entropy}\n"
            f"Информационная энтропия (Шеннон): {shannon_entropy}\n"
            f"Среднее кол-во бит на символ: {avg_bits_per_symbol}\n"
            f"Степень сжатия: {compression_ratio:.2f}\n"
        )

        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info)
        messagebox.showinfo("Успех", "Код Хаффмана и сжатый текст сохранены в json файле.")

    def decode_text(self):
        file_path = filedialog.askopenfilename(title="Выберите файл с зашифрованным текстом")
        if not file_path:
            return

        try:
            with open("code.json", 'r') as json_file:
                save_data = json.load(json_file)
                huff_codes = save_data["huffman_tree"]

            uncompressed_data = load_binary_data(file_path)
            decoded_text = decompress_data(uncompressed_data, huff_codes)
            create_text_file(decoded_text)

            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Текст успешно декодирован и сохранен в decode.txt.\n")

            messagebox.showinfo("Успех", "Текст успешно декодирован и сохранен.")
        except FileNotFoundError as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}. Проверьте пути к файлам.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при декодировании файла: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()
