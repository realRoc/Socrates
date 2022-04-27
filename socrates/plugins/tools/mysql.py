#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:DOULIHANG
@file: db_operation.py
@time: 2020/07/01 
"""
import json
import pymysql
 
class DbOperation():
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        # 连接数据库
        self.conn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    database=self.database,
                                    port=self.port)
 
    def select(self, sql):
        try:
            # 使用cursor操作游标
            cursor = self.conn.cursor()
            # 执行sql
            cursor.execute(sql)
            # 获取所有记录，返回格式为元组
            results = cursor.fetchall()
            return results
        except:
            print("SQL: {} cannot select".format(sql))
 
    def update(self, sql):
        try:
            # 使用cursor操作游标
            cursor = self.conn.cursor()
            # 执行sql
            cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()
 
    def delete(self, sql):
        try:
            # 使用cursor操作游标
            cursor = self.conn.cursor()
            # 执行sql
            cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()
 
    def insert(self, sql):
        try:
            # 使用cursor操作游标
            cursor = self.conn.cursor()
            # 执行sql
            cursor.execute(sql)
            # 提交到数据库执行
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()
 
    def run_stored_procedure(self, args):
        # 调用存储过程
        try:
            cur = self.conn.cursor()
            # 调用存储过程，QSP_Clean_Data为存储过程名称，args为存储过程要传入的参数，格式为元组
            cur.callproc('QSP_Clean_Data', args)
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()
 
    def close(self):
        # 关闭数据库连接
        self.conn.close()
 