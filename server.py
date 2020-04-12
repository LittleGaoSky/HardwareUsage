#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 适用于Windows, Linux环境，Python3.x
import socket
import threading
import time
import json
import sys


def tcp_link(sock, addr):
    print('Accept new connection from %s %s...' % addr)
    sock.send(b'Welcome to the server!')
    try:
        data = sock.recv(1024).decode('utf-8')
        data = json.loads(data)  # 接收到client端发来的info（CPU、内存、硬盘等信息）
        print(data)
        sock.send(b'Success!')
        print('Connection from %s:%s closed' % addr)
        sock.close()
    except sock.error as msg:
        print(msg)
        print(sys.exit(1))


def server_receive_info(host='127.0.0.1', port=9427):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(100)  # 最大监听连接数目
    print('Waiting for connection...')
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=tcp_link, args=(sock, addr))  # 每个新连接，单独新建一个线程来处理
        t.start()


if __name__ == '__main__':
    # 默认值 host='127.0.0.1', port=9427
    host = '192.168.1.6'  # 配置server端监听地址
    port = 9427  # 配置server端监听端口
    server_receive_info(host, port)
