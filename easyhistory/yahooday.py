# coding: utf-8

from datetime import datetime
from datetime import timedelta
from multiprocessing.pool import Pool, ThreadPool
import pickle
import os
from functools import partial
import stockcodes
from . import yahoostore
import platform
import pandas as pd
# import pandas.io.data as yahoo
import pandas_datareader.data as yahoo


class YahooDay:

    def __init__(self, store_type, path, start_year='1990'):
        self.start_year = start_year
        self.store_type = store_type
        self.path = path

        if store_type == 'csv':
            self.store = yahoostore.csvStore(path)

        self.is_debug = True if platform.system() == 'Windows' else False

    def init(self):
        stock_codes = self.get_yahoo_stock_codes()
        exists_codes = self.store.get_exists_codes()
        stock_codes = set(stock_codes).difference(exists_codes)

        # pool = ThreadPool(4)
        # func = partial(self.out_stock_history)
        # pool.map(func, stock_codes)
        for stock_code in stock_codes:
            self.out_stock_history(stock_code)
    def update(self, force=False):
        """ 更新已经下载的历史数据
        :return:
        """
        try:
            with open(os.path.join(self.path, "last_upd_info.pkl"), "rb") as f:
                last_upd_info = pickle.load(f)
                store_type = last_upd_info[0]
                path = last_upd_info[1]
                last_upd_time = last_upd_info[2]

                if (not force) and store_type == self.store_type \
                        and path == self.path \
                        and datetime.now() - last_upd_time < timedelta(hours=1):
                    return
        except:
            pass

        stock_codes = self.store.get_exists_codes()

        pool = Pool(4)
        func = partial(self.update_single_code)
        pool.map(func, stock_codes)

        last_upd_info = (self.store_type, self.path, datetime.now())

        with open(os.path.join(self.path, "last_upd_info.pkl"), "wb") as f:
            pickle.dump(last_upd_info, f)

    def update_single_code(self, stock_code):
        """ 更新对应的股票文件历史行情
        :param stock_code: 股票代码
        :return:
        """
        latest_date = self.store.get_last_update_date(stock_code)
        updated_data = self.get_update_day_history(stock_code, latest_date)
        self.store.update_stock(stock_code, updated_data)

    def get_update_day_history(self, stock_code, from_date):

        from_date_s = from_date.strftime('%D')
        to_date_s = datetime.now().strftime('%D')

        df = yahoo.get_data_yahoo(stock_code, from_date_s, to_date_s)
        df.index.name = 'date'
        del df['Adj Close']
        df.columns = ['open', 'high', 'low', 'close', 'volume']
        df['amount'] = df['volume']
        df['factor'] = 1;
        return df

    # 获得一只股票的全部历史数据，并保存
    def out_stock_history(self, stock_code):
        all_history = self.get_all_history(stock_code)
        if len(all_history) <= 0:
            return
        self.store.write(stock_code, all_history)
        return all_history

    def get_all_history(self, stock_code):

        from_date_s = '1/1/{}'.format(self.start_year)
        to_date_s = datetime.now().strftime('%D')  # %D:  formate: 1/30/2016

        df = yahoo.get_data_yahoo(stock_code, from_date_s, to_date_s)
        df.index.name = 'date'
        del df['Adj Close']
        df.columns = ['open', 'high', 'low', 'close', 'volume']
        df['amount'] = df['volume']
        df['factor'] = 1;

        return df

    @staticmethod
    def convert_stock_data_type(day_data):
        """ 将获取的对应日期股票数据除了日期之外，转换为正确的 float / int 类型
        :param day_data: ['2016-02-19', '945.019', '949.701', '940.336', '935.653', '31889.000', '32093.000', '93.659']
        :return: ['2016-02-19', 945.019, 949.701, 940.336, 935.653, 31889824.000, 320939648.000, 93.659]
        """
        date_index = 0

        for i, val in enumerate(day_data):
            if i == date_index:
                continue
            day_data[i] = float(val)

    @staticmethod
    def get_yahoo_stock_codes():
        return stockcodes.get_yahoo_stock_codes()
