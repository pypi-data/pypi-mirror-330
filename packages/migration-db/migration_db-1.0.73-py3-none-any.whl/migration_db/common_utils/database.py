# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 7/31/2023 3:03 PM
@Description: Description
@File: compare_two_dict.py
"""

from .my_db import MyDB


class Database(MyDB):
    def __init__(self, config):
        super().__init__(config)
        self.name = config.database
        self.table_structures = dict()

    @staticmethod
    def _get_field_values(items):
        return items and [list(item.values())[0] for item in items] or None

    def get_all_tables(self):
        items = self.fetchall("SHOW FULL TABLES  WHERE Table_type = 'BASE TABLE';")
        return self._get_field_values(items)

    def get_all_databases(self):
        items = self.fetchall("SHOW DATABASES;")
        return self._get_field_values(items)

    def get_table_desc(self, table):
        return self.fetchall(f"DESC `{table}`;")
