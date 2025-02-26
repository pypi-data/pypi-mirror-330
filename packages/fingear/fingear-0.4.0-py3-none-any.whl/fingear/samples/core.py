import pandas as pd
import os

def _join_module_path(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

def ticker_sample(country):
    """
    country in ['Japan', 'Russia', 'USA']
    """
    if country == 'Japan':
        return pd.read_pickle(_join_module_path('data/japan_stocks.pkl'))
    if country == 'Russia':
        return pd.read_pickle(_join_module_path('data/russia_stocks.pkl'))
    if country == 'USA':
        return pd.read_pickle(_join_module_path('data/usa_stocks.pkl'))
    raise "country should be in ['Japan', 'Russia', 'USA']"