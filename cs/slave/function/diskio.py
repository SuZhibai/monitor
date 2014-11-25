#!/usr/bin/env python
# coding=utf-8

#  ------------------------------------
#  Create date : 2014-10-20 22:08
#  Author : Wangzhaojiang
#  Email : wangzhaojiang2013@gmail.com
#  ------------------------------------
import re
import time
import MySQLdb
import os
import sys
from get_conf import *

##os.chdir(os.path.dirname('./' + sys.argv[0]))
#
#sys.path.append('../../')
#
#from get_conf import *

def getdata_diskio():
    f = open('/proc/vmstat', 'r')
    content = f.readlines()

    option = ['^pgpgin', '^pgpgout']

    data = {}

    for each_line in content:
        for search in option:
            result = re.findall(search, each_line)
            if len(result) != 0:
                result = each_line.split()

                data[result[0]] = int(result[1])
                
                break

    return data


def diskio():
    data_old = getdata_diskio()
    #old_time = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
    #time.sleep(240)
    time.sleep(2)
    #new_time = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
    data_new = getdata_diskio()

    pgpgin_pass = (data_new['pgpgin'] - data_old['pgpgin']) / 240
    pgpgout_pass = (data_new['pgpgout'] - data_old['pgpgout']) / 240

    result = [pgpgin_pass, pgpgout_pass]

    return result

def sql(result):
    time_now = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
    pgpgin_pass = result[0]
    pgpgout_pass = result[1]

   # conn = MySQLdb.connect(
   #         host = 'localhost',
   #         port = 3306,
   #         user = 'root',
   #         passwd = 'notamaiba',
   #         db = 'monitor',
   #         )
    
    #os.chdir(os.path.dirname('../../'))
    #print os.getcwd()
    param = get_conf_data()

    conn = MySQLdb.connect(
            host = param['database_host'],
            port = int(param['database_port']),
            user = param['database_user'],
            passwd = param['database_passwd'],
            db = param['database_db'],
            )

    cur = conn.cursor()
    
    cur.execute(
            'insert into state_diskio(ip, time, pgpgin, pgpgout) values(%s, %s, %s, %s)',
            ('127.0.0.1', time_now, pgpgin_pass, pgpgout_pass)
            )
    
    cur.close()
    conn.commit()
    conn.close()

    sqldata = [time_now, pgpgin_pass, pgpgout_pass]

    return sqldata


def main():
    result = diskio()
    sqldata = sql(result)
    return sqldata

if __name__ == '__main__':
    main()
