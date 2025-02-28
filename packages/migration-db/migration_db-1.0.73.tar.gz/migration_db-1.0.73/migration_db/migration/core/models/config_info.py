# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 12/5/2024 2:04 PM
@Description: Description
@File: config_info.py
"""
from dataclasses import dataclass

from common_utils.dto.base_dto import BaseDto


@dataclass
class ConfigInfo(BaseDto):
    """
    ConfigInfo
    """
    data: list = None
    external_condition_fields_mapping: list = None
    table_actions: list = None
    sql_statement: list = None
