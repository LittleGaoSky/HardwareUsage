#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 适用于Windows, Linux环境，Python3.x
import psutil
import socket
import sys
import json
import time


class HardwareUsage(object):
    def __init__(self, remote='127.0.0.1', port=9427):
        self.remote = remote
        self.port = port

    def __get_cpu(self):
        self.__cpu = dict()
        self.__cpu['count'] = psutil.cpu_count(logical=True)
        self.__cpu['percent'] = psutil.cpu_percent(interval=1, percpu=True)
        return self.__cpu

    def __get_memory(self):
        self.__memory = self.__obj_to_dic(psutil.virtual_memory())
        return self.__memory

    def __get_disk(self):
        self.__disk = dict()
        disk_partitions = [sdiskpart.mountpoint for sdiskpart in psutil.disk_partitions()]
        for partition in disk_partitions:
            self.__disk[partition] = self.__obj_to_dic(psutil.disk_usage(partition))
        return self.__disk

    def __obj_to_dic(self, obj):
        key_tuple = ('total', 'used', 'percent', 'free', 'available')
        tmp = dict()
        for key in dir(obj):
            if key.startswith(key_tuple):
                tmp[key] = getattr(obj, key)
        return tmp

    def get_info(self):
        info = {
            'cpu': self.__get_cpu(),
            'memory': self.__get_memory(),
            'disk': self.__get_disk()
        }
        return info

    def client_send_info(self):
        while True:
            data = self.get_info()
            data = json.dumps(data).encode('utf-8')
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.remote, self.port))  # 建立连接
                print(s.recv(1024).decode('utf-8'))  # 接收欢迎消息
                s.send(data)  # 发送info（CPU、内存、硬盘等信息）
                print(s.recv(1024).decode('utf-8'))  # 接收回复
                s.close()
                time.sleep(120)  # 每120秒采集发送一次信息
            except socket.error as msg:
                print(msg)
                print(sys.exit(1))


if __name__ == '__main__':
    # 默认值：remote='127.0.0.1', port=9427
    hu = HardwareUsage('192.168.1.6')
    hu.client_send_info()
