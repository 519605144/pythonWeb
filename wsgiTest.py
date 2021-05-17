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
import logging

import pymysql
from json import dumps

route_table = {}


def router(url):
    def wrapper(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        route_table[url] = inner
        return inner

    return wrapper


def application(environ, start_response):
    request_url = environ['PATH']
    if request_url in route_table:
        start_status = '200 OK'
        data = route_table[request_url]()
    else:
        logging.warning("客户端访问动态页面不存在")
        start_status = '404 NOT FOUND'
        data = error()

    start_response(start_status, [('Server', 'PMiniWebServer'), ('Content-Type', 'text/html; charset=utf-8')])
    return data


@router('/index.html')
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
                     <input type="button" name="toAdd" value="添加" id="toAdd" systemidvalue="%s">           
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


@router('/center_data.html')
def center_data():
    db = pymysql.Connection(host="localhost",
                            user="root",
                            password="huanghao",
                            database="python",
                            charset='utf8')

    cursor = db.cursor()
    sql = '''select b.code, b.short, b.chg, b.turnover, b.price, b.highs, a.note_info from focus a left join info b on a.info_id = b.id'''
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()

    json_list = []
    for t in result:
        json_data_dict = {}
        json_data_dict['code'] = t[0]
        json_data_dict['short'] = t[1]
        json_data_dict['chg'] = t[2]
        json_data_dict['turnover'] = t[3]
        json_data_dict['price'] = t[4]
        json_data_dict['highs'] = t[5]
        json_data_dict['note_info'] = t[6]
        json_list.append(json_data_dict)
    json_str = dumps(json_list, ensure_ascii=False)

    return json_str


@router('/center.html')
def center():
    with open('center.html', 'r', encoding='utf-8')  as f:
        content = f.read()
    content = content.replace('{%content%}', '')
    return content


def error():
    return '<h1>404 NOT FOUND!!!!!!....<h1>'
