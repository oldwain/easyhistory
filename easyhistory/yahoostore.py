import os
import json
import csv
import pandas as pd
from datetime import datetime,timedelta

from .history2 import Indicator
from . import helpers


class Store:
    def __init__(self):
        pass

    def init(self, store_type='csv', path='history'):
        pass

    def get_exists_codes(self):
        pass

    def write(self, stock_code, data):
        pass

    def load(self, stock_code):
        pass

    def loadtoHistory(self):
        pass


class csvStore(Store):
    def __init__(self, path):
        super(csvStore, self).__init__()
        self.store_type = 'csv'
        self.root_path = path

        daypath = os.path.join(self.root_path, 'day')
        self.result_path = os.path.join(daypath, 'data')
        self.raw_path = os.path.join(daypath, 'raw_data')

    #
    # 获得信息类
    #
    def get_exists_codes(self):
        if os.path.exists(self.result_path):
            exists_codes = [code[:-4] for code in os.listdir(self.raw_path) if code.endswith('.csv')]
        else:
            exists_codes = set()

        return exists_codes

    def get_last_update_date(self, stock_code):
        summary_path = os.path.join(self.raw_path, '{}_summary.json'.format(stock_code))
        #        try:
        with open(summary_path) as f:
            summary = json.load(f)
        latest_date = datetime.strptime(summary['date'], '%Y-%m-%d')
        return latest_date

    #
    # 保存相关
    #

    def write(self, stock_code, data):
        # print(data)
        self.write_stock_data(stock_code, data, 'data')
        self.write_summary_data(stock_code, data)

    # 保存股票数据， fuquan='raw' 保存原始数据， fuquan='data' 保存还原后的数据
    def write_stock_data(self, stock_code, history, Fuquan='data'):
        if Fuquan == 'raw':
            file_path = os.path.join(self.raw_path,  '{}.csv'.format(stock_code))
        else:
            file_path = os.path.join(self.result_path,  '{}.csv'.format(stock_code))

        history.to_csv(file_path)

    def write_summary_data(self, stock_code, history):
        file_path = os.path.join(self.raw_path, '{}_summary.json'.format(stock_code))
        with open(file_path, 'w') as f:
            latest_day = history.index[-1].strftime('%Y-%m-%d')
            year = latest_day[:4]
            month = latest_day[5: 7]
            day = latest_day[8:]
            summary = dict(
                year=year,
                month=month,
                day=day,
                date=latest_day
            )
            json.dump(summary, f)

    def loadtodict(self, stock_code):
        path = os.path.join(self.result_path, '{}.csv'.format(stock_code))
        with open(path) as f:
            f_csv = csv.DictReader(f)
            data = [day for day in f_csv]
        return data

    def update_stock(self, stock_code, updated_data):
        self.update_stock_data(stock_code, updated_data)
        self.write_summary_data(stock_code, updated_data)


    def update_stock_data(self, stock_code, updated_data):
        csv_file_path = os.path.join(self.result_path, '{}.csv'.format(stock_code))
        old_history = pd.read_csv(csv_file_path, index_col = 0, parse_dates=True)
        update_start_day = updated_data.index[0]

        old_clean_history = old_history[old_history.index <  update_start_day]
        new_history = pd.concat([old_clean_history, updated_data])
        self.write_stock_data(stock_code, new_history)

    def loadtoHistory(self):
        file_list = [f for f in os.listdir(self.result_path) if f.endswith('.csv')]
        market = dict()
        for stock_csv in file_list:
            csv_ext_index_start = -4
            stock_code = stock_csv[:csv_ext_index_start]

            csv_path = os.path.join(self.result_path, stock_csv)

            ind = Indicator(stock_code, pd.read_csv(csv_path, index_col='date'))
            market[stock_code] = ind

        return market



class xlsStore:
    def __init__(self, path):
        super(xlsStore, self).__init__()
        self.store_type = 'xls'
        self.root_path = path

    def loadtoHistory(self):
        pass

    def get_exists_codes(self):
        pass

    def write(self, stock_code, data):
        pass

    def loadtodict(self, stock_code):
        pass

    def write_csv_file(self, stock_code, history, Fuquan='raw'):
        pass

    def update_stock(self, stock_code, updated_data):
        pass

    def get_last_update_date(self, stock_code):
        pass

    def write_stock_data(self, stock_code, history, Fuquan='raw'):
        pass

