# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 12/5/2024 2:11 PM
@Description: Description
@File: base_dto.py
"""
from dataclasses import dataclass, fields, Field
from typing import Dict, Any, TypeVar, Type, get_origin, get_args

T = TypeVar('T', bound='BaseDto')


@dataclass
class BaseDto:

    def to_dict(self) -> Dict[str, Any]:
        data = dict()
        for f in fields(self):
            key = f.metadata.get('alias', f.name)
            value = getattr(self, f.name)
            if isinstance(value, BaseDto):
                value = value.to_dict()
            elif isinstance(value, list):
                value = [item.to_dict() if isinstance(item, BaseDto) else item for item in value]
            if not f.metadata.get('ignore', False):
                data[key] = value
        return data

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        kwargs = dict()
        for f in fields(cls):
            key = f.metadata.get("alias", f.name)
            if key in data:
                kwargs[f.name] = convert_value(f, data[key])
        return cls(**kwargs)


def convert_value(field: Field, value: Any) -> Any:
    origin = get_origin(field.type)
    if origin is not None:
        if isinstance(value, dict) and isinstance(field.type, type) and issubclass(field.type, BaseDto):
            return field.type.from_dict(value)
        if origin is list:
            item_type = get_args(field.type)[0]
            if issubclass(item_type, BaseDto):
                return [item_type.from_dict(item) for item in value]
        return value
    if isinstance(value, field.type):
        return value
    elif isinstance(value, int) and field.type is str:
        return str(value)
    elif isinstance(value, str) and field.type is int:
        if value.isdigit():
            return int(value)
        else:
            return value
    else:
        return value
