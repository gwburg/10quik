from unicodedata import normalize

import requests

from myapi.filings import Quarterlies
from myapi.parsers import TableCollector
from myapi.utils.constant import user_agent
from myapi.converter import Converter


ticker = 'jpm'
conv = None
print('getting links...')
q = Quarterlies(ticker, recent_only=True)
link = q.links()[0]
r = requests.get(link, headers={'user-agent': user_agent})
html = str(r.content)
collector = TableCollector()
collector.feed(html)
tables = collector.tables

def my_code_test(num):
    global conv
    global tables

    table = tables[num]
    table = normalize('NFKD', table).replace('\\n','').replace('\\t','')
    conv = Converter(table, compress=True)
    #for row in conv.rows:
    #    print(row)
    return conv
