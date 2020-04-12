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
        self.__memory = self.obj_to_dic(psutil.virtual_memory())
        return self.__memory

    def __get_disk(self):
        self.__disk = dict()
        disk_partitions = [sdiskpart.mountpoint for sdiskpart in psutil.disk_partitions()]
        for partition in disk_partitions:
            self.__disk[partition] = self.obj_to_dic(psutil.disk_usage(partition))
        return self.__disk

    def get_info(self):
        info = {
            'cpu': self.__get_cpu(),
            'memory': self.__get_memory(),
            'disk': self.__get_disk()
        }
        return info

    def obj_to_dic(self, obj):
        ket_tuple = ('total', 'used', 'percent', 'free', 'available')
        tmp = dict()
        for key in dir(obj):
            if key.startswith(ket_tuple):
                tmp[key] = getattr(obj, key)
        return tmp

    def client_send_info(self):
        while True:
            data = self.get_info()
            data = json.dumps(data).encode('utf-8')
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.remote, self.port))   # 建立连接
                print(s.recv(1024).decode('utf-8'))  # 接收欢迎消息
                s.send(data)                          # 发送info
                print(s.recv(1024).decode('utf-8'))  # 接收回复
                s.close()
                time.sleep(120)
            except socket.error as msg:
                print(msg)
                print(sys.exit(1))

hu = HardwareUsage()
hu.client_send_info()
