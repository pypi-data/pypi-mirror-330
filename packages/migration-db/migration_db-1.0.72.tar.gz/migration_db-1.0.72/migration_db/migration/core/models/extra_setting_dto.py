# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 1/7/2025 10:26 AM
@Description: for incremental sql
@File: extra_setting_dto.py
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from common_utils.dto.base_dto import BaseDto


@dataclass
class ExtraSettingDto(BaseDto):
    """
    ExtraSettingDto
    """
    name: str = None
    filename: str = None
    tag: str = None
    time: datetime = None
    type: str = None
    sn: int = None


@dataclass
class ApiDto(BaseDto):
    """
    ApiDto
    """
    method: str = None
    api: str = None
    json: Optional[Dict[str, Any]] = None
