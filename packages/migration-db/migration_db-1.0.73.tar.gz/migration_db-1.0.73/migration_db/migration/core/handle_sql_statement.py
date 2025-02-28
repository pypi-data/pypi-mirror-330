# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 5/28/2024 3:01 PM
@Description: Description
@File: handle_sql_statement.py
"""
import sqlparse
from sqlparse.sql import Identifier

from common_utils.log import Logger
from migration.core.construct_sql.parse_sql import parse_sql


def extract_tables_and_columns(sql):
    parsed = sqlparse.parse(sql)
    table_columns = {}
    for stmt in parsed:
        tokens = stmt.tokens
        sql_stmt = stmt.value.strip()
        print(sql_stmt)
        for token in tokens:
            table_name = None
            if isinstance(token, Identifier):
                identifier_tokens = token.tokens
                for identifier_token in identifier_tokens:
                    if table_name is None:
                        table_name = identifier_token.value
                    else:
                        raise Exception("error.")
    return table_columns


def handle_sql_statement(sql_statement, all_table, all_table_field):
    result = []
    for sql_dto in sql_statement:
        statements = sql_dto.get('details')
        if not statements:
            continue
        try:
            parsed = parse_sql(statements)
            filter_sql = []
            for stmt, tables_fields in parsed.items():
                for table, fields in tables_fields.items():
                    if table not in all_table:
                        break
                    fields_ = all_table_field.get(table) or set()
                    if not (fields_ and set(fields).issubset(fields_)):
                        break
                else:
                    filter_sql.append(stmt)
            if filter_sql:
                result.extend(filter_sql)
        except Exception as e:
            Logger().error(f"Error parsing SQL: {e}")
            result.append(statements)
    return result


def get_table_from_sql_statement(sql_statement):
    result = set()
    for sql_dto in sql_statement:
        statements = sql_dto.get('details')
        if not statements:
            continue
        try:
            parsed = parse_sql(statements)
            for tables_fields in parsed.values():
                for table in tables_fields.keys():
                    result.add(table)
        except Exception as e:
            Logger().error(f"Error parsing SQL: {e}")
    return result
