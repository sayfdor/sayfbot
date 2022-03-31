import requests
import json
import xmltodict

# Центральный Банк России - https://www.cbr-xml-daily.ru/daily_json.js
# Центральный Банк Европы - https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml

# Парсинг курса рубля к другим валютам с сайта Центрального Банка России
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

# Парсинг курса евро к другим валютам с сайта Центрального Банка Европы
def central_european_bank() -> str:
    all_curr = []
    resp = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
    json_resp = json.loads(json.dumps(xmltodict.parse(resp.text)))
    currencies_json_resp = json_resp["gesmes:Envelope"]["Cube"]["Cube"]["Cube"]
    for currency in currencies_json_resp:
        all_curr.append(f'EUR -> {currency["@currency"]} {currency["@rate"]}')
    return '\n'.join(all_curr)


if __name__ == '__main__':
    pass
