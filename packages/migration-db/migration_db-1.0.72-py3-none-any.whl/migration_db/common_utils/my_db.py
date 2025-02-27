"""
Created on Nov 27, 2019

@author: xiaodong.li
"""

import pymysql

from .log import Logger


class MyDB(object):
    """
    define my database
    """

    def __init__(self, config):
        """
        initialization parameters
        :param config: object
        """
        self.connect_params = dict(host=config.host, port=int(config.port), user=config.user_name,
                                   password=config.password, db=config.database, charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
        self.env = f"{config.host} / {config.database}"
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        """
        : 获取连接对象和执行对象
        :return:
        """
        try:
            self.conn = pymysql.Connect(**self.connect_params)
            self.cur = self.conn.cursor()
            Logger().debug(f"Connect Database ({self.env}) successfully.")
        except Exception as e:
            Logger().error(f"Connect Database ({self.env}): Mysql Error{e}.")
            raise BaseException(e)

    def fetchone(self, sql, params=None):
        """
        : 根据sql和参数获取一行数据
        :param sql: sql语句
        :param params: sql语句对象的参数元祖，默认值为None
        :return: 查询的一行数据
        """
        data_one = None
        try:
            count = self.cur.execute(sql, params)
            Logger().debug(f"SQL>>>{self.cur._executed}")
            if count != 0:
                data_one = self.cur.fetchone()
            else:
                Logger().debug("The SQL query data is empty.")
        except Exception as ex:
            self.close()
            Logger().error(ex)
        return data_one

    def fetchall(self, sql, params=None):
        """
        : 根据sql和参数获取一行数据
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 查询的一行数据
        """
        data_all = None
        try:
            count = self.cur.execute(sql, params)
            Logger().debug(f"SQL>>>{self.cur._executed}")
            if count != 0:
                data_all = self.cur.fetchall()
            else:
                Logger().debug("The SQL query data is empty.")
        except Exception as ex:
            Logger().error(sql)
            Logger().error(ex)
            self.close()
        return data_all

    def execute(self, sql, params=None):
        """
        : 执行sql
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return:
        """
        Logger().debug(f"SQL>>>{sql}")
        try:
            self.cur.execute(sql, params)
            return True
        except Exception as ex:
            Logger().error(ex)
            return False

    def execute_many(self, stmts):
        """
        : 执行多条sql
        """
        Logger().debug(f"SQL_STATEMENTS>>>{stmts}")
        try:
            sqls = stmts.split(";")
            self.cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
            for sql in sqls:
                sql = sql.strip().replace("\n", "").replace(";", "").replace("  ", " ")
                if not sql:
                    continue
                sql = f"{sql};"
                self.cur.execute(sql)
                Logger().info(f"SQL>>>{sql}")
            self.cur.execute("SET FOREIGN_KEY_CHECKS = 1;")
        except Exception as ex:
            Logger().error(ex)
        finally:
            self.close()

    def _items(self, sql, params=None):
        """
        : 执行增删改
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 受影响的行数
        """
        try:
            Logger().debug(f"SQL>>>{self.cur._executed}")
            self.cur.execute(sql, params)
            self.conn.commit()
        except Exception as ex:
            Logger().error(ex)

    def update(self, sql, params=None):
        """
        : 执行修改
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 受影响的行数
        """
        return self._items(sql, params)

    def insert(self, table_name, table_data):
        """
        : 执行新增
        :param table_name: 表名
        :param table_data: 数据字典
        :return: 受影响的行数
        """
        keys = ','.join(table_data.keys())
        values = ','.join(['%s'] * len(table_data))
        sql = f"INSERT INTO {table_name}({keys}) VALUES ({values});"
        try:
            self._items(sql, params=tuple(table_data.values()))
            Logger().debug("插入数据成功.")
        except:
            self.db.rollback()
            self.close()
            Logger().error("插入数据失败.")

    def delete(self, table_name, table_data, params=None):
        """
        : 执行删除
        :param table_name: 表名
        :param table_data: 数据字典
        :return: 受影响的行数
        """
        condition = ""
        if params is None:
            for keys in table_data.keys():
                if keys == list(table_data.keys())[-1]:
                    condition = condition + keys + ' = %s'
                    break
                condition = condition + keys + " = %s and "
        elif params == 'in':
            for keys, values in table_data.items():
                if values is None:
                    table_data[keys] = (None,)
                condition = f"{keys} in %s"
        sql = f"DELETE FROM {table_name} WHERE {condition};"
        try:
            self._items(sql, params=tuple(table_data.values()))
        except:
            self.close()

    def close(self):
        """
        : Close the execution tool and the connected object.
        """
        try:
            if self.cur is not None:
                self.cur.close()
            if self.conn is not None:
                self.conn.close()
                Logger().debug(f"Database ({self.env}) closed.")
        except Exception as e:
            return Logger().error(f"Mysql Error {e}")

    def insert_many(self, table_name, data: list):
        try:
            length = len(data)
            print(f"insert_many start: {length}")
            slice_size = 10000
            if length > 0:
                first_row = data[0]
                fields = ','.join(list(data[0].keys()))
                values = ','.join(['%s'] * len(first_row))
                sql = f"INSERT INTO {table_name}({fields}) VALUES ({values})"
                slice_count = length // slice_size
                remainder = len(data) % slice_size
                if remainder > 0:
                    slice_count += 1
                start = 0
                for count in range(1, slice_count + 1):
                    if count < slice_count:
                        end = slice_size * count
                    else:
                        end = length
                    items = data[start: end]
                    partial_data = [tuple(item.values()) for item in items]
                    self.cur.executemany(sql, partial_data)
                    start = end
                    print(end)
                self.conn.commit()
            print(f"insert_many end: {length}")
        except Exception as e:
            raise Exception(str(e))
