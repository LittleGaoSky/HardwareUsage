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
        data = json.loads(data)
        print(data)
        sock.send(b'Success!')
        print('Connection from %s:%s closed' % addr)
        sock.close()
    except sock.error as msg:
        print(msg)
        print(sys.exit(1))

def server_receive_info(host, port):
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(100)
    print('Waiting for connection...')
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=tcp_link, args=(sock, addr))
        t.start()

if __name__ == '__main__':
    server_host = '127.0.0.1'
    server_port = 9427
    server_receive_info(server_host,server_port)