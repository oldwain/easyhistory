# coding: utf-8
import math


def get_stock_type(stock_code):
    """判断股票ID对应的证券市场
    :param stock_code:股票ID
    :return 'sh' or 'sz'"""
    return stock_code[:2] if str(stock_code).startswith(('s', 'o')) \
        else ('sh' if str(stock_code).startswith(('5', '6', '9'))
              else 'sz')


def get_full_code(stock_code):
    """
    :param stock_code:  股票 ID
    :return:  'sh000001' or 'sz000001'
    """

    return stock_code if str(stock_code).startswith(('s', 'o')) else get_stock_type(stock_code) + stock_code


def get_quarter(month):
    return math.ceil(int(month) / 3)


def code_type(stock_code):
    if stock_code.startswith(('sh00', 'sz39')):
        return 'index'
    elif stock_code.startswith(('sh5', 'sz15', 'sz16', 'sz18')):
        return 'fund'   # 基金，包含封基、etf、lof等
    elif stock_code.startswith(('sh01', 'sh02', 'sh10', 'sh12', 'sh13', 'sz10', 'sz11')):
        return 'bond'   # 债券
    elif stock_code.startswith(('sh11', 'sz12')):
        return 'cb'     # 可转债
    elif stock_code.startswith(('sh132', 'sz12')):
        return 'eb'     # 可交换债
    elif stock_code.startswith(('sh20', 'sz13')):
        return 'repo'   # 逆回购
    elif stock_code.startswith('o'):
        return 'fundnav'
    else:
        return 'stock'
