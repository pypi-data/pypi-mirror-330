import yfinance as yf
import pandas as pd

# [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
def interval_transcription():
    transcription =  {
        '1m': '1m',
        '2m': '2m',
        #'3m': '2m',
        '5m': '5m',
        #'10m': CandleInterval.CANDLE_INTERVAL_10_MIN,
        '15m': '15m',
        '30m': '30m',
        '1h': '1h',
        #'2h': 'ERR',
        #'4h': 'ERR'
        'day': '1d',
        '5d': '5d', # NO Tinkoff
        'week': '1wk',
        'month': '1mo',
    }
    return transcription

def transcript_interval(interval):
    return interval_transcription()[interval]


def load_exchange_rate(currency, start, end, interval):
    start = pd.to_datetime(start).strftime('%Y-%m-%d')
    end = pd.to_datetime(end).strftime('%Y-%m-%d')
    data = yf.download(f'{currency}=X', start=start, end=end, 
                       progress=False, interval=transcript_interval(interval))

    data = pd.DataFrame(data.reset_index().values, columns = ['dt', 'close', 'high', 'low', 'open', 'volume'])
    data = data[['dt', 'close']]
    data.columns = ['dt', 'rate']
    return data

def load_candles(ticker, start, end, interval):
    start = pd.to_datetime(start).strftime('%Y-%m-%d')
    end = pd.to_datetime(end).strftime('%Y-%m-%d')
    data = yf.download(ticker, start=start, end=end, 
                       progress=False, interval=transcript_interval(interval))
    print(data)
    data = pd.DataFrame(data.reset_index().values, columns = ['datetime', 'close', 'high', 'low', 'open', 'volume'])
    data = data[['datetime', 'open', 'close', 'low', 'high', 'volume']]
    return data