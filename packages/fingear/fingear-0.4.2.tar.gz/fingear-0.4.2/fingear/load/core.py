from .yahoo import load_candles as load_candles_yahoo
from .tinkoff import load_candles as load_candles_tinkoff


from .tinkoff import load_bond_coupons as load_bond_coupons_tinkoff
from .tinkoff import load_bond_info as load_bond_info_tinkoff

import pandas as pd
    

def load_candles(ticker, start, end, interval, core='tinkoff'):
    if core == 'tinkoff':
        return load_candles_tinkoff(ticker, start, end, interval)
    elif core == 'yahoo':
        return load_candles_yahoo(ticker, start, end, interval)
    
def load_asset_price(ticker, start, end, interval, core='tinkoff'):
    candles = load_candles(ticker, start, end, interval, core=core)
    candles = candles[['datetime', 'close']]
    candles.columns = ['dttm', 'price']
    candles.sort_values('dttm', inplace=True)
    return candles

def load_single_price(ticker, date, core='tinkoff'):
    start = pd.to_datetime(date)-pd.DateOffset(days=30) # Тут если не торговались, то грузим раньше
    end = pd.to_datetime(date)+pd.DateOffset(days=1)
    candles = load_candles(ticker, start, end, 'day', core=core)
    price = candles.tail(1)['close'].values[0]
    return price
    


### BOND

def load_bond_info(ticker, core='tinkoff'):
    if core == 'tinkoff':
        return load_bond_info_tinkoff(ticker)
    else:
        raise NotImplementedError
    

def load_bond_coupons(ticker, start, end, core='tinkoff'):
    if core == 'tinkoff':
        return load_bond_coupons_tinkoff(ticker, start, end)
    else:
        raise NotImplementedError