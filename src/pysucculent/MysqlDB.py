# coding: utf-8
# Desc: mysql crud
"""
params Demo:
condition:
{
    "field1": ['=', 'test1'],
    'field2': ["=", 'test1']
}
order_by:
{
    "id": "desc"
}

fields:
['id', 'field1']
"""
import pymysql
import time
from pymysql.converters import escape_string
import threading
mysql_safe_lock = threading.Lock()

def instance_cls(cls):
    instance = {}
    def _singleton_wrapper(*args, **kargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kargs)
        return instance[cls]
    return _singleton_wrapper

def safe_connect(func):
    def wrapper(self, *args, **kw):
        result = None
        mysql_safe_lock.acquire()
        try:
            result = func(self, *args, **kw)
        except Exception as e:
            print("call function name [%s] error, reason mysql disconnect...."  % func.__name__, e)
            self.re_connect_db()
        mysql_safe_lock.release()
        return result
    return wrapper


@instance_cls
class baseDB:
    def __init__(self, host, user, port, password, database, exp=30):
        self.host = host
        self.user = user
        self.port = port
        self.passwd = password
        self.db = database
        self.conn = False
        self.cursor = False
        self.exp = 30
        self.conn = pymysql.connect(host=host,
                                    port=port,
                                    user=user,
                                    passwd=password,
                                    db=database,
                                    connect_timeout=exp)
        self.cursor = self.conn.cursor()

    @staticmethod
    def standard_condition(condition):
        where = ""
        if condition:
            where = " where 1 "
            for item in condition:
                where = "%s and `%s` %s '%s'" % (where,
                                                 escape_string(item),
                                                 escape_string(condition[item][0]),
                                                 escape_string(condition[item][1]))
        return where

    @staticmethod
    def standard_fields(fields):
        fieldsStr = ""
        if not fields:
            fieldsStr = "*"
        else:
            for field in fields:
                fieldsStr = fieldsStr + "`%s`," % field
            fieldsStr = fieldsStr.strip(",")
        return fieldsStr

    @staticmethod
    def standard_orderby(order_by):
        orderByStr = ""
        if order_by:
            orderByStr = " order by "
            for item in order_by:
                orderByStr = orderByStr + " " + str(item) + " " + str(order_by[item]) + ","
            orderByStr = orderByStr.strip(",")
        return orderByStr

    def connect_db(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, connect_timeout=self.exp)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("connect mysql failed! error %s" % e)
            self.conn = False
            self.cursor = False

    def re_connect_db(self, num=1, stime=1):
        _number = 1
        _status = True
        while _status and _number <= num:
            try:
                self.conn.ping()
                _status = False
            except Exception as e:
                print("Missing connect! Error:%s, Connecting..." % e)
                if self.connect_db() is True:
                    _status = False
                    break
                _number += 1
                time.sleep(stime)

    def close(self):
        self.conn.close()

    @safe_connect
    def first(self, table_name, condition=None, fields=None):
        fieldsStr = self.standard_fields(fields)
        sql = "select %s from %s" % (fieldsStr, table_name)
        sql = sql + self.standard_condition(condition)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result:
            fields = [i[0] for i in self.cursor.description]
            return dict(zip(fields, result))
        else:
            return result

    @safe_connect
    def all(self, table_name):
        self.cursor.execute("select * from %s" % table_name)
        data = self.cursor.fetchall()
        return data

    @safe_connect
    def get(self, table_name, condition=None, fields=None, order_by=None,  start:int = 0, len:int=999):
        start = int(start)
        len = int(len)
        if start < 0:
            start = 0
        fieldsStr = self.standard_fields(fields)
        sql = "select %s from %s" % (fieldsStr, table_name)
        sql = sql + self.standard_condition(condition)
        sql = sql + self.standard_orderby(order_by)
        sql = sql + " limit %s, %s" % (start, len)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        fields = [i[0] for i in self.cursor.description]
        return [dict(zip(fields, row)) for row in result]

    @safe_connect
    def total(self, table_name, condition=None):
        sql = "select * from %s" % table_name
        sql = sql + self.standard_condition(condition)
        self.cursor.execute(sql)
        return self.cursor.rowcount

    @safe_connect
    def group_total(self,table_name, fields, condition=None):
        fieldStr = self.standard_fields(fields)
        sql = "select %s from %s" % (self.standard_fields(fields),table_name)
        sql = sql + self.standard_condition(condition)
        sql = "%s group by %s" % (sql, fieldStr)
        self.cursor.execute(sql)
        return self.cursor.rowcount

    @safe_connect
    def insert(self, table_name, data):
        keys = data.keys()
        values = data.values()
        values = ['%s' % row for row in values]
        key_str = "`%s`" % "`,`".join(keys)
        value_str = "'%s'" % "','".join(values)
        sql = "insert into `%s` (%s) value(%s)" % (table_name, key_str, value_str)
        return self.exec(sql)

    @safe_connect
    def update(self, table_name, data, condition):
        sql = "update %s set " % table_name
        for item in data:
            sql = "%s `%s`='%s'," % (sql, item, data[item])
        sql = sql.strip(",")
        if condition:
            sql = sql + self.standard_condition(condition)
        else:
            return False
        return self.exec(sql)

    @safe_connect
    def delete(self, table_name, condition):
        sql = "delete from %s " % table_name
        if condition:
            sql = sql + self.standard_condition(condition)
        else:
            return False
        return self.exec(sql)

    @safe_connect
    def insertGetId(self, table_name, data):
        keys = data.keys()
        values = data.values()
        values = ['%s' % row for row in values]
        key_str = "`%s`" % "`,`".join(keys)
        value_str = "'%s'" % "','".join(values)
        sql = "insert into `%s` (%s) value(%s)" % (table_name, key_str, value_str)
        try:
            ret = self.cursor.execute(sql)
            retID = self.conn.insert_id()
            self.conn.commit()
        except Exception as e:
            retID = None
            self.conn.rollback()
        return retID

    def exec(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
        return False