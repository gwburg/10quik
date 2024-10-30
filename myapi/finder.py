from unicodedata import normalize

#from myapi.parsers import TableCollector
from myapi.ml import model


class Finder:
    '''
    Classifies html tables into Income Statement, Balance Sheet, Cash Flows, Other
    '''

    #def __init__(self, html):
    #    collector = TableCollector()
    #    collector.feed(html)
    #    self.all_tables = collector.tables
    #    self.tables = {'Income Statement': [], 'Balance Sheet': [], 'Cash Flows': [], 'Other': []}
    #    self.find()
    def __init__(self):
        pass

    def find(self, tables):
        categories = {'Income Statement': [], 'Balance Sheet': [], 'Cash Flows': [], 'Other': []}
        for table in tables:
            #table = normalize('NFKD', table).replace('\\n','').replace('\\t','')
            #table = table.text
            label, conf = model.predict(table) 
            categories[label].append((conf, table))
            if categories['Income Statement'] and categories['Balance Sheet'] and categories['Cash Flows']:
                break
        return self._trim_tables(categories)

    def _trim_tables(self, categorized_tables):
#        for label,lst in categorized_tables:
#            lst = sorted(lst, key = lambda item: float(item[0]), reverse = True)
#            categorized_tables[label] = lst
        trimmed = {}
        for label in categorized_tables:
            if label == 'Other':
                continue
            max_conf = 0
            likely_table = None
            for conf, table in categorized_tables[label]:
                if conf > max_conf:
                    max_conf = conf
                    likely_table = table
            if likely_table:
                trimmed[label] = likely_table
        return trimmed
