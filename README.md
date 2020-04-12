# HardwareUsage
A tool with c/s architecture to detect hardware utilization 

# Step 1 of 2

`pip install psutil  -i https://pypi.tuna.tsinghua.edu.cn/simple`

# Step 2 of 2

## Server
1. config
    ```
    # host: the server ip， port: the server port
    server_receive_info(host, port)
    ```
2. run

    `python3 server.py`

    ![hardware_usage_server](https://cdn.pandas.icu/blog/typecho/hardware_usage_server.JPG)

## Client
1. config
    ```
    # remote: the server ip， port: the server port
    hu = HardwareUsage(remote, port)
    hu.client_send_info()
    ```
2. run

    `python3 client.py`

    ![hardware_usage_client_1of2](https://cdn.pandas.icu/blog/typecho/hardware_usage_client_1of2.JPG)

    ![hardware_usage_client_2of2](https://cdn.pandas.icu/blog/typecho/hardware_usage_client_2of2.JPG)

# PS

> Linux: memory_usage = 1 - available/total

# Reference
[廖雪峰-常用第三方模块psutil][1]

[简书-psutil 模块获取主机信息][2]

[1]: https://www.liaoxuefeng.com/wiki/1016959663602400/1183565811281984
[2]: https://www.jianshu.com/p/835054a11343