# coding:utf-8
import os

import pandas as pd
import talib
from . import store


class Indicator(object):
    def __init__(self, stock_code, history):
        self.stock_code = stock_code
        self.history = history

    def __getattr__(self, item):
        def talib_func(*args, **kwargs):
            str_args = ''.join(map(str, args))
            if self.history.get(item + str_args) is not None:
                return self.history
            func = getattr(talib, item)
            res_arr = func(self.history['close'].values, *args, **kwargs)
            self.history[item + str_args] = res_arr
            return self.history

        return talib_func


class History(object):
    def __init__(self, dtype='D', store_type='csv', path='history'):

        self.market = dict()
        # self.data_path = os.path.join(path, 'day', 'data')

        if dtype != 'D':
            print('not implemented!')
            return
        if store_type == 'csv':
            self.store = store.csvStore(path)
        elif store_type == 'xls':
            self.store = store.xlsStore(path)

        self.load()

        # self.load_csv_files(data_path)

    def load(self):
        self.market = self.store.loadtoHistory()

    def load_csv_files(self, path):
        file_list = [f for f in os.listdir(path) if f.endswith('.csv')]
        for stock_csv in file_list:
            csv_ext_index_start = -4
            stock_code = stock_csv[:csv_ext_index_start]

            csv_path = os.path.join(path, stock_csv)

            self.market[stock_code] = Indicator(stock_code, pd.read_csv(csv_path, index_col='date'))

    def __getitem__(self, item):
        return self.market[item]

    def __setitem__(self, item, value):
        self.market[item] = value
