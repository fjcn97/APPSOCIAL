#!/usr/bin/python

import pymysql

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='')

sql = """CREATE DATABASE APPSOCIAL;"""

conn.cursor().execute(sql)
