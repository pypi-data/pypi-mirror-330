# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 2/28/2025 1:22 PM
@Description: Description
@File: parse_sql.py
"""
import sqlparse
from sqlparse.sql import Identifier, Where, Parenthesis, TokenList, Comparison, Function, Token
from sqlparse.tokens import Keyword, DML, Name


def parse_sql(sql):
    statements = sqlparse.parse(sql)
    result = {}
    for stmt in statements:
        stmt_str = str(stmt).strip()
        if not stmt_str:
            continue
        parsed = stmt
        tables_fields = {}
        if parsed.get_type() == 'UPDATE':
            main_table = None
            for token in parsed.tokens:
                if token.ttype is DML and token.value.upper() == 'UPDATE':
                    next_token = _get_next_non_whitespace_token(parsed.tokens, token)
                    if isinstance(next_token, Identifier):
                        main_table = next_token.get_real_name()
                        tables_fields[main_table] = []
                    break
            for token in parsed.tokens:
                if isinstance(token, TokenList):
                    for t in token.tokens:
                        if isinstance(t, Identifier):
                            col = get_column_name(t)
                            if main_table and col not in tables_fields[main_table]:
                                tables_fields[main_table].append(col)
                        elif isinstance(t, Function):
                            for t1 in t.tokens:
                                if isinstance(t1, Parenthesis):
                                    sub_sql = t1.value.strip('()')
                                    sub_tables = _parse_subquery(sub_sql)
                                    for tbl, fields in sub_tables.items():
                                        tables_fields.setdefault(tbl, []).extend(fields)
                                        tables_fields[tbl] = list(set(tables_fields[tbl]))
            for token in parsed.tokens:
                if isinstance(token, Where):
                    _extract_fields(token, main_table, tables_fields)
                elif isinstance(token, Parenthesis):
                    sub_sql = token.value.strip('()')
                    sub_tables = _parse_subquery(sub_sql)
                    for tbl, fields in sub_tables.items():
                        tables_fields.setdefault(tbl, []).extend(fields)
                        tables_fields[tbl] = list(set(tables_fields[tbl]))
        result[stmt_str] = tables_fields
    return result


def _get_next_non_whitespace_token(tokens, current_token):
    idx = tokens.index(current_token)
    for token in tokens[idx + 1:]:
        if not token.is_whitespace:
            return token
    return None


def _extract_fields(token, current_table, tables_fields, is_value=False):
    if isinstance(token, Identifier):
        if is_value:
            return
        name = token.get_real_name()
        if current_table and name not in tables_fields.get(current_table, []):
            tables_fields.setdefault(current_table, []).append(name)
    elif isinstance(token, Comparison):
        token: Comparison
        _extract_fields(token.left, current_table, tables_fields, False)
        _extract_fields(token.right, current_table, tables_fields, True)
    elif isinstance(token, TokenList):
        for t_ in token.tokens:
            new_is_value = is_value
            if t_.ttype == Comparison or t_.value.upper() in ('IN', 'VALUES'):
                new_is_value = True
            _extract_fields(t_, current_table, tables_fields, new_is_value)


def get_column_name(token):
    if is_quoted(token):
        return token.value.strip('`"\'')
    elif isinstance(token, Identifier):
        return token.get_real_name().split('.')[-1]
    elif isinstance(token, Token) and token.ttype == Name:
        return token.value
    return None


def is_quoted(token):
    if not token.value:
        return False
    return (token.value[0] in ('`', '"', "'") and
            token.value[-1] in ('`', '"', "'"))


def _parse_subquery(sql):
    statements = sqlparse.parse(sql)
    if len(statements) != 1:
        raise Exception(f"包含{len(statements)}个sql")
    parsed = statements[0]
    tables_fields = {}
    if parsed.get_type() == 'SELECT':
        main_table = None
        for token in parsed.tokens:
            if token.ttype is Keyword and token.value.upper() == 'FROM':
                next_token = _get_next_non_whitespace_token(parsed.tokens, token)
                if isinstance(next_token, Identifier):
                    main_table = next_token.get_real_name()
                    tables_fields[main_table] = []
                break
        for token in parsed.tokens:
            if isinstance(token, TokenList):
                for t in token.tokens:
                    if isinstance(t, Identifier) or (isinstance(t, Token) and t.ttype == Name):
                        col = get_column_name(t)
                        if main_table and col and col != main_table and col not in tables_fields[main_table]:
                            tables_fields[main_table].append(col)
            if isinstance(token, Where):
                _extract_fields(token, main_table, tables_fields)
    else:
        for token in parsed.tokens:
            if isinstance(token, Parenthesis):
                sub_sql = token.value.strip('()')
                sub_tables = _parse_subquery(sub_sql)
                for tbl, fields in sub_tables.items():
                    tables_fields.setdefault(tbl, []).extend(fields)
                    tables_fields[tbl] = list(set(tables_fields[tbl]))

    return tables_fields
