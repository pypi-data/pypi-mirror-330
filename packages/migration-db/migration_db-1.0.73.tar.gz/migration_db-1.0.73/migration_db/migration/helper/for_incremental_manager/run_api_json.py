# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 1/7/2025 2:37 PM
@Description: Description
@File: run_api_json.py
"""
from common_utils.read_file import connect_to
from migration.core.models.extra_setting_dto import ApiDto

if __name__ == '__main__':
    dto = ApiDto.from_dict({
        "method": "post",
        "api": "/data-change/resolve/phase/capping/history",
        "json": {
            "includeKeyList": ["${sponor_id}_${study_id}_${lifecycle}"],
            "excludeKeyList": [],
            "lifecycle": ""
        }
    })
    a = dto.to_dict()
    file_path = r"D:\melen\my_tools\docs\business sql\incremental_extra\edc\a.json"
    b = connect_to(file_path).data

    print(a)
    print(b)
    print(a==b)
