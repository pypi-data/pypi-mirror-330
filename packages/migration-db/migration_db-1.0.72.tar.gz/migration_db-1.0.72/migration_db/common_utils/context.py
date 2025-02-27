# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 1/7/2025 5:41 PM
@Description: Description
@File: context.py
"""
from contextvars import ContextVar
from typing import Optional, Any


class ApplicationContext:
    """应用上下文管理，提供线程/协程安全的用户信息存取功能"""
    _user_info: ContextVar[Any] = ContextVar("user_info", default=None)

    @classmethod
    def set_user_info(cls, user_info: Any) -> None:
        """设置用户信息"""
        cls._user_info.set(user_info)

    @classmethod
    def get_user_info(cls) -> Optional[Any]:
        """获取用户信息"""
        return cls._user_info.get()


application_context = ApplicationContext()
