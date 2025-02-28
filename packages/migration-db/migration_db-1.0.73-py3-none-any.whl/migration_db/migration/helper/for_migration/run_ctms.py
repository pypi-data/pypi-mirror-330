# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 12/5/2024 1:30 PM
@Description: Description
@File: run_etmf.py
"""
from common_utils.conf.constant import TestEnv
from common_utils.conf.data_source_route import DataSourceRoute
from common_utils.constant import AppEnum
from migration.core.build_test_platform_data import build_config_info
from migration.core.build_update_sql import BuildUpdateSQL

if __name__ == '__main__':
    database = "eclinical_ctms_dev_581"
    data_source = DataSourceRoute().build_config(TestEnv.dev03, use_config_obj=False)
    test_platform = dict(host="localhost", port=3306, db="eclinical_test_platform", password="admin123", user="root")
    config_info = build_config_info(test_platform, AppEnum.CTMS.id)
    _path = BuildUpdateSQL(database, data_source, assigned_study_id=2172, assigned_replace_study_id=1002).build(
        config_info)
    print(_path)
