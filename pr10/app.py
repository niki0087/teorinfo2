"""_summary_

    Returns:
        _type_: _description_
"""
import time
from flask import Flask, render_template, request
from hemming import Hamming
from haffman2 import HuffmanTree, Node

app = Flask(__name__)
hamming = Hamming()

@app.route('/')
def root():
    """_summary_

    Returns:
        _type_: _description_
    """
    template = 'index.html'
    datestamp = time.asctime(time.localtime(time.time()))
    return render_template(template, datestamp=datestamp)

@app.route('/result', methods=['POST'])
def result():
    """_summary_

    Returns:
        _type_: _description_
    """
    textarea_data = request.form['source_data']
    # Кодирование Хаффмана
    huffman_tree = HuffmanTree(textarea_data)
    huffman_tree.build_tree()
    huff_codes = huffman_tree.generate_codes(huffman_tree.build_tree()) \
          # Используем build_tree() для получения корневого узла
    encoded_huffman = Node.compress_data(textarea_data, huff_codes)
    # Кодирование Хэмминга
    encoded_hamming = hamming.encode(encoded_huffman)
    return render_template('result.html', data=encoded_hamming)


if __name__ == '__main__':
    app.run(debug=True)
