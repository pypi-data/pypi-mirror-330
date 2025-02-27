# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 3/24/2023 9:06 PM
@Description: Description
@File: handle_procedures.py
"""
import json
import re

from .handle_special_field import REPLACE_STR, REPLACE_STR_BY_MAPPING
from ..lib.constant import NEWLINE_PLACEHOLDER_PATTERN, DOT_PLACEHOLDER

REPLACE_STR_TEMPLATE = 'CALL REPLACE_STR("{table_name}", "{field_name}", "{pre_value}", "{cur_value}", "{separator}", {pos});'
REPLACE_STR_BY_MAPPING_TEMPLATE = 'CALL REPLACE_STR_BY_MAPPING("{table_name}", "{field_name}", "{separator}", \'{mapping}\', "{primary_key}");'


def handle_procedures(fields, values, all_table, all_table_field):
    result = list()
    items = [item.strip() for item in re.split(NEWLINE_PLACEHOLDER_PATTERN, fields) if item]
    result.extend(handle_replace_str_by_mapping(items, all_table, all_table_field, values))
    for new_value, replace_value in values.items():
        result.extend(handle_replace_str(items, all_table, all_table_field, new_value, replace_value))
    return result


def handle_replace_str(items, all_table, all_table_field, new_value, replace_value):
    result = list()
    for item in items:
        if REPLACE_STR not in item:
            continue
        tmp_fields = [x for x in re.split(rf"{REPLACE_STR}|,|\(|\)| ", item) if x]
        if len(tmp_fields) < 3:
            continue
        table_field = tmp_fields[0].split(DOT_PLACEHOLDER)
        if len(table_field) < 2:
            continue
        table, field = table_field[0], table_field[1]
        if table not in all_table or field not in all_table_field.get(table):
            continue
        separator, pos = tmp_fields[1], tmp_fields[2]
        result.append(REPLACE_STR_TEMPLATE.format(table_name=table, field_name=field, pre_value=replace_value,
                                                  cur_value=new_value, separator=separator, pos=pos))
    return result


def handle_replace_str_by_mapping(items, all_table, all_table_field, mapping):
    result = list()
    for item in items:
        if REPLACE_STR_BY_MAPPING not in item:
            continue
        match_obj = re.match(rf"^{REPLACE_STR_BY_MAPPING}\((.*)\)$", item)
        if match_obj is None:
            continue
        match_str = match_obj.group(1).strip()
        match_obj = re.match(r"([a-zA-Z_]+)\.([a-zA-Z_ ]+),(.*),([a-zA-Z_ ]+)$", match_str)
        if match_obj is None:
            continue
        table = match_obj.group(1).strip()
        field = match_obj.group(2).strip()
        if table not in all_table or field not in all_table_field.get(table):
            continue
        separator = match_obj.group(3).strip().strip("'\"")
        primary_key = match_obj.group(4).strip()
        result.append(REPLACE_STR_BY_MAPPING_TEMPLATE.format(
            table_name=table, field_name=field, separator=separator,
            mapping=json.dumps([dict(new_value=k, old_value=v) for k, v in mapping.items()]), primary_key=primary_key))
    return result
