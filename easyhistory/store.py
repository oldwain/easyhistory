import os
import json
import csv
import pandas as pd
from datetime import datetime
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
        if os.path.exists(self.raw_path):
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
        self.write_stock_data(stock_code, data, 'raw')
        self.write_summary_data(stock_code, data)
        new_history = self.gen_history_result(stock_code)
        self.write_stock_data(stock_code, new_history, 'data')

    # 保存股票数据， fuquan='raw' 保存原始数据， fuquan='data' 保存还原后的数据
    def write_stock_data(self, stock_code, history, Fuquan='raw'):
        if Fuquan == 'raw':
            file_path = os.path.join(self.raw_path,  '{}.csv'.format(stock_code))
        else:
            file_path = os.path.join(self.result_path,  '{}.csv'.format(stock_code))

        with open(file_path, 'w') as f:
            f.write('date,open,high,close,low,volume,amount,factor\n')
            for day_line in history:
                # print (day_line)
                if len(day_line) == 7:
                    day_line.append(1.0)
                write_line = '{},{},{},{},{},{},{},{}\n'.format(*day_line)
                f.write(write_line)

    def write_summary_data(self, stock_code, history):
        file_path = os.path.join(self.raw_path, '{}_summary.json'.format(stock_code))
        with open(file_path, 'w') as f:
            latest_day = history[-1][0]
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
        path = os.path.join(self.raw_path, '{}.csv'.format(stock_code))
        with open(path) as f:
            f_csv = csv.DictReader(f)
            data = [day for day in f_csv]
        return data

    def update_stock(self, stock_code, updated_data):
        self.update_stock_data(stock_code, updated_data)
        self.write_summary_data(stock_code, updated_data)

        new_history = self.gen_history_result(stock_code)
        self.write_stock_data(stock_code, new_history, 'data')

    def update_stock_data(self, stock_code, updated_data):
        csv_file_path = os.path.join(self.raw_path, '{}.csv'.format(stock_code))
        with open(csv_file_path) as f:
            f_csv = csv.reader(f)
            old_history = [l for l in f_csv][1:]
        # latest_day = updated_data[-1][0]
        update_start_day = updated_data[0][0]
        # old_clean_history = [day for day in old_history if day < latest_day]
        old_clean_history = [day for day in old_history if day[0] < update_start_day]
        new_history = old_clean_history + updated_data
        new_history.sort(key=lambda day: day[0])
        self.write_stock_data(stock_code, new_history)

    def loadtoHistory(self):
        file_list = [f for f in os.listdir(self.raw_path) if f.endswith('.csv')]
        market = dict()
        for stock_csv in file_list:
            csv_ext_index_start = -4
            stock_code = stock_csv[:csv_ext_index_start]

            csv_path = os.path.join(self.result_path, stock_csv)

            ind = Indicator(stock_code, pd.read_csv(csv_path, index_col='date'))
            market[stock_code] = ind

        return market

    # 根据复权数据生成一只股票的原始数据
    def gen_history_result(self, stock_code):
        factor_cols = {'close', 'open', 'high', 'low'}
        history_order = ['date', 'open', 'high', 'close', 'low', 'volume', 'amount', 'factor']

        # TODO 思考读取是使用 字典 还是 列表? 主要是方便后面指标的添加计算
        day_history = self.loadtodict(stock_code)

        if helpers.code_type(stock_code) in ['index', 'fund']:
            factor = 1
        else:
            factor = float(max(day_history, key=lambda x: float(x['factor']))['factor'])
        new_history = []
        for day_data in day_history:
            for col in day_data:
                if col in factor_cols:
                    day_data[col] = round(float(day_data[col]) / factor, 2)
            ordered_item = []
            for col in history_order:
                ordered_item.append(day_data[col])
            new_history.append(ordered_item)

        return new_history


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

