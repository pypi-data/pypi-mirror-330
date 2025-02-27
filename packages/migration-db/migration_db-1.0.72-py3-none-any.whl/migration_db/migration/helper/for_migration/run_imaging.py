# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 2024/11/5 15:56
@Description: Description
@File: run_imaging.py
"""
from common_utils.conf.data_source_route import DataSourceRoute
from common_utils.constant import AppEnum
from migration.core.build_test_platform_data import build_external_condition_mapping, get_data, get_table_actions
from migration.core.build_update_sql import BuildUpdateSQL

if __name__ == '__main__':
    database = "eclinical_imaging_dev_2071"
    system_id = AppEnum.IMAGING.id
    data_source = DataSourceRoute().build_config("dev03", use_config_obj=False)
    # data_source = dict(host="localhost", port=3306, db="eclinical_test_platform", password="admin123",
    #                    user="root")
    test_platform = dict(host="localhost", port=3306, db="eclinical_test_platform", password="admin123",
                         user="root")
    external_condition_fields_mapping = build_external_condition_mapping(test_platform)
    data = get_data(test_platform, system_id)
    table_actions = get_table_actions(test_platform, system_id)
    config_info = dict(data=data, external_condition_fields_mapping=external_condition_fields_mapping,
                       table_actions=table_actions)
    _path = BuildUpdateSQL(database, data_source).build(config_info)
    print(_path)
