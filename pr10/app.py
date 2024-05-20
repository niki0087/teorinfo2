import time
import random
from flask import Flask, render_template, request
from hamm import Hamming

app = Flask(__name__)
hamming = Hamming()

@app.route('/')
def root():
    template = 'index.html'
    datestamp = time.asctime(time.localtime(time.time()))
    return render_template(template, datestamp=datestamp)

@app.route('/result', methods=['POST'])
def result():
    textarea_data = request.form['source_data']
    data = hamming.encode(textarea_data)
    return render_template('result.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)