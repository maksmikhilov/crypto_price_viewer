kukoin_url =  'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol='
kraken_url = 'https://api.kraken.com/0/public/Ticker?pair='
binance_url = 'https://api.binance.com/api/v3/ticker/price?symbol='
commex_url = 'https://api.commex.com/api/v1/ticker/24hr?symbol='

def coinbase_url(symbol):
    # BTC-USDT
    return f'https://api.coinbase.com/v2/prices/{symbol}/spot'
    
def poloniex_url(symbol):
    # BTC_USDT
    return f'https://api.poloniex.com/markets/{symbol}/price'

symbols = {
    'USDTRUB': {
        'COINBASE': coinbase_url('USDT-RUB'),
        'BINANCE': binance_url+'USDTRUB',
        'COMMEX': commex_url+'USDTRUB'
    },
    'XMRUSDT': {
        'KRAKEN': kraken_url+'XMRUSDT',
        'COINBASE': coinbase_url('XMR-USDT'),
        'KUKOIN': kukoin_url+'XMR-USDT',
        'POLONIEX': poloniex_url('XMR_USDT')
    },
    'BTCUSDT': {
        'KRAKEN': kraken_url+'BTCUSDT',
        'COINBASE': coinbase_url('BTC-USDT'),
        'BINANCE': binance_url+'BTCUSDT',
        'COMMEX': commex_url+'BTCUSDT',
        'KUKOIN': kukoin_url+'BTC-USDT',
        'POLONIEX': poloniex_url('BTC_USDT')
    },
    'XMRBTC': {
        'KRAKEN': kraken_url+'XMRBTC',
        'COINBASE': coinbase_url('XMR-BTC'),
        'POLONIEX': poloniex_url('XMR_BTC'),
        'KUKOIN': kukoin_url+'XMR-BTC'
    }
}






