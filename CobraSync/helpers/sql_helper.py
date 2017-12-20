# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import cx_Oracle
import pymysql
import pymssql

def readOracleSQL(connection_string, sql_statement):
    with cx_Oracle.connect(connection_string) as conn:
        cur = conn.cursor()
        cur.execute(sql_statement)
        result_list = cur.fetchall()
    
    return result_list

def writeOracleSQL(connection_string, sql_statement):
    with cx_Oracle.connect(connection_string) as conn:
        cur = conn.cursor()
        cur.execute(sql_statement)
        
def readMSSQL(sql_statement, config):
    username = config['MSSQL']['username']
    password = config['MSSQL']['password']
    host = str(config['MSSQL']['server'])
    database = config['MSSQL']['database']

    conn = pymssql.connect(host=host, user=username, password=password, db=database)
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_statement)
            result_list = cursor.fetchall()
    finally:
        conn.close()
    
    return result_list        

def readMySQL(sql_statement, config):
    username = config['MYSQL']['username']
    password = config['MYSQL']['password']
    host = str(config['MYSQL']['host'])
    port = int(config['MYSQL']['port'])
    database = config['MYSQL']['database']

    conn = pymysql.connect(host=host, user=username, password=password, db=database, port=port)
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_statement)
            result_list = cursor.fetchall()
    finally:
        conn.close()
    
    return result_list

def writeMySQL(sql_statement, config):
    username = config['MYSQL']['username']
    password = config['MYSQL']['password']
    host = str(config['MYSQL']['host'])
    port = int(config['MYSQL']['port'])
    database = config['MYSQL']['database']

    conn = pymysql.connect(host=host, user=username, password=password, db=database, port=port)
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_statement)
    finally:
        conn.close()