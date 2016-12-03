import easyhistory
import multiprocessing
if __name__ == '__main__':
    multiprocessing.freeze_support()
    # easyhistroy.update_single_code('000001', 'out')
    # easyhistory.init('D', 'csv', 'd:\\gitlocal\\easydata_test', '2014')

    #easyhistory.update('D', 'csv', 'd:\\gitlocal\\easydata_test', '2014')

    easyhistory.init_yahoo('d', 'csv', 'd:\\gitlocal\\easydata_test\\yahoo', '2016')
    easyhistory.update_single_code_yahoo('^HSCE', 'd:\\gitlocal\\easydata_test\\yahoo')