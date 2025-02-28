# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 3/28/2023 2:09 PM
@Description: Description
@File: handle_special_field.py
"""
import re

from migration.lib.constant import DOT_PLACEHOLDER

REPLACE_STR = "REPLACE_STR"
GET_STR = "GET_STR"
REPLACE_STR_BY_MAPPING = "REPLACE_STR_BY_MAPPING"
SPLIT_STR_AND_RETURN = "REPLACE(SUBSTRING(SUBSTRING_INDEX({field_name}, '{separator}', {pos}), LENGTH(SUBSTRING_INDEX({field_name}, '{separator}', {pos} - 1)) + 1), '{separator}', '') AS {field_name}"


def handle_special_table_field(string):
    table_field_name = None
    if REPLACE_STR_BY_MAPPING in string:
        tmp = [i for i in re.split(rf"{REPLACE_STR_BY_MAPPING}|,|\(|\)| ", string) if i]
        table_field_name = tmp[0]
    elif REPLACE_STR in string:
        tmp = [i for i in re.split(rf"{REPLACE_STR}|,|\(|\)| ", string) if i]
        table_field_name = tmp[0]
    elif GET_STR in string:
        find_objs = re.findall(rf"({GET_STR}\(.*\))", string)
        for find_obj in find_objs:
            tmp = [i for i in re.split(rf"{GET_STR}|,|\(|\)| ", find_obj) if i]
            field_name = tmp[0]
            string = string.replace(find_obj, field_name)
        table_field_name = string
    return table_field_name


def generate_sql_for_special_rule(string):
    sql = ""
    fields = string.split(DOT_PLACEHOLDER)[-1]
    if GET_STR in string:
        find_objs = re.findall(rf"({GET_STR}\(.*\))", fields)
        for find_obj in find_objs:
            tmp = re.split(rf"{GET_STR}|,|\(|\)| ", find_obj)
            while "" in tmp:
                tmp.remove("")
            field_name = tmp[0]
            separator = tmp[1]
            pos = tmp[2]
            fields = fields.replace(find_obj,
                                    SPLIT_STR_AND_RETURN.format(field_name=field_name, separator=separator, pos=pos))
        sql = fields
    return sql


def judge_special_table_field(string):
    return any(i in string for i in [REPLACE_STR_BY_MAPPING, REPLACE_STR, GET_STR])
