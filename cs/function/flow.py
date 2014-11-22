#!/usr/bin/env python
# coding=utf-8

#  ------------------------------------
#  Create date : 2014-10-21 18:09
#  Author : Wangzhaojiang
#  Email : wangzhaojiang2013@gmail.com
#  ------------------------------------
import re
import time
import MySQLdb


def getdata_flow():
    f = open('/proc/net/dev', 'r')
    content = f.readlines()
    f.close()

    del content[0]
    del content[0]

    data = []

    for each_line in content:
        each_line = each_line.split()
        result = [each_line[0], int(each_line[1]), int(each_line[2])]

        data.append(result)

    return data

def flow():
    data_old = getdata_flow()
    
    #time_old = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
    #time.sleep(60)
    time.sleep(2)
    #time_new = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
    
    data_new = getdata_flow()

    result = []

    count = 0

    while count < len(data_old):
        old = data_old[count]
        new = data_new[count]
        interface = old[0]
        #byte = (new[1] - old[1]) * 8 #转换成bit流
        byte = (new[1] - old[1])
        packets = new[2] - old[2]

        tmp = [interface, byte, packets]
        result.append(tmp)

        count += 1

    return result

def sql(result):
    time_now = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))

    conn = MySQLdb.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'notamaiba',
            db = 'monitor',
            )
    cur = conn.cursor()

    sqldata = []
    
    for each_line in result:

        cur.execute(
                'insert into state_flow(ip, time, interface, byte, packets) values(%s, %s, %s, %s, %s)',
                ('127.0.0.1', time_now, each_line[0], each_line[1], each_line[2])
                )
        sqldata.append([time_now, each_line[0], each_line[1], each_line[2]])

    cur.close()
    conn.commit()
    conn.close()

    #print sqldata

    return sqldata


def main():
    result = flow()
    sqldata = sql(result)
    return sqldata


if __name__ == '__main__':
    main()

