# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 12/23/2020 1:08 PM
@Description: Description
@File: write_file.py
"""

import datetime
import json
import os
import warnings


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, bytes):
            # return str(obj, encoding='utf-8')
            return bytes.decode(obj)
        return json.JSONEncoder.default(self, obj)


def to_json_file(base_path, file_name, obj, sort_keys=True, indent=4):
    warnings.warn("to_json_file is deprecated.", DeprecationWarning)
    if not obj:
        return
    os.makedirs(base_path, exist_ok=True)
    path = f"{base_path}/{file_name}.json"
    with open(path, "w") as fp:
        json.dump(obj, fp, indent=indent, sort_keys=sort_keys, cls=ComplexEncoder)


def write_json_file(file_path, obj, sort_keys=True, indent=4):
    if not file_path or not isinstance(file_path, str):
        raise ValueError("文件路径不能为空，且必须为字符串。")
    if not file_path.lower().endswith('.json'):
        raise ValueError(f"文件路径无效：{file_path}。必须是以.json结尾的路径。")
    if not obj:
        raise ValueError("待写入的对象不能为空。")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as fp:
        json.dump(obj, fp, indent=indent, sort_keys=sort_keys, cls=ComplexEncoder)
