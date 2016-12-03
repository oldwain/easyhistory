# coding:utf-8
# from .day import Day
from .day2 import Day
from .yahooday import YahooDay
dayhist = None


def init(qtype, export, path, start_year='1990'):
    if qtype.lower() in ['d']:
        return Day(export, path, start_year).init()


def update(dtype='D', export='csv', path='history', start_year='1990'):
    return Day(export, path, start_year).update()


def prepare(export='csv', path='history', start_year='1990'):
    global dayhist
    dayhist = Day(export, path, start_year)


def update_single_code(stock_code):
    if dayhist is None:
        print(u'调用update_single_code需先执行prepare')
    return dayhist.update_single_code(stock_code)

def init_yahoo(qtype, export, path, start_year='1990'):
    if qtype.lower() in ['d']:
        return YahooDay(export, path, start_year).init()

def update_single_code_yahoo(stock_code,path):
    dayhist = YahooDay('csv', path, '1990')
    return dayhist.update_single_code(stock_code)

