# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 2/4/2021 2:47 PM
@Description: Description
@File: mysql_task.py
"""
import subprocess

from common_utils.lib import quote_identifier


class MysqlCommand(str):
    MYSQL = "mysql"
    MYSQLDUMP = "mysqldump"


class MysqlTask:

    def __init__(self, host, port, password, user, db=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db or ""

    def __mysql_task(self, sql_path, task_type, ignore_table=None, tables=None, no_create_info=False):
        task_type_symbol = dict(mysql="<", mysqldump=">").get(task_type, None)
        if task_type_symbol is None:
            raise Exception("Task type symbol is illegal.")
        pre_option = "--set-gtid-purged=OFF" if task_type == MysqlCommand.MYSQLDUMP else str()
        if no_create_info:
            pre_option += " " + MysqlOption().prepare_no_create_info_arg()
        tables_option = str()
        if task_type == MysqlCommand.MYSQLDUMP:
            if ignore_table is not None:
                tables_option += " " + MysqlOption(self.db).prepare_ignore_tables(ignore_table)
            if tables is not None:
                tables_option += " " + MysqlOption().prepare_tables_args(tables)
        host = f"-h{self.host}"
        port = f"-P {self.port}"
        user = f"-u{self.user}"
        password = f"-p{self.password}"
        db = f'"{self.db}"'
        sql_path = f"\"{sql_path}\""
        cmd = " ".join(
            [task_type, host, port, user, password, pre_option, db, tables_option, task_type_symbol, sql_path])
        exitcode, data = subprocess.getstatusoutput(cmd)
        if exitcode != 0:
            raise Exception(data)

    def _mysql_task(self, sql_path):
        return self.__mysql_task(sql_path, MysqlCommand.MYSQL)

    def _mysqldump_task(self, sql_path, ignore_table, tables=None, no_create_info=False):
        return self.__mysql_task(sql_path, MysqlCommand.MYSQLDUMP, ignore_table, tables, no_create_info)

    def mysql_task(self, sql_path):
        return self._mysql_task(sql_path)

    def mysqldump_task(self, sql_path, ignore_table=None, tables=None, no_create_info=False):
        return self._mysqldump_task(sql_path, ignore_table, tables, no_create_info)


class MysqlOption:

    def __init__(self, db=None):
        self.db = quote_identifier(db) if db is not None else db

    def prepare_ignore_tables(self, ignore_tables):
        """
       构造忽略指定表的 mysqldump 参数。
       :param ignore_tables: 要忽略的表列表
       :return: 包含忽略表的参数字符串
       """
        args = ["--ignore-table"]
        for table in ignore_tables:
            args.append("{db}.{table}".format(db=self.db, table=quote_identifier(table)))
        return " ".join(args)

    @staticmethod
    def prepare_tables_args(tables):
        """
        构造指定表进行备份的参数。
        :param tables:
        :return:
        """
        return " ".join(tables)

    @staticmethod
    def prepare_no_create_info_arg():
        return "--no-create-info"
