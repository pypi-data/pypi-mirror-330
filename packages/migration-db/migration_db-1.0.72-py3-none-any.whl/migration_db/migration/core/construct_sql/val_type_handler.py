# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 12/19/2024 2:28 PM
@Description: Description
@File: val_type_handler.py
"""
from common_utils.log import Logger
from migration.lib.constant import ValTypeEnum, DataType, BoolData

TYPE_CAST_MAP = {
    DataType.STRING.code: str,
    DataType.INT.code: int,
    DataType.BOOL.code: lambda x: x.lower() not in [BoolData.FALSE.lower(), "0"]
}


def cast_data(data, data_type):
    cast_func = TYPE_CAST_MAP.get(data_type, str)
    try:
        return cast_func(data)
    except (ValueError, AttributeError) as e:
        Logger().error(f"Type casting failed for value '{data}' with type '{data_type}': {e}")
        return data


class ValTypeHandler:

    def __init__(self, data):
        self.data = data

    def get(self, code, condition=None):
        condition = condition or dict()
        if code == ValTypeEnum.CONSTANT.code:
            val_data_type = condition.get("val_data_type", DataType.STRING.code)
            val = condition.get("val", str())
            return cast_data(val, val_data_type)
        return self.data.get(code)
