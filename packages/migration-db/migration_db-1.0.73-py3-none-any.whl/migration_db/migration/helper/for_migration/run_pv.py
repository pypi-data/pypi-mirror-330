# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 2022/6/19 17:15
@Description: Description
@File: run_pv.py
"""
from common_utils.conf.data_source_route import DataSourceRoute
from migration.core.build_test_platform_data import build_external_condition_mapping, get_data
from migration.core.build_update_sql import BuildUpdateSQL

if __name__ == '__main__':
    data_base = "eclinical_pv_dev_816"
    data_source = DataSourceRoute().build_config("dev01", use_config_obj=False)
    # data_source = dict(host="localhost", port=3306, db="eclinical_test_platform", password="admin123",
    #                    user="root")
    test_platform = dict(host="localhost", port=3306, db="eclinical_test_platform", password="admin123",
                         user="root")
    external_condition_fields_mapping = build_external_condition_mapping(test_platform)
    data = get_data(test_platform, 8)
    config_info = dict(data=data, external_condition_fields_mapping=external_condition_fields_mapping)
    _path = BuildUpdateSQL(data_base, data_source, assigned_study_id=820, assigned_replace_study_id=790).build(
        config_info)
    print(_path)
