#!/usr/bin/python  
# -*- coding: utf-8 -*-  
import ftplib   
import os  
import socket  
import datetime
import sys
import rarfile
import struct
import time
import re
import string
import sys
import requests

HOST = '222.73.103.181'   # dzh download
DIRN = '/platform/download/PWR/'  
FILE = 'full.PWR'  
API = 'http://222.73.103.181/platform/download/PWR/{}.PWR'
filepath = os.path.normcase('d:/')


def getfile():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    url = API.format('full')

    loop_nums = 10
    for i in range(loop_nums):
        try:  
            rep = requests.get(url, timeout=3, headers=headers)
            break
        except requests.ConnectionError:
            time.sleep(60)
        except Exception as e:
            print(str(e))
        if rep is None:
            print('error')
        
    contents = rep.content
    with open(os.path.join(filepath,'full.PWR'), 'wb') as f:
        f.write(contents)


def pwrtocsv():
    '''
    结构：
    header(8b)
        ffff(4b) 
        code(8b)
        00000000(8b)
            ymd  (all 4b)
            sz
            pgs
            pgj
            fh

    '''
    infilename =   os.path.join(filepath,'full.PWR')            
    outfilename =  os.path.join(filepath,'full.csv')
    f = open(infilename ,"rb")
    fw = open(outfilename,'w')
    s = f.read(8)

    (fileflag,unknow1) = struct.unpack('II',s)
    if fileflag != 4282632242:
        print ('error file flag.')
        return
    lines = ''
    stock_code = ''
    while True:
        try:
            s = f.read(20)
            if len(s)==0:
                break
        except Exception as e:
            print(e)
            break

        if s[0:4] == b'\xff\xff\xff\xff':
            stock_code = s[4:12].decode('utf-8')

        else:        

            try:
                (iymd, szs, pgs,pgj,fh) = struct.unpack('I4f',s)
            except Exception as e:
                f.close()
                fw.close()
                print(e)
                break
            ymd = time.localtime(iymd)
            symd = time.strftime("%Y-%m-%d", ymd)
            line = '{},{},{},{},{},{}\n'.format(stock_code, symd,szs,pgs,pgj,fh)
            #print (line)
            lines += line
            fw.write(line)
            fw.flush()
    f.close()
    fw.close()
    print (lines[:200])
##  main ##
#getfile()

pwrtocsv()
