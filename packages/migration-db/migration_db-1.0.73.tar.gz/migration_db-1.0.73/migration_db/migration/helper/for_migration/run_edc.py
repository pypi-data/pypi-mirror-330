# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 2022/6/19 17:15
@Description: Description
@File: run_edc.py
"""
from common_utils.conf.data_source_route import DataSourceRoute
from common_utils.constant import AppEnum
from migration.core.build_test_platform_data import build_config_info
from migration.core.build_update_sql import BuildUpdateSQL

if __name__ == '__main__':
    database = "eclinical_edc_dev_820"
    data_source = DataSourceRoute().build_config("dev01", use_config_obj=False)
    test_platform = dict(host="localhost", port=3306, db="eclinical_test_platform", password="admin123", user="root")
    config_info = build_config_info(test_platform, AppEnum.EDC.id)
    _path = BuildUpdateSQL(database, data_source).build(config_info)
    print(_path)
