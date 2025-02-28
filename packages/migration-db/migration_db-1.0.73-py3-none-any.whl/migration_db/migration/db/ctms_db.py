# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 11/12/2024 3:27 PM
@Description: Description
@File: ctms_db.py
"""
from .base_db import BaseDb


class CtmsDb(BaseDb):

    def __init__(self, data_source):
        super().__init__(data_source)

    def get_study_site_info(self, study_id):
        study_dto = self.fetchone("SELECT id, name, randomize as randomzied FROM eclinical_ctms_study WHERE id=%s;",
                                  study_id)
        if not study_dto:
            raise Exception(f"未查询到studyId:{study_dto}。")
        site_list = self.get_site_info(study_id)
        depots = self.get_study_depot_info(study_id)
        return dict(study_dto=study_dto, sites=site_list, depots=depots)

    def get_site_info(self, study_id):
        sql = """SELECT DISTINCT ss.site_code FROM eclinical_ctms_study_site ss
                JOIN eclinical_ctms_site s ON ss.site_id=s.id
                WHERE ss.study_id=%s;"""
        items = self.fetchall(sql, study_id) or list()
        return [item.get("site_code") for item in items]

    def get_study_depot_info(self, study_id):
        sql = """SELECT DISTINCT d.`name`, sd.number FROM eclinical_ctms_study_depot sd
                JOIN eclinical_ctms_depot d ON sd.depot_id=d.id
                WHERE sd.study_id=%s;"""
        return self.fetchall(sql, study_id)
