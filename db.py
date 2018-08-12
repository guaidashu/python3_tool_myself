# -*- coding:utf8 -*-

import pymysql
from config import dbconfig
from .function import debug


# noinspection PyPep8Naming,PyMethodMayBeStatic,PyBroadException,PyStatementEffect
class DBConfig(object):
    config = dbconfig.dbconfig()
    username = config['username']
    password = config['password']
    host = config['host']
    port = config['port']
    database = config['database']
    # username = "yy"
    # password = "wyysdsa!"
    # host = "127.0.0.1"
    # port = "3306"
    # database = "hedui"
    db = None
    cursor = None

    def __init__(self):
        pass

    def getConnect(self):
        return pymysql.connect(self.host, self.username, self.password, self.database, charset="utf8")

    def getCursor(self):
        self.db = self.getConnect()
        return self.db.cursor()

    def closeDB(self):
        self.db.close()

    def select(self, data, get_all=True):
        self.cursor = self.getCursor()
        sql = self.getSelectSql(data)
        try:
            data['columns'][0]
            if data['columns'][0] == "*":
                try:
                    columns_sql = {
                        "table": "information_schema.columns",
                        "columns": ["COLUMN_NAME", "DATA_TYPE"],
                        "condition": ['TABLE_NAME = "' + data['table'] + '"', "and", 'TABLE_SCHEMA = "' + self.database + '"']
                    }
                    columns_data = self.getColumns(columns_sql)
                except:
                    return {"error": "字段信息获取失败"}
            else:
                columns_data = tuple()
                for v in data['columns']:
                    tmp_tuple = ((v,),)
                    columns_data = columns_data + tmp_tuple
        except:
            try:
                columns_sql = {
                    "table": "information_schema.columns",
                    "columns": ["COLUMN_NAME", "DATA_TYPE"],
                    "condition": ['TABLE_NAME = "' + data['table'] + '"', "and", 'TABLE_SCHEMA = "' + self.database + '"']
                }
                columns_data = self.getColumns(columns_sql)
            except:
                return {"error": "字段信息获取失败"}
        try:
            self.cursor.execute(sql)
            if get_all:
                results = self.cursor.fetchall()
            else:
                results = self.cursor.fetchone()
        except:
            results = {"error": "数据获取失败"}
        self.closeDB()
        if get_all:
            results_final = list()
            for v in results:
                length = len(v)
                content = dict()
                for k in range(length):
                    content[columns_data[k][0]] = v[k]
                results_final.append(content)
        else:
            results_final = dict()
            length = len(results)
            for k in range(length):
                results_final[columns_data[k][0]] = results[k]
        return results_final

    def getColumns(self, data, num=1):
        self.cursor = self.getCursor()
        sql = self.getSelectSql(data)
        try:
            self.cursor.execute(sql)
            if num == 1:
                results = self.cursor.fetchall()
            else:
                results = self.cursor.fetchone()
        except:
            results = 0
            debug("It's error that get table columns")
        return results

    def insert(self, sql):
        self.cursor = self.getCursor()
        try:
            self.cursor.execute(sql)
            self.db.commit()
            results = 1
        except:
            debug("Database insert error")
            results = 0
        self.closeDB()
        return results

    def update(self, sql):
        self.cursor = self.getCursor()
        try:
            self.cursor.execute(sql)
            self.db.commit()
            results = 1
        except:
            debug("Database update error")
            results = 0
        self.closeDB()
        return results

    # noinspection PyUnresolvedReferences
    def getSelectSql(self, data):
        sql = "select "
        s = ""
        # spell condition
        try:
            for i in data['columns']:
                if i != data['columns'][-1]:
                    s = s + i + ","
                else:
                    s = s + i
        except:
            s = "*"
        sql = sql + s + " from " + data['table']
        # if there is a condition , we spell it
        try:
            data['condition']
            sql = sql + " where "
            s = ""
            for i in data['condition']:
                s = s + i + " "
            sql = sql + s
        except:
            pass
        # if there is a order need , we spell it
        try:
            data['order']
            sql = sql + " order by " + data['order'][0] + " " + data['order'][1]
        except:
            pass
        # if there is limit. we spell it
        try:
            data['limit']
            sql = sql + " limit " + str(data['limit'][0]) + "," + str(data['limit'][1])
        except:
            pass
        return sql

    def getInsertSql(self, data, table):
        # 构造插入查询语句，此函数传入参数data必须为dict()类型
        s = "insert into " + table + "("
        columns = ""
        value = ""
        # get table's columns name
        table_sql = {
            "table": "information_schema.columns",
            "columns": ["COLUMN_NAME", "DATA_TYPE"],
            "condition": ['TABLE_NAME = "' + table + '"', "and", 'TABLE_SCHEMA = "' + self.database + '"']
        }
        table_columns = self.getColumns(table_sql)
        table_sql['condition'].append("and EXTRA like '%auto_increment%'")
        table_auto_increment = self.getColumns(table_sql)
        table_columns_dict = dict()
        str_dict = {"text": "text", "varchar": "varchar", "longtext": "longtext", "datetime": "datetime",
                    "char": "char"}
        # int_dict = {"int": "int", "bigint": "bigint", "decimal": "decimal", "double": "double", "float": "float"}
        try:
            for v in table_columns:
                table_columns_dict[v[0]] = v[1]
        except:
            pass
        length = len(data)
        i = 1
        for k, v in data.items():
            if i != length:
                columns = columns + k + ","
                # if table_columns_dict[k] in str_dict:
                tmpstr = "%s," % self.db.escape(str(v))
                value = value + tmpstr
                # else:
                # tmpstr = "%s," % self.db.escape()
                # value = value + tmpstr
            else:
                columns = columns + k
                # if table_columns_dict[k] in str_dict:
                tmpstr = "%s" % self.db.escape(str(v))
                value = value + tmpstr
                # else:
                #     value = value + str(v)
            if k in table_columns_dict:
                del table_columns_dict[k]
            i = i + 1
        # 删除主键id
        for v in table_auto_increment:
            del table_columns_dict[v[0]]
        for k, v in table_columns_dict.items():
            columns = columns + "," + str(k)
            if table_columns_dict[k] in str_dict:
                value = value + ",'" + str("") + "'"
            else:
                value = value + "," + "0"
        data = s + columns + ")values(" + value + ")"
        return data


"""
designed by yy(奕弈)
"""
