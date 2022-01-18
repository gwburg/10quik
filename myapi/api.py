import asyncio

import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

from myapi.utils.constant import user_agent
from myapi.finder import Finder
from myapi.converter import Converter

@app.route('/api/companies', methods=['GET'])
def get_companies():
    companies = requests.get('https://sec.gov/files/company_tickers.json', headers={'user-agent': user_agent}).json()
    companies = list(companies.values())
    return jsonify(
        companies=companies
    )

@app.route('/api/filings-data', methods=['POST'])
def get_data():
    url = request.json
    data = requests.get(url, headers={'user-agent': user_agent}).json()
    recent = data["filings"]["recent"]
    files = data["filings"]["files"]
    return jsonify(
        recent=recent,
        files=files
    )

@app.route('/api/filing-html', methods=['POST'])
def get_html():
    url = request.json
    r = requests.get(url, headers={'user-agent': user_agent})
    html = r.text
    return jsonify(
        html=html
    )

@app.route('/api/filing-html-modified', methods=['POST'])
def modify_html():
    url = request.json
    r = requests.get(url, headers={'user-agent': user_agent})
    html = r.text

    soup = BeautifulSoup(html, 'html.parser')
    all_tables = soup.find_all('table')
    for i,table in enumerate(all_tables):
        if '$' in table.get_text():
            if 'class' not in table.attrs:
                table['class'] = f'{i}'
            else:
                table['class'] += f' {i}'
            button = new_button(soup, str(i))
            table.insert_before(button)

    all_imgs = soup.find_all('img')
    base_url = '/'.join(url.split('/')[:-1])
    for img in all_imgs:
        img['src'] = f"{base_url}/{img['src']}"

    finder = Finder()
    found_tables = finder.find(all_tables)
    for label, table in found_tables.items():
        table['id'] = f'{label.replace(" ","")}'
        if 'class' not in table.attrs:
            table['class'] = f'{label.replace(" ","")}'
        else:
            table['class'] += f' {label.replace(" ","")}'

    html = str(soup)
    return jsonify(
        html=html
    )

def new_button(soup, label):
    button = soup.new_tag('button')
    button['class'] = 'tableButton btn btn-primary'
    button['id'] = f'{label.replace(" ","")}Button'
    button.string = f'To Excel'
    return  button

@app.route('/api/convert-excel', methods=['POST'])
def convert():
    html = request.json
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    conv = Converter(html)
    conv.convert()
    conv.upload()
    return ('', 204)
