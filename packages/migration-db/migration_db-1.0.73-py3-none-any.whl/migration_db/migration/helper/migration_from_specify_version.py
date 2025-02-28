# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 7/25/2024 3:01 PM
@Description: Description
@File: migration_from_specify_version.py
"""
import os
from typing import List

from common_utils.conf.constant import TestEnv
from common_utils.conf.data_source_route import DataSourceRoute
from common_utils.constant import AppEnum, AppEnvEnum
from common_utils.database import Database
from common_utils.handle_str import ParseNameForAppInfo, ParseBizSqlForAppInfo
from common_utils.path import incremental_sql_dir_path
from common_utils.read_file import connect_to
from migration.core.execute_script import ExecuteScript
from migration.lib.mysql_task import MysqlTask


def execute_incremental_sql(data_source, start_sql_version_id, end_sql_version_id):
    """
    在incremental_sql_dir_path()目录下，执行增量SQL
    :param data_source: 数据源
    :param start_sql_version_id: 开始sql version id, >=
    :param end_sql_version_id: 结束sql version id, <=
    :return:
    """
    if data_source is None:
        raise Exception("Please set the data source.")
    database = data_source["db"]
    incremental_sql_path_dir: str = incremental_sql_dir_path()
    p = ParseNameForAppInfo().parse(database)
    sql_dir = os.path.join(incremental_sql_path_dir, p.app)
    source_file_data = connect_to(os.path.join(sql_dir, "source.json")).data
    execute_mapping = dict()
    for sql_name in source_file_data.keys():
        p = ParseBizSqlForAppInfo().parse(sql_name)
        if start_sql_version_id <= p.version_id <= end_sql_version_id:
            execute_mapping.update({p.version_id: sql_name})
    execute_mapping = dict(sorted(execute_mapping.items()))
    for sql_version_id, sql_name in execute_mapping.items():
        local_sql_path = os.path.join(sql_dir, sql_name)
        try:
            MysqlTask(**data_source).mysql_task(local_sql_path)
            ExecuteScript(data_source).init_schema_history_and_latest_sql_version(sql_version_id)
        except Exception as e:
            print(f"Execute increment({sql_name}) failed: {str(e)}.")


def batch_execute_incremental_sql(host, items, app):
    data_source = DataSourceRoute().build_config(host, use_config_obj=False)
    data_source_admin = DataSourceRoute().build_config(host, database="eclinical_admin")
    admin_db = Database(data_source_admin)
    for item in items:
        print(f"{item} is start.")
        _id, app_env = item.split("-")
        if app == AppEnum.DESIGN.code:
            app_env = AppEnvEnum.DEV.description
        database = "_".join(["eclinical", app, app_env, str(_id)])
        app_db = Database(DataSourceRoute().build_config(host, database=database))
        start_sql_version_id = get_start_sql_version_id(admin_db, app_db)
        end_sql_version_id = LATEST_SQL_VERSION.get(app)
        if start_sql_version_id > end_sql_version_id:
            print(f"{item} is end: {start_sql_version_id}>{end_sql_version_id}.")
            continue
        data_source["db"] = database
        execute_incremental_sql(data_source, start_sql_version_id, end_sql_version_id)
        print(f"{item} is end.")


def get_start_sql_version_id(admin_db: Database, app_db: Database):
    p = ParseNameForAppInfo().parse(app_db.name)
    if p.app in [AppEnum.CTMS.code, AppEnum.ETMF.code]:
        condition = "sponsor_id={0}".format(p.id)
    elif p.app in [AppEnum.DESIGN.code, AppEnum.EDC.code, AppEnum.IWRS.code]:
        condition = "study_id={0}".format(p.id)
    else:
        condition = None
    if condition is None:
        raise Exception("请设置condition")
    sql = ('SELECT sql_file_name FROM eclinical_admin_database_sql_execution WHERE system_name REGEXP %s AND '
           '{0} AND env_name=%s ORDER BY creator_dt LIMIT 1'.format(condition))
    item = admin_db.fetchone(sql, (p.app, p.app_env)) or dict()
    sql_file_name = item.get("sql_file_name")
    all_tables = app_db.get_all_tables()
    script = None
    li = [sql_file_name]
    if "eclinical_schema_history" in all_tables:
        sql = "SELECT * FROM eclinical_schema_history WHERE type='SQL' " \
              "AND success=TRUE ORDER BY installed_rank DESC LIMIT 1;"
        item = app_db.fetchone(sql) or dict()
        script = item.get("script")
    li.append(script)
    li = list(filter(lambda x: x is not None, li))
    if len(li) > 0:
        result = []
        for item in li:
            p = ParseBizSqlForAppInfo().parse(item)
            result.append(p.version_id)
        return max(result) + 1
    else:
        # return 100
        raise Exception("error")


def auto_fix(host):
    data_source = DataSourceRoute().build_config(host)
    db = Database(data_source)
    databases = db.get_all_databases()
    fix_dbs = list()
    for database in databases:
        d = ParseNameForAppInfo().parse(database)
        if d.app == AppEnum.CTMS.code:
            fix_dbs.append(f"{d.id}-{d.app_env}")
    print(fix_dbs)
    return fix_dbs


def auto_by_ids(ids: List[int]):
    li = list()
    for _id in ids:
        # for app_env in [AppEnvEnum.DEV.description, AppEnvEnum.UAT.description, AppEnvEnum.PROD.description]:
        for app_env in [AppEnvEnum.PROD.description]:
            li.append("{0}-{1}".format(_id, app_env))
    return li


LATEST_SQL_VERSION = {
    AppEnum.CTMS.code: 49,
    AppEnum.ETMF.code: 37,
    AppEnum.IWRS.code: 56,
    AppEnum.EDC.code: 94,
    AppEnum.DESIGN.code: 43,
    AppEnum.CODING.code: 6,
}

if __name__ == '__main__':
    target_host = TestEnv.dev03
    # app_env = AppEnv.dev
    # app = AppEnum.CTMS.code
    # _id = 359
    # database = "_".join(["eclinical", app, app_env, str(_id)])
    # start_sql_version_id = 17
    # end_sql_version_id = 38
    # data_source = DataSourceRoute().build_config(target_host, use_config_obj=False)
    # data_source["db"] = database
    # execute_incremental_sql(data_source, start_sql_version_id, end_sql_version_id)
    # items = ['845-dev', '846-dev', '847-dev']
    # items = auto_fix(target_host)
    # items = ["43-dev", "43-uat", "43-prod"]
    # handle_list = auto_by_ids([221, 220, 219, 218, 217])
    handle_list = auto_by_ids([599])
    app_name = AppEnum.CTMS.code
    batch_execute_incremental_sql(target_host, handle_list, app_name)
