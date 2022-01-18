import requests

from myapi.utils.constant import tickers, base_url, user_agent


class FilingsInfo:
    '''
    Gets filings json data for given stock ticker
    '''

    def __init__(self, ticker, recent_only):
        ticker = ticker.upper().replace('.','-')
        if ticker not in tickers:
            raise UnknownTickerError(ticker)
        
        self.ticker = ticker
        self.cik = tickers[ticker]['cik_str'] # unique identifier for stock
        self.data = self._get_all_filings(recent_only)

    def _get_json(self, url):
        return requests.get(url, headers={'user-agent': user_agent}).json()

    def _get_all_filings(self, recent_only):
        ''' 
        Pulls recent and older filings json and returns a list of dicts

        Using a list of dicts rather than combining 
        all dicts into one is probably much faster
        '''

        url = f'{base_url}{self.cik:010d}'
        filings = []

        # initial json data has info for recent filings only
        initial_json = self._get_json(f'{url}.json')
        recent_filings = initial_json['filings']['recent']
        filings.append(recent_filings)
    
        # initial json data also provides urls to older filings
        if not recent_only:
            old_files = initial_json['filings']['files']
            for _file in old_files:
                path = _file['name'].split('-',1)[1]
                old_filings = self._get_json(f'{url}-{path}')
                filings.append(old_filings)

        return filings

    def collect_quarterlies(self):
        quarterlies = []
        for d in self.data:
            indexes = self._indexes(d, ['10-Q','10-K'])
            for i in indexes:
                type_ = d['form'][i]
                #date = d['filingDate'][i]
                date = d['reportDate'][i]
                link = self._build_link(d, i)
                quarterlies.append(Filing(type_, date, link))
        return quarterlies

    def _indexes(self, data, filing_type):
        forms = data['form']
        return [i for i in range(len(forms)) if forms[i] in filing_type]

    def _build_link(self, data, index):
        base = f'https://www.sec.gov/Archives/edgar/data/{self.cik}'
        doc = data['primaryDocument'][index]
        num = data['accessionNumber'][index]
        if doc:
            link = f'{base}/{num.replace("-","")}/{doc}'
        else:
            link = f'{base}/{num}.txt'
        return link


class Filing:
    def __init__(self, type_, date, link):
        self.type = type_
        self.date = date
        self.link = link


class UnknownTickerError(Exception):
    def __init__(self, ticker):
        message = f'{ticker} is not a valid ticker'
        super().__init__(message)
