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
        # �������ݿ�
        self.conn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    database=self.database,
                                    port=self.port)
 
    def select(self, sql):
        try:
            # ʹ��cursor�����α�
            cursor = self.conn.cursor()
            # ִ��sql
            cursor.execute(sql)
            # ��ȡ���м�¼�����ظ�ʽΪԪ��
            results = cursor.fetchall()
            return results
        except:
            print("SQL: {} cannot select".format(sql))
 
    def update(self, sql):
        try:
            # ʹ��cursor�����α�
            cursor = self.conn.cursor()
            # ִ��sql
            cursor.execute(sql)
            # �ύ�����ݿ�ִ��
            self.conn.commit()
        except:
            # ��������ʱ�ع�
            self.conn.rollback()
 
    def delete(self, sql):
        try:
            # ʹ��cursor�����α�
            cursor = self.conn.cursor()
            # ִ��sql
            cursor.execute(sql)
            # �ύ�����ݿ�ִ��
            self.conn.commit()
        except:
            # ��������ʱ�ع�
            self.conn.rollback()
 
    def insert(self, sql):
        try:
            # ʹ��cursor�����α�
            cursor = self.conn.cursor()
            # ִ��sql
            cursor.execute(sql)
            # �ύ�����ݿ�ִ��
            self.conn.commit()
        except:
            # ��������ʱ�ع�
            self.conn.rollback()
 
    def run_stored_procedure(self, args):
        # ���ô洢����
        try:
            cur = self.conn.cursor()
            # ���ô洢���̣�QSP_Clean_DataΪ�洢�������ƣ�argsΪ�洢����Ҫ����Ĳ�������ʽΪԪ��
            cur.callproc('QSP_Clean_Data', args)
            self.conn.commit()
        except:
            # ��������ʱ�ع�
            self.conn.rollback()
 
    def close(self):
        # �ر����ݿ�����
        self.conn.close()
 