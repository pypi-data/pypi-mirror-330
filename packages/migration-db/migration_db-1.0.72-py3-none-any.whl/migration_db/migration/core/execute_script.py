# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 6/27/2022 10:46 AM
@Description: Description
@File: execute_script.py
"""
import os
import time

from common_utils.format_time import now_utc
from common_utils.handle_str import ParseBizSqlForAppInfo, ParseNameForAppInfo
from common_utils.path import incremental_sql_dir_path
from .incremental_manager.setting import IncrementalSqlSettingManager, init_api_client
from ..db.base_db import BaseDb
from ..lib.constant import TABLE_SCHEMA_HISTORY, ExecutionOrderEnum, IncrementalExtraEnum
from ..lib.mysql_task import MysqlTask
from ..lib.path import common_sql_path


class ExecuteScript:

    def __init__(self, data_source):
        self.data_source = data_source
        db = self.data_source.get("db")
        if db is not None:
            p = ParseNameForAppInfo().parse(db)
            app = p.app
            app_env = p.app_env
            hierarchy_level = p.hierarchy_level
        else:
            raise Exception("The db is empty.")
        self.app: str = app
        self.app_env = app_env
        self.hierarchy_level = hierarchy_level

    def execute_incremental_sql(self, ignore_error=False, latest_version=None, incremental_sql_dir=None,
                                request_id=None):
        if incremental_sql_dir is None:
            incremental_sql_dir = incremental_sql_dir_path()
        sql_dir = os.path.join(incremental_sql_dir, self.app)
        all_tables = BaseDb(self.data_source).get_all_tables()
        if TABLE_SCHEMA_HISTORY not in all_tables:
            table_schema_path = os.path.join(common_sql_path(), "{0}.sql".format(TABLE_SCHEMA_HISTORY))
            MysqlTask(**self.data_source).mysql_task(table_schema_path)
        sql = "SELECT script FROM eclinical_schema_history WHERE type='SQL' " \
              "AND success=TRUE ORDER BY installed_rank DESC LIMIT 1;"
        item = BaseDb(self.data_source).fetchone(sql)
        db_max_version = None
        if item is not None:
            script = item.get("script")
            p = ParseBizSqlForAppInfo().parse(script)
            db_max_version = p.version_id
        if db_max_version is None or db_max_version == latest_version:
            return
        version_file_mapping = dict()
        for root, dirs, files in os.walk(sql_dir):
            for sql_name in files:
                if not sql_name.endswith('.sql'):
                    continue
                p = ParseBizSqlForAppInfo().parse(sql_name)
                version = p.version_id
                if (latest_version is not None and version > latest_version) or version <= db_max_version:
                    continue
                hierarchy_level = p.hierarchy_level
                if self.hierarchy_level and hierarchy_level and self.hierarchy_level != hierarchy_level:
                    continue
                version_file_mapping.update({version: sql_name})
        version_file_mapping = sorted(version_file_mapping.items(), key=lambda s: s[0])
        sql_names = [i[-1] for i in version_file_mapping]
        m = IncrementalSqlSettingManager(os.path.dirname(incremental_sql_dir), app=self.app)
        client = init_api_client(
            request_id, app=self.app, app_env=self.app_env,
            ignore_error=ignore_error) if m.has_ttype_in_sqls(sql_names, IncrementalExtraEnum.API.code) else None
        for version, sql_name in version_file_mapping:
            is_execute = False
            try:
                item = BaseDb(self.data_source).fetchone(
                    f"SELECT * FROM eclinical_schema_history WHERE script='{sql_name}';")
            except Exception:
                raise
            if not item:
                if db_max_version and version > db_max_version:
                    is_execute = True
                elif db_max_version is None:
                    is_execute = True
                execution_time = 0
                try:
                    if is_execute:
                        m.execute_by_tag(self.data_source, client, sql_name, ExecutionOrderEnum.BEFORE.code,
                                         ignore_error)
                        start_time = time.time() * 1000
                        MysqlTask(**self.data_source).mysql_task(os.path.join(sql_dir, sql_name))
                        execution_time = time.time() * 1000 - start_time
                        success = True
                    else:
                        continue
                except Exception as e:
                    success = False
                    if ignore_error is False:
                        raise RuntimeError(f"An error occurred while executing {sql_name}: {e}") from e
                # insert the sql executed record
                if success is False:
                    continue
                max_item = BaseDb(self.data_source).fetchone(
                    f"SELECT installed_rank FROM eclinical_schema_history ORDER BY installed_rank DESC LIMIT 1;")
                max_id = max_item.get('installed_rank') if max_item else 0
                if self.hierarchy_level is not None:
                    description = "{0} {1} business schema incremental sql".format(self.app, self.hierarchy_level)
                else:
                    description = "{0} business schema incremental sql".format(self.app)
                BaseDb(self.data_source).insert(
                    "eclinical_schema_history",
                    dict(installed_rank=max_id + 1, version=version, type="SQL", script=sql_name, checksum=0,
                         execution_time=execution_time, description=description, installed_by="test_platform",
                         installed_on=now_utc(), success=1), name=sql_name)
                m.execute_by_tag(self.data_source, client, sql_name, ExecutionOrderEnum.AFTER.code, ignore_error)

    def init_schema_history_and_latest_sql_version(self, latest_version_id):
        if latest_version_id is None:
            return
        all_tables = BaseDb(self.data_source).get_all_tables()
        if TABLE_SCHEMA_HISTORY not in all_tables:
            table_schema_path = os.path.join(common_sql_path(), "{0}.sql".format(TABLE_SCHEMA_HISTORY))
            MysqlTask(**self.data_source).mysql_task(table_schema_path)
        sql = "SELECT * FROM eclinical_schema_history WHERE type='SQL' " \
              "AND success=TRUE ORDER BY installed_rank DESC LIMIT 1;"
        item = BaseDb(self.data_source).fetchone(sql)
        db_max_version = None
        installed_rank = 0
        if item is not None:
            script = item.get("script")
            installed_rank = item.get("installed_rank")
            p = ParseBizSqlForAppInfo().parse(script)
            db_max_version = p.version_id
        flag = False
        if db_max_version is None:
            flag = True
        elif db_max_version < latest_version_id:
            flag = True
        if flag:
            # insert the latest sql_version
            if self.hierarchy_level is None:
                sql_name = "V{0}__{1}_business_schema_incremental_sql.sql".format(latest_version_id, self.app)
                description = "{0} business schema incremental sql".format(self.app)
            else:
                sql_name = "V{0}__{1}_{2}_business_schema_incremental_sql.sql".format(
                    latest_version_id, self.app, self.hierarchy_level)
                description = "{0} {1} business schema incremental sql".format(self.app, self.hierarchy_level)
            new_record_installed_rank = installed_rank + 1
            sql = "SELECT MAX(installed_rank) max_installed_rank FROM `eclinical_schema_history`;"
            max_installed_rank = BaseDb(self.data_source).fetchone(sql).get("max_installed_rank") or 0
            if max_installed_rank >= new_record_installed_rank:
                new_record_installed_rank = max_installed_rank + 1
            BaseDb(self.data_source).insert(
                "eclinical_schema_history",
                dict(installed_rank=new_record_installed_rank, version=latest_version_id, type="SQL", script=sql_name,
                     checksum=0, execution_time=0, description=description, installed_by="test_platform",
                     installed_on=now_utc(), success=1), name=sql_name)
