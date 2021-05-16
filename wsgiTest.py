#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   wsgiTest.py    
@Contact :   519605144@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/5/14 14:35   huanghao      1.0         None
'''
import pymysql


def index():
    with open('index.html', encoding='utf-8') as f:
        content = f.read()
    row_str = """
       <tr>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>%s</td>
              <td>
                     <input type="button" value="添加" id="toAdd name="toAdd" systemidvalue="%s">           
              </td>
       </tr>   
       """
    db = pymysql.Connection(host="localhost",
                         user="root",
                         password="huanghao",
                         database="python",
                         charset='utf8')

    cursor = db.cursor()

    sql = '''select * from info'''
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()

    all_data = " "
    for i in result:
        all_data += row_str % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[1])
    content = content.replace('{%content%}', all_data)
    return content


def center():
    return '<h1>Center Page Run....<h1>'


def error():
    return '<h1>404 NOT FOUND!!!!!!....<h1>'


def application(environ, start_response):
    request_url = environ['PATH']
    start_status = '200 OK'
    if request_url == '/index.html':
        data = index()
    elif request_url == '/center.html':
        data = center()
    else:
        start_status = '404 NOT FOUND'
        data = error()

    start_response(start_status, [('Server', 'PMiniWebServer'), ('Content-Type', 'text/html')])
    return data

index()