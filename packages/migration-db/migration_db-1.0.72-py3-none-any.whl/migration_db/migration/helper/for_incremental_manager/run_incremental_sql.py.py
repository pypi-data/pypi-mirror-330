# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 6/17/2024 10:38 AM
@Description: Description
@File: run.py
"""
from migration.core.incremental_manager.setting import IncrementalSqlSettingManager

if __name__ == '__main__':
    m = IncrementalSqlSettingManager(app="edc")
    a = m.get("V80__edc_business_schema_incremental_sql.sql")
    print(a)
    a = m.has_extra_ttype("V90__edc_business_schema_incremental_sql.sql", "API")
    print(a)
    # m.update("V80__edc_business_schema_incremental_sql.sql", "SQL", "update_audit_trail_sql.sql",
    #          "Before")
    # m.delete("V80__edc_business_schema_incremental_sql.sql", "update_audit_trail_sql.sql")
