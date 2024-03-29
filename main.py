import requests
import json
from datetime import datetime
import utils
import config
import time 

def get_symbol_prices(symbol, exchanges):
    symbol_result = dict()
    for exchange, url in exchanges.items():
        exchange_symbol = exchange+f'_{symbol}'
        try:
            price = requests.get(url)   
            price = price.json()
            price = utils.parse_response(exchange, price)
            symbol_result[exchange_symbol] = price
            if not isinstance(price, float):
                symbol_result[exchange_symbol] = f'{exchange} failed'
        except:
            symbol_result[exchange_symbol] = f'{exchange} failed'
            continue
    symbol_result = utils.filter_dict(symbol_result)
    key_median = f'{symbol}_MEDIAN'
    symbol_result[key_median] = utils.calculate_median(symbol_result)
    return symbol_result
    
while True:
    result = dict()
    
    for symbol, exchanges in config.symbols.items():
        symbol_result = get_symbol_prices(symbol, exchanges)
        result.update(symbol_result)
    file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"
    with open(file_name, 'w') as json_file:
        json.dump(result, json_file, indent=4)
    time.sleep(60)