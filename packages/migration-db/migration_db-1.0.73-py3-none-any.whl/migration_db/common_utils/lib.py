# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 7/14/2023 11:27 AM
@Description: Description
@File: lib.py
"""
import os

import numpy as np


def is_na_no(sth) -> bool:
    """
    NaN、None或者空字符串返回True，其他情况返回False
    """
    if sth == 0:
        return False
    if not sth:
        return True
    if isinstance(sth, float):
        if np.isnan(sth):
            return True
    return False


def check_file_path():
    def __wrapper__(func):
        def __inner__(*args, **kwargs):
            _path = func(*args, **kwargs)
            return (_path and os.path.exists(_path)) and _path or None

        return __inner__

    return __wrapper__


def param_is_digit(param):
    return (type(param) is str and param.isdigit()) or type(param) is int


def get_class_attr_values(obj: object):
    result = list()
    for var_name, var_value in vars(obj).items():
        if not var_name.startswith('__') and not callable(var_value):
            result.append(var_value)
    return result


def split_list(lst, n):
    """将一组数字拆分成n个组，形成一个列表"""
    quotient = len(lst) // n
    remainder = len(lst) % n
    result = []
    start = 0
    for i in range(n):
        if i < remainder:
            end = start + quotient + 1
        else:
            end = start + quotient
        result.append(lst[start:end])
        start = end
    return result


def quote_identifier(identifier):
    if identifier.startswith("`") and identifier.endswith("`"):
        return identifier
    return "`{0}`".format(identifier)
