# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 11/5/2024 3:53 PM
@Description: Description
@File: build_test_platform_data.py
"""
from migration.db.base_db import BaseDb


def build_external_condition_mapping(test_platform):
    items = BaseDb(test_platform).fetchall("SELECT * FROM eclinical_condition_field WHERE is_delete=FALSE;") or list()
    mapping = dict()
    for item in items:
        system_id = item.get("system_id")
        table_name = item.get("table_name")
        key = f"{system_id}_{table_name}"
        if mapping.get(key, None) is not None:
            mapping[key].append(item)
        else:
            system_table_list = list()
            system_table_list.append(item)
            mapping[key] = system_table_list
    return mapping


def get_data(test_platform, system_id):
    return BaseDb(test_platform).fetchall("""
            SELECT f.fields, f.app_source_field, af.data_type, af.code, af.admin_source_field, af.id, af.comment, f.id AS app_field_id
            FROM eclinical_app_field f JOIN eclinical_admin_field af ON f.admin_field_id = af.id
            WHERE f.system_id=%s AND f.is_delete=FALSE ORDER BY af.data_type, af.code; 
            """, system_id)


def get_table_actions(test_platform, system_id):
    return BaseDb(test_platform).fetchall(
        "SELECT * FROM eclinical_table_action WHERE is_delete=FALSE AND system_id=%s AND action_id!=100;",
        system_id)  # 100 为SQL_STATEMENT_CODE


def get_sql_statement(test_platform, system_id):
    return BaseDb(test_platform).fetchall(
        "SELECT * FROM eclinical_table_action WHERE is_delete=FALSE AND system_id=%s AND action_id=100;",
        system_id)  # 100 为SQL_STATEMENT_CODE


def build_config_info(test_platform, system_id):
    external_condition_fields_mapping = build_external_condition_mapping(test_platform)
    data = get_data(test_platform, system_id)
    table_actions = get_table_actions(test_platform, system_id)
    sql_statement = get_sql_statement(test_platform, system_id)
    return dict(data=data, external_condition_fields_mapping=external_condition_fields_mapping,
                table_actions=table_actions, sql_statement=sql_statement)
