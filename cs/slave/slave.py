#!/usr/bin/env python
# coding=utf-8

#  ------------------------------------
#  Create date : 2014-11-01 18:13
#  Author : Wangzhaojiang
#  Email : wangzhaojiang2013@gmail.com
#  ------------------------------------
import socket
import os
import threading
import sys

#切换工作目录
os.chdir(os.path.dirname('./' + sys.argv[0]))

from function import *

sys.path.append('../')

from get_conf import *


def client_socket():
    os.chdir(os.path.dirname('../'))
    data = get_conf_data()
    HOST = data['master_node']
    PORT = int(data['trans_port'])
    BUFSIZ = 4096
    ADDR = (HOST, PORT)
    
    clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    clisock.connect(ADDR)

    data = getdata()

    data = process_data(data)

    clisock.send(data)

def process_data(data):
    host = socket.gethostname()
    ip = socket.gethostbyname(host)

    cpu_data = data['cpu']
    diskio_data = data['diskio']
    flow_data = data['flow']
    memory_data = data['memory']
    netstat_data = data['netstat']

    def tostr(data):
        count = 0
        while count < len(data):
            data[count] = str(data[count])
            count += 1

    tostr(cpu_data)
    tostr(diskio_data)
    tostr(flow_data)
    tostr(memory_data)
    tostr(netstat_data)
    
    cpu_data = 'cpu' + '^^' + '^^'.join(cpu_data) + '^^' + '|' + '^^'
    diskio_data = 'diskio' + '^^' + '^^'.join(diskio_data) + '^^' + '|' + '^^'
    flow_data = 'flow' + '^^' + '^^'.join(flow_data) + '^^' + '|' + '^^'
    memory_data = 'memory' + '^^' + '^^'.join(memory_data) + '^^' + '|' + '^^'
    netstat_data = 'netstat' + '^^' + '^^'.join(netstat_data) + '^^' + '|' + '^^'
    
    print host
    

    result = host + '^^' + ip + '^^' + cpu_data + diskio_data + flow_data + memory_data + netstat_data

    print result
    print len(result)

    return result



def getdata():
    # execute the __file__.py to get the monitor data
    
    categoty = {'cpu': cpu.main,
            'diskio': diskio.main,
            'flow': flow.main,
            'memory': memory.main,
            'netstat': netstat.main,
            }

    data = {}
    threads = []
    
    #让各个线程去处理数据
    for key in categoty.iterkeys():
        t = thread_getdata(key, categoty, data)
        t.setDaemon(True)
        t.start()
        threads.append(t)

    #等待所有数据处理完毕
    for t in threads:
        t.join()


    return data

class thread_getdata(threading.Thread):
    def __init__(self, key, categoty, data):
        self.key = key
        self.categoty = categoty
        self.data = data
        print key, 'getting the data'

        threading.Thread.__init__(self)

    def run(self):
        # 多线程获得数据并且 加锁
        lock = threading.Lock()

        lock.acquire()

        try:
            self.data[self.key] = self.categoty[self.key]()

        finally:
            lock.release()



if __name__ == '__main__':
    
    client_socket()
    
