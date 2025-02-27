# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 7/18/2022 10:03 AM
@Description: Description
@File: format_time.py
"""

from datetime import datetime, timezone

import pytz


def now() -> datetime:
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz).replace(microsecond=0)


def now_yyyy_mm_dd() -> str:
    return now().strftime("%Y-%m-%d")


def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def now_for_file() -> str:
    return now().strftime("%Y-%m-%d %H-%M-%S")
