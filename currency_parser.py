import requests
import json
import xmltodict
import config
from datetime import datetime
import seaborn as sns
import pandas as pd
import logging
import matplotlib.ticker as ticker


# Центральный Банк России - https://www.cbr-xml-daily.ru/daily_json.js
# Центральный Банк Европы - https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml

def get_currency_currate(pair) -> str:
    resp = requests.get('https://currate.ru/api/?',
                        params={"get": "rates", "pairs": pair, "key": config.API_CURRATE_KEY})
    return resp.json()["data"][pair]

def central_russian_bank(input_currency='all', value=1) -> str:
    resp = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    json_resp = resp.json()
    currencies_json_resp = json_resp['Valute']
    if input_currency == 'all':
        all_curr = []
        for currency, curr_d in currencies_json_resp.items():
            all_curr.append(f'RUB -> {curr_d["CharCode"]} {round(1 / int(curr_d["Value"]), 5)} ({curr_d["Name"]})')
        return '\n'.join(all_curr)
    else:
        return f'{value} {input_currency} -> {value * currencies_json_resp[input_currency]["Value"]} RUB'


def get_currency_range(value: str, date1: str, date2=datetime.now().strftime("%d/%m/%Y")) -> list:
    resp = requests.get('http://www.cbr.ru/scripts/XML_dynamic.asp?',
                        params={"date_req1": date1, "date_req2": date2, "VAL_NM_RQ": get_currency_pcode(value)})
    json_resp = json.loads(json.dumps(xmltodict.parse(resp.text)))
    try:
        return json_resp["ValCurs"]["Record"]
    except Exception as E:
        logging.error(f'get_currency_range: {E}')
        return ['error']

def get_currency_pcode(value: str, user_lang=None) -> str:  # 59 currencies
    lang = {'en': 'EngName', 'ru': 'Name'}
    resp = requests.get('http://www.cbr.ru/scripts/XML_valFull.asp')
    json_resp = json.loads(json.dumps(xmltodict.parse(resp.text)))
    currencies_json_resp = json_resp["Valuta"]["Item"]
    currencies_dict = {x["ISO_Char_Code"]: x["ParentCode"] for x in currencies_json_resp}
    if value == 'all':
        return "\n".join([f'▪️{x[lang[user_lang]]}: {x["ISO_Char_Code"]}' for x in currencies_json_resp])
    try:
        return currencies_dict[value]
    except Exception as E:
        logging.error(f'get_currency_pcode: {E}')
        return 'error'

def get_lineplot(currency_range, user_id):
    if currency_range == ['error']:
        logging.error(f"get_lineplot")
        return ['error']
    sns.set(font_scale=0.55)
    data_x = [float(i["Value"].replace(',', '.')) for i in currency_range]
    data_y = [i["@Date"] for i in currency_range]
    data_all = {'value': data_x, 'date': data_y}
    data = pd.DataFrame(data=data_all)
    plot = sns.lineplot(x="date", y="value", data=data, label='value', color='#8944B4')
    plot.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plot.figure.savefig(f"plots/{user_id}_plot.png")
    plot.figure.clf()


if __name__ == '__main__':
    pass
