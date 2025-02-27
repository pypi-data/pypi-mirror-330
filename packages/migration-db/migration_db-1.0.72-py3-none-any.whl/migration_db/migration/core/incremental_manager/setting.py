# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 1/7/2025 10:35 AM
@Description: Description
@File: setting.py
"""
import os
import traceback
from datetime import datetime

from api_requester.core.call_api import ApiRequester
from werkzeug.datastructures import FileStorage

from common_utils.context import application_context
from common_utils.format_time import now_utc
from common_utils.handle_str import ParseBizSqlForAppInfo
from common_utils.log import Logger
from common_utils.path import build_biz_sql_docs
from common_utils.read_file import connect_to
from common_utils.write_file import write_json_file
from migration.core.models.extra_setting_dto import ExtraSettingDto, ApiDto
from migration.lib.constant import SOURCE_FILENAME, INCREMENTAL_EXTRA, IncrementalExtraEnum
from migration.lib.mysql_task import MysqlTask


def init_api_client(request_id=None, user_info=None, app=None, app_env=None, ignore_error=False):
    try:
        if not user_info:
            user_info = application_context.get_user_info()
        if not user_info:
            Logger().info(f"{request_id}: No user_info found")
            return None
        # 使用 getattr 方法获取属性，提供默认值
        username = getattr(user_info, 'usr', getattr(user_info, 'username', None))
        password = getattr(user_info, 'pwd', getattr(user_info, 'password', None))
        app = app or user_info.app
        app_env = app_env or user_info.app_env
        role = getattr(user_info, 'role', None)
        Logger().info(f"{request_id}: {user_info.__dict__}")
        if user_info:
            c = ApiRequester(username, password, user_info.sponsor, user_info.study, user_info.test_env,
                             app_env, app, user_info.company, role, external=False)
            c.login()
            return c
    except Exception:
        if ignore_error:
            raise
        return None


class IncrementalSqlSettingManager:

    def __init__(self, root: str = None, sql_name: str = None, app=None):
        self.root: str = root or build_biz_sql_docs()
        if sql_name:
            p: ParseBizSqlForAppInfo = ParseBizSqlForAppInfo().parse(sql_name)
            app = app or p.app
        self.app = app
        self.extra_app_dir = os.path.join(self.root, INCREMENTAL_EXTRA, app)
        self.source_filepath = self.get_cwd_filepath(SOURCE_FILENAME)

    def check(self, user_info, ignore_error=False):
        if self.has_ttype_in_app(IncrementalExtraEnum.API.code):
            init_api_client(user_info=user_info, app=self.app, ignore_error=ignore_error)

    def get_cwd_filepath(self, filename):
        return os.path.join(self.extra_app_dir, filename)

    def load_cwd_file(self, filename, raw=False):
        filepath = os.path.join(self.extra_app_dir, filename)
        if raw:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        else:
            f = connect_to(filepath, ignore_error=True)
            return f.data if f else {}

    def load_source_file(self):
        f = connect_to(self.source_filepath, ignore_error=True)
        return f.data if f else {}

    def get(self, sql_name):
        data = self.load_source_file()
        items = data.get(sql_name) or list()
        result = []
        date_format = "%Y-%m-%d %H:%M:%S"
        for item in items:
            dto = ExtraSettingDto.from_dict(item)
            if isinstance(dto.time, str):
                dto.time = datetime.strptime(dto.time, date_format)
            result.append(dto)
        return result

    def get_by_sn(self, sql_name, sn):
        return next((item for item in self.get(sql_name) if item.sn == sn), None)

    def save(self, data):
        write_json_file(self.source_filepath, data)

    def update(self, sql_name, ttype, name, execution_order):
        data = self.load_source_file()
        flag = False
        if sql_name in data:
            items = data[sql_name]
            for item in items:
                dto = ExtraSettingDto.from_dict(item)
                if dto.name == name and dto.type == ttype:
                    dto.tag = execution_order
                    dto.time = now_utc()
                    flag = True
                    item.update(**dto.to_dict())
        if flag:
            self.save(data)

    def delete(self, sql_name, sn):
        data = self.load_source_file()
        flag = False
        delete_filename = None
        if sql_name in data:
            items = data[sql_name]
            delete_item = None
            for item in items:
                dto = ExtraSettingDto.from_dict(item)
                if dto.sn == sn:
                    delete_item = item
                    delete_filename = dto.filename
                    flag = True
                    break
            if flag:
                items.remove(delete_item)
                items = sorted(items, key=lambda i: i["sn"])
                for sn, item in enumerate(items, start=1):
                    item["sn"] = sn

        if flag:
            self.save(data)
            file_path = self.get_cwd_filepath(delete_filename)
            if os.path.exists(file_path):
                os.remove(file_path)

    def add_or_update(self, sql_name, sn, name, execution_order=None, ttype=None, filename: str = None, file=None):
        data = self.load_source_file()
        flag = False
        if sn:
            items = data.get(sql_name, [])
            for item in items:
                dto = ExtraSettingDto.from_dict(item)
                if dto.sn == sn:
                    dto.name = name or dto.name
                    dto.tag = execution_order or dto.tag
                    dto.type = ttype or dto.type
                    dto.filename = filename or dto.filename
                    dto.time = now_utc()
                    item.update(**dto.to_dict())
                    flag = True
                    break
        if not flag:
            sn = len(data.get(sql_name, [])) + 1
            data.setdefault(sql_name, [])
            items = data[sql_name]
            dto = ExtraSettingDto(name, filename, execution_order, now_utc(), ttype, sn)
            items.append(dto.to_dict())
        self.save(data)
        if isinstance(file, FileStorage):
            file_path = self.get_cwd_filepath(filename)
            file.save(file_path)

    def has_ttype_in_sql(self, sql_name, ttype) -> bool:
        return any(item.type == ttype for item in self.get(sql_name))

    def has_ttype_in_sqls(self, sql_names, ttype) -> bool:
        return any(
            ExtraSettingDto.from_dict(item).type == ttype
            for sql_name in sql_names
            for item in self.load_source_file().get(sql_name, [])
        )

    def has_ttype_in_app(self, ttype) -> bool:
        """
        检查在当前应用下的增量脚本中是否存在指定类型的额外设置。

        参数:
            ttype: 要检查的类型。

        返回:
            bool: 如果存在指定类型，返回 True；否则返回 False。
        """
        return any(
            ExtraSettingDto.from_dict(item).type == ttype
            for items in self.load_source_file().values()
            for item in items
        )

    def get_by_tag(self, sql_name, tag):
        items = list()
        for item in self.get(sql_name):
            if item.tag == tag:
                items.append(item)
        items = sorted(items, key=lambda i: i.sn)
        return items

    def execute_by_tag(self, data_source, client, sql_name, tag, ignore_error=False):
        try:
            for item in self.get_by_tag(sql_name, tag):
                if item.type == IncrementalExtraEnum.SQL.code:
                    MysqlTask(**data_source).mysql_task(self.get_cwd_filepath(item.filename))
                elif item.type == IncrementalExtraEnum.API.code:
                    if not client:
                        return Logger().warn(f"No client.")
                    replacer = client.user_replacer()
                    data = self.load_cwd_file(item.filename)
                    Logger().info(data)
                    dto = ApiDto.from_dict(data)
                    if isinstance(dto.json, str):
                        json_value = replacer.replace(dto.json)
                        if json_value:
                            dto.json = eval(json_value)
                        else:
                            dto.json = None
                    dto.api = replacer.replace(dto.api)
                    client.request(dto.method, dto.api, json=dto.json)
                Logger().info(f"{item.type} ({item.tag}-{item.name}) successfully executed.")
        except Exception:
            traceback.print_exc()
            if ignore_error:
                raise


class ApiJson:

    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, method, api, json):
        dto = ApiDto(method, api, json)
        write_json_file(self.file_path, dto.to_dict())

    def delete(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
