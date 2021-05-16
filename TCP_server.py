#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   TCP_server.py    
@Contact :   519605144@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/4/28 16:07   huanghao      1.0         None
'''
import socket
import multiprocessing
from wsgiTest import application


# 1.构建socket对象
class staticWebServer():
    def __init__(self, port):
        self.static_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.static_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.static_server.bind(('', port))
        self.static_server.listen(5)
        print('服务器启动-----------------')

    def start(self):
        # 2.接受请求
        while True:
            clients, ip_ports = self.static_server.accept()
            print(f'客户端{ip_ports[0]}使用{ip_ports[1]}端口接入...')
            p = multiprocessing.Process(target=self.task, args=(clients,))
            p.start()
            clients.close()
        self.static_server.close()

    def task(self, clients):
        request_info = clients.recv(1024).decode()
        if len(request_info) == 0:
            clients.close()

        else:
            request_path = request_info.split(' ')[1]
            if request_path == '/':
                request_path = '/index.html'
            print("请求地址是:", request_path)

            # wsgi动静分离
            # 后缀为html为动态数据
            if request_path.endswith('.html'):
                # 处理动态数据
                env = {"PATH": request_path}
                response_body = application(env, self.start_response)
                response_line = f'HTTP/1.1 {self.__status}\r\n'
                response_head = ''
                for k, v in self.__headers:
                    response_head += f'{k}:{v}\r\n'
                response_data = (response_line + response_head + '\r\n' + response_body).encode()
                clients.send(response_data)
                clients.close()

            else:
                # 3.读取资源内容
                try:
                    with open(f"..\\{request_path}", 'rb') as f:
                        file_content = f.read()
                # 4.拼接响应报文
                except Exception as e:
                    response_line = 'HTTP/1.1 404 NOT FOUND\r\n'
                    response_head = 'Server:PSW1.0\r\n'
                    with open('error.html', 'rb') as f:
                        error_html = f.read()
                    response_data = (response_line + response_head + '\r\n').encode() + error_html
                    clients.send(response_data)
                else:
                    response_line = 'HTTP/1.1 200 OK\r\n'
                    response_head = 'Server:PSW1.0\r\n'
                    response_data = (response_line + response_head + '\r\n').encode() + file_content
                    clients.send(response_data)

                # 5.发送响应报文
                finally:
                    clients.close()

    def start_response(self, status, headers):
        self.__status = status
        self.__headers = headers


if __name__ == '__main__':
    staticWebServer(port=4444).start()
