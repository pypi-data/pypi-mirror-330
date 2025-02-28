# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 5/6/2024 9:51 AM
@Description: Description
@File: backup_by_database.py
"""
import threading
import time

from common_utils.conf.constant import TestEnv
from common_utils.conf.data_source_route import DataSourceRoute
from common_utils.format_time import now_yyyy_mm_dd
from migration.core.backup import mgmt_schema_history_and_backup

if __name__ == '__main__':
    sql_dir = r"D:\Temp-own"
    target_host = TestEnv.dev03
    is_compress = True
    databases = [
        # "eclinical_edc_dev_1968",
        "eclinical_cmd_company_common_96",
    ]
    for database in databases:
        sql_name = "_".join([database, target_host, now_yyyy_mm_dd()])
        data_source = DataSourceRoute().build_config(target_host, use_config_obj=False)
        data_source["db"] = database
        # ignore_table = ["eclinical_admin_database_sql"]
        ignore_table = None
        t = threading.Thread(target=mgmt_schema_history_and_backup,
                             args=(sql_dir, sql_name, is_compress, data_source, 1, ignore_table))
        t.start()
        print(f"Starting to back up database: {database}.")
