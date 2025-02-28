# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 2/4/2021 8:25 PM
@Description: Description
@File: edc_db.py
"""

from .base_db import BaseDb


class EdcDb(BaseDb):

    def __init__(self, data_source):
        super().__init__(data_source)

    def get_study_site_info(self):
        study_dto = self.fetchone("SELECT id, name, randomzied FROM eclinical_study;")
        items = self.fetchall("SELECT code FROM eclinical_study_site;")
        site_list = [item.get("code") for item in items]
        return dict(study_dto=study_dto, sites=site_list)
