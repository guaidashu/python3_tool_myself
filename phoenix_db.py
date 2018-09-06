# -*- coding:utf8 -*-

from phoenixdb import connect
from .function import debug
import pymysql
from .config import phoenix_db_config as dbconfig


# noinspection PyPep8Naming,PyMethodMayBeStatic,PyBroadException,PyStatementEffect
class DBConfig(object):
    config = dbconfig.dbconfig()
    host = config['host']
    table_prefix = config['table_prefix']
    try:
        is_debug = config['debug']
    except:
        is_debug = False
    db = None
    cursor = None

    def __init__(self):
        pass

    def getConnect(self):
        return connect(url=self.host, autocommit=True)

    def getCursor(self):
        try:
            self.db = self.getConnect()
        except Exception as e:
            if self.is_debug:
                debug("数据库连接失败：")
                debug(e)
        finally:
            return self.db.cursor()

    def closeDB(self):
        try:
            self.db.close()
        except Exception as e:
            if self.is_debug:
                debug("数据库关闭失败：")
                debug(e)

    def select(self, data, get_all=True, is_close_db=True):
        self.cursor = self.getCursor()
        sql = self.getSelectSql(data)
        try:
            data['columns'][0]
            if data['columns'][0] == "*":
                try:
                    columns_sql = {
                        "table": data['table']
                    }
                    columns_data = self.getColumns(columns_sql)
                except:
                    self.closeDB()
                    if self.is_debug:
                        return {"error": "字段信息获取失败"}
            else:
                columns_data = tuple()
                for v in data['columns']:
                    tmp_tuple = ((v,),)
                    columns_data = columns_data + tmp_tuple
        except:
            try:
                columns_sql = {
                    "table": data['table']
                }
                columns_data = self.getColumns(columns_sql)
            except:
                self.closeDB()
                if self.is_debug:
                    return {"error": "字段信息获取失败"}
        try:
            self.cursor.execute(sql)
            if get_all:
                results = self.cursor.fetchall()
            else:
                results = self.cursor.fetchone()
        except:
            self.closeDB()
            if self.is_debug:
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
            length = len(results)
            for k in range(length):
                results_final[columns_data[k][0]] = results[k]
        return results_final

    def getColumns(self, data, num=1, is_close_db=False):
        self.cursor = self.getCursor()
        sql = self.getSelectSql(data)
        try:
            self.cursor.execute(sql)
            if num == 1:
                results = self.cursor.description
            else:
                results = self.cursor.description
        except Exception as e:
            results = 0
            if self.is_debug:
                debug("It's error that get table columns")
                debug(e)
        if is_close_db:
            self.closeDB()
        return results

    def insert(self, sql, is_close_db=True):
        self.cursor = self.getCursor()
        table = sql['table']
        del sql['table']
        sql = self.getInsertSql(sql, table)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            results = 1
        except Exception as e:
            if self.is_debug:
                debug("Database insert error, error info is:")
                debug(e)
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
            if self.is_debug:
                debug("Database insert error")
                debug(e)
            results = 0
        if is_close_db:
            self.closeDB()
        return results

    def update(self, sql, is_close_db=True):
        self.cursor = self.getCursor()
        try:
            self.cursor.execute(sql)
            self.db.commit()
            results = 1
        except Exception as e:
            if self.is_debug:
                debug("Database update error")
                debug(e)
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
        except Exception as e:
            if self.is_debug:
                debug("Database delete error")
                debug(e)
            results = 0
        if is_close_db:
            self.closeDB()
        return results

    # noinspection PyUnresolvedReferences
    def getDeleteSql(self, data, is_close_db=False):
        sql = "delete "
        s = ""
        sql = sql + s + ' from "' + self.table_prefix + data['table'] + '"'
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
        sql = sql + s + ' from "' + self.table_prefix + data['table'] + '"'
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

    def getInsertSql(self, data, table, is_close_db=False):
        # 构造插入查询语句，此函数传入参数data必须为dict()类型
        s = "upsert into \"" + self.table_prefix + table + "\"("
        columns = ""
        value = ""
        # get table's columns name
        table_sql = {
            "table": table
        }
        table_columns = self.getColumns(table_sql)
        table_columns_dict = dict()
        str_dict = {"text": "text", "varchar": "varchar", "longtext": "longtext", "datetime": "datetime",
                    "char": "char"}
        # int_dict = {"int": "int", "bigint": "bigint", "decimal": "decimal", "double": "double", "float": "float"}
        try:
            for v in table_columns:
                table_columns_dict[v[0]] = v[1].lower()
        except:
            pass
        length = len(data)
        i = 1
        filter_db = pymysql.connect()
        for k, v in data.items():
            if i != length:
                columns = columns + '"' + k + "\","
                tmpstr = "%s," % filter_db.escape(v)
                value = value + tmpstr
            else:
                columns = columns + '"' + k + '"'
                tmpstr = "%s" % filter_db.escape(v)
                value = value + tmpstr
            if k in table_columns_dict:
                del table_columns_dict[k]
            i = i + 1
        filter_db.close()
        for k, v in table_columns_dict.items():
            columns = columns + ",\"" + str(k) + "\""
            if table_columns_dict[k] in str_dict:
                value = value + ",'" + str("") + "'"
            else:
                value = value + "," + "0"
        data = s + columns + ")values(" + value + ")"
        if is_close_db:
            self.closeDB()
        return data

    def createTable(self, sql, sequence=False):
        self.cursor = self.getCursor()
        try:
            self.cursor.execute(sql)
            if isinstance(sequence, str):
                self.cursor.execute("create sequence " + sequence)
            if self.is_debug:
                debug("数据库创建成功")
        except Exception as e:
            if self.is_debug:
                debug("创建数据库出错，报错信息：")
                debug(e)
        finally:
            self.closeDB()
        return 0

    def free(self, sql):
        self.cursor = self.getCursor()
        data = 0
        try:
            self.cursor.execute(sql)
            if sql.find("select ") != -1:
                data = self.cursor.fetchall()
            if self.is_debug:
                debug("原生语句执行成功")
        except Exception as e:
            if self.is_debug:
                debug("原生语句执行出错，报错信息：")
                debug(e)
        finally:
            self.closeDB()
        return data


"""
designed by yy(奕弈)
"""
