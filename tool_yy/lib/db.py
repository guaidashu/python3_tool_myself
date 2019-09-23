# -*- coding:utf8 -*-

import pymysql
from tool_yy.config import dbconfig
from .function import debug


# noinspection PyPep8Naming,PyMethodMayBeStatic,PyBroadException,PyStatementEffect
class DBConfig(object):
    config = dbconfig.dbconfig()
    username = config['username']
    password = config['password']
    host = config['host']
    port = config['port']
    database = config['database']
    table_prefix = config['table_prefix']
    is_debug = True
    db = None
    cursor = None

    def __init__(self, **kwargs):
        self.is_connection = False
        # 初始化方法允许用户单独定义要访问的数据库
        self.username = kwargs.setdefault("username", "root")
        self.password = kwargs.setdefault("password", "root")
        self.host = kwargs.setdefault("host", "127.0.0.1")
        self.port = kwargs.setdefault("port", "3306")
        self.database = kwargs.setdefault("database", "mysql")
        self.table_prefix = kwargs.setdefault("table_prefix", "")

    def __del__(self):
        self.closeDB()

    def getConnect(self):
        return pymysql.connect(self.host, self.username, self.password, self.database, charset="utf8")

    def getCursor(self):
        try:
            if not self.is_connection:
                self.db = self.getConnect()
                self.is_connection = True
        except Exception as e:
            if self.is_debug:
                debug("数据库连接失败：")
                debug(e)
        return self.db.cursor()

    def closeDB(self):
        try:
            self.db.close()
        except:
            pass
            # debug("数据库关闭失败")

    def close(self):
        try:
            self.db.close()
        except:
            pass

    def select(self, data, get_all=True, is_close_db=True):
        self.cursor = self.getCursor()
        data['table'] = self.table_prefix + data['table']
        sql = self.getSelectSql(data)
        try:
            data['columns'][0]
            if data['columns'][0] == "*":
                try:
                    columns_sql = {
                        "table": "information_schema.columns",
                        "columns": ["COLUMN_NAME", "DATA_TYPE"],
                        "condition": ['TABLE_NAME = "' + data['table'] + '"', "and",
                                      'TABLE_SCHEMA = "' + self.database + '"']
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
                    "condition": ['TABLE_NAME = "' + data['table'] + '"', "and",
                                  'TABLE_SCHEMA = "' + self.database + '"']
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
        if is_close_db:
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
            try:
                length = len(results)
            except:
                length = 0
            for k in range(length):
                results_final[columns_data[k][0]] = results[k]
        return results_final

    def getColumns(self, data, num=1, is_close_db=False):
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
        if is_close_db:
            self.closeDB()
        return results

    def insert(self, sql, is_close_db=True):
        self.cursor = self.getCursor()
        try:
            self.cursor.execute(sql)
            self.db.commit()
            results = 1
        except Exception as e:
            self.db.rollback()
            debug(e)
            debug("Database insert error")
            results = 0
        if is_close_db:
            self.closeDB()
        return results

    def insertLastId(self, sql, is_close_db=True):
        self.cursor = self.getCursor()
        try:
            self.cursor.execute(sql)
            self.db.commit()
            results = self.cursor.lastrowid
        except Exception as e:
            self.db.rollback()
            debug(e)
            debug("Database insert error")
            results = 0
        if is_close_db:
            self.closeDB()
        return results

    def update(self, data, is_close_db=True):
        self.cursor = self.getCursor()
        sql = self.getUpdateSql(data)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            results = 1
        except:
            self.db.rollback()
            debug("Database update error")
            results = 0
        if is_close_db:
            self.closeDB()
        return results

    def delete(self, data, is_close_db=True):
        self.cursor = self.getCursor()
        sql = self.getDeleteSql(data)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            results = 1
        except:
            self.db.rollback()
            debug("Database delete error")
            results = 0
        if is_close_db:
            self.closeDB()
        return results

    def getDeleteSql(self, data):
        sql = 'delete'
        data['table'] = self.table_prefix + data['table']
        sql = sql + " from " + data['table']
        try:
            data['condition']
            sql = sql + " where "
            s = ""
            for i in data['condition']:
                s = s + i + " "
            sql = sql + s
        except Exception as e:
            debug("condition is err, err info: {error}".format(error=e))
        return sql

    # noinspection PyUnresolvedReferences
    def getSelectSql(self, data, is_close_db=False):
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
        if is_close_db:
            self.closeDB()
        return sql

    def filterStr(self, s):
        if not self.is_connection:
            self.cursor = self.getCursor()
        return self.db.escape(s)

    def getUpdateSql(self, data, is_close_db=False):
        """
        :param data:  data['set'] is a dict  data['condition'] is a list
        :param is_close_db:
        :return:
        """
        sql = "update "
        sql = sql + self.table_prefix + data['table'] + ' set '
        try:
            data['set']
            s = ""
            m = 0
            for k, i in data['set'].items():
                if m == 0:
                    s = s + k + "=" + self.db.escape(i)
                    m = m + 1
                else:
                    s = s + "," + k + "=" + self.db.escape(i)
            sql = sql + s
        except Exception as e:
            pass
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
        if is_close_db:
            self.closeDB()
        return sql

    def getInsertSql(self, data, table, is_close_db=False, table_columns=False, table_auto_increment=False):
        # 构造插入查询语句，此函数传入参数data必须为dict()类型
        s = "insert into " + self.table_prefix + table + "("
        columns = ""
        value = ""
        # get table's columns name
        table_sql = {
            "table": "information_schema.columns",
            "columns": ["COLUMN_NAME", "DATA_TYPE"],
            "condition": ['TABLE_NAME = "' + self.table_prefix + table + '"', "and",
                          'TABLE_SCHEMA = "' + self.database + '"']
        }
        if not table_columns:
            table_columns = self.getColumns(table_sql)
        table_sql['condition'].append("and EXTRA like '%auto_increment%'")
        if not table_auto_increment:
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
                tmp_str = "%s," % self.db.escape(str(v))
                value = value + tmp_str
                # else:
                # tmp_str = "%s," % self.db.escape()
                # value = value + tmp_str
            else:
                columns = columns + k
                # if table_columns_dict[k] in str_dict:
                tmp_str = "%s" % self.db.escape(str(v))
                value = value + tmp_str
                # else:
                #     value = value + str(v)
            if k in table_columns_dict:
                del table_columns_dict[k]
            i = i + 1
        # 删除主键id
        for v in table_auto_increment:
            try:
                data['id']
                if v[0] == "id":
                    continue
            except Exception as e:
                pass
            del table_columns_dict[v[0]]
        for k, v in table_columns_dict.items():
            columns = columns + "," + str(k)
            if table_columns_dict[k] in str_dict:
                value = value + ",'" + str("") + "'"
            else:
                value = value + "," + "0"
        data = s + columns + ")values(" + value + ")"
        if is_close_db:
            self.closeDB()
        return data

    def free(self, sql, is_close_db=True):
        self.cursor = self.getCursor()
        data = 1
        try:
            self.cursor.execute(sql)
            if sql.lower().find("select ") != -1:
                data = self.cursor.fetchall()
        except Exception as e:
            self.db.rollback()
            if self.is_debug:
                debug("原生语句执行出错，报错信息：")
                data = 0
                debug(e)
        finally:
            if is_close_db:
                self.closeDB()
        return data


"""
designed by yy(奕弈)
"""
