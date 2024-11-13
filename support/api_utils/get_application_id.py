#!/usr/bin/python3
# coding=utf-8
import time
import pymysql.cursors
import ast
from datetime import datetime 

def get_group_id(app, api_host):
    mysql_host = api_host[7:]
    if "https" in api_host:
        mysql_host = api_host[8:]
    if "192.168.44.3" in api_host:
        db = pymysql.connect(host=mysql_host,
                             user='test',
                             password='test@cm',
                             database='tsg-bifang')
    else:
        db = pymysql.connect(host=mysql_host,
                             user='test',
                             password='test',
                             database='tsg-bifang')
    group_id_list = []
    # 该方法用于将字符串类型的['ssl', 'http']转换为list类型的['ssl', 'http']（在无法使用list函数直接转换的情况下）
    app = ast.literal_eval(app)
    for app_name in app:
        sql = "select object_uuid from app_id_dict where app_name= 'appname'"
        sql = sql.replace("appname", app_name)
        # 连接数据库
        mycursor = db.cursor()
        # 根据sql查询
        mycursor.execute(sql)
        # 获取查询结果
        myresult = mycursor.fetchall()
        # 处理查询结果，获取id
        group_id = myresult[0][0]
        group_id_list.append(group_id)
    return group_id_list

    if __name__ == '__main__':
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "test")