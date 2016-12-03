# coding: utf-8

import math
import re
import time
from datetime import datetime
from datetime import timedelta
from multiprocessing.pool import Pool, ThreadPool
import pickle
import os
import requests
from functools import partial
from pyquery import PyQuery
import stockcodes
from . import helpers
from . import store
import platform
import pandas as pd



class Day:

    def __init__(self, store_type, path, start_year='1990'):
        self.start_year = start_year
        self.store_type = store_type
        self.path = path

        if store_type == 'csv':
            self.store = store.csvStore(path)
        elif store_type == 'xls':
            self.store = store.xlsStore(path)

        self.is_debug = True if platform.system() == 'Windows' else False

    def init(self):
        stock_codes = self.get_all_stock_codes()
        exists_codes = self.store.get_exists_codes()
        stock_codes = set(stock_codes).difference(exists_codes)

        pool = ThreadPool(4)
        func = partial(self.get_save_stock_history)
        pool.map(func, stock_codes)

    def update(self, force=False):
        """ 更新已经下载的历史数据
        :param force: 不考虑最后更新日期，强制更新
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

    def get_update_day_history(self, stock_code, latest_date):
        pass
    # 获得一只股票的全部历史数据，并保存
    def get_save_stock_history(self, stock_code):
        all_history = self.get_all_history(stock_code)
        if len(all_history) <= 0:
            return
        self.store.write(stock_code, all_history)
        return all_history

    def get_all_history(self, stock_code):
        years = self.get_stock_time(stock_code)
        years = [x for x in years if x >= self.start_year]
        all_history = []
        for year in years:
            year_history = self.get_year_history(stock_code, year)
            all_history += year_history
        all_history.sort(key=lambda day: day[0])
        return all_history

    def get_year_history(self, stock_code, year):
        year_history = []
        now_year = datetime.now().year
        now_month = datetime.now().month
        end_quarter = 5 if str(year) != str(now_year) else math.ceil(now_month / 3) + 1
        for quarter in range(1, end_quarter):
            quarter_data = self.get_quarter_history(stock_code, year, quarter)
            if quarter_data is None:
                continue
            year_history += quarter_data
        return year_history


    @staticmethod
    def convert_stock_data_type(day_data):
        """将获取的对应日期股票数据除了日期之外，转换为正确的 float / int 类型
        :param day_data: ['2016-02-19', '945.019', '949.701', '940.336', '935.653', '31889824.000', '320939648.000', '93.659']
        :return: ['2016-02-19', 945.019, 949.701, 940.336, 935.653, 31889824.000, 320939648.000, 93.659]
        """
        date_index = 0

        for i, val in enumerate(day_data):
            if i == date_index:
                continue
            day_data[i] = float(val)

    @staticmethod
    def get_all_stock_codes():
        return stockcodes.get_stock_codes()
