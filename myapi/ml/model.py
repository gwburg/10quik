import re
import string
import pickle
from bs4 import BeautifulSoup

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.get_logger().setLevel('INFO')
tf.autograph.set_verbosity(0)


LABELS = ['Income Statement', 'Balance Sheet', 'Cash Flows', 'Other']

def get_words(table):
    '''
    Extracts all word content from a BeautifulSoup table
    '''

    #soup = BeautifulSoup(table, 'html.parser')
    rows = table.find_all('tr')
    text = ''
    for row in rows:
        row_text = row.get_text()
        #trans = str.maketrans(dict.fromkeys(string.punctuation.replace('$','')))
        trans = str.maketrans(dict.fromkeys(string.punctuation))
        row_text = row_text.translate(trans)
        matches = re.findall('[a-z][A-Z]|' +
                             '[0-9][A-Za-z]|' +
                             '[A-Za-z][0-9]|' +
                             '[A-Za-z][\u2014\u2019\$]',
                             row_text)
        for match in matches:
            row_text = row_text.replace(match, match[0] + ' ' + match[1])
        text += f' {row_text}'
    words = [word for word in text.split() if word.isalpha()]
    return ' '.join(words)

def vectorize(text):
    vectorizer = pickle.load(open('/home/gwburg/python/get_financials/react/app/myapi/ml/vectorizer.pkl', 'rb'))
    selector = pickle.load(open('/home/gwburg/python/get_financials/react/app/myapi/ml/selector.pkl', 'rb'))

    x_test = vectorizer.transform(text)
    x_test = selector.transform(x_test).astype('float32').todense()
    return x_test

def predict(table):
    words = get_words(table)
    data = vectorize([words])

    model = tf.keras.models.load_model('/home/gwburg/python/get_financials/react/app/myapi/ml/model.h5')
    pred = model(data)
    pred = pred.numpy().tolist()[0]
    label = pred.index(max(pred))
    return LABELS[label], max(pred)
