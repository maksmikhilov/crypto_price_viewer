import statistics
def parse_response(exchange, data):
    if exchange == 'BINANCE':
        return float(data['price'])
    if exchange == 'COINBASE':
        return float(data['data']['amount'])
    if exchange == 'KUKOIN':
        return float(data['data']['price'])
    if exchange == 'KRAKEN':
        return float(data['result'][list(data['result'])[0]]['c'][0])
    if exchange == 'COMMEX':
        return float(data['lastPrice'])
    if exchange == 'POLONIEX':
        return float(data['price'])
        
def calculate_deviation(data_dict, key):
    other_values = [value for k, value in data_dict.items() if k != key]
    mean_without_current = sum(other_values) / len(other_values)
    deviation = abs((data_dict[key] - mean_without_current) / mean_without_current) * 100
    return deviation
    
def filter_dict(data_dict):
    filtered_dict = data_dict.copy()
    for key in data_dict:
        deviation = calculate_deviation(data_dict, key)
        if deviation > 3:
            filtered_dict[key] = 'Deviation more 3%'
    return filtered_dict

def calculate_median(data_dict):
    prices = [price for exchange_symbol, price in data_dict.items() if isinstance (price,float)]
    return statistics.median(prices)