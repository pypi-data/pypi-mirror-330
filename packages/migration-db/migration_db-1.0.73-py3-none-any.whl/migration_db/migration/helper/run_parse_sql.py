# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 2/28/2025 11:18 AM
@Description: Description
@File: run_parse_sql.py
"""
from migration.core.construct_sql.parse_sql import parse_sql

if __name__ == '__main__':
    # 示例SQL语句
    sql = """
    UPDATE eclinical_crf_version SET `status`=(CASE WHEN `status` >= 500 THEN 560 WHEN `status` >= 100 THEN 100 END) WHERE latest=TRUE;
    """
    result1 = parse_sql(sql)
    for stmt, tables in result1.items():
        print(f"SQL: {stmt}")
        for table, fields in tables.items():
            print(f"  Table: {table}")
            print(f"    Fields: {fields}")
        print("\n" + "-" * 50 + "\n")
