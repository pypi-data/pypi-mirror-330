# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 1/9/2024 4:26 PM
@Description: Description
@File: constant.py
"""
from enum import unique, Enum


@unique
class AppEnvEnum(Enum):

    def __init__(self, code, description):
        self.code = code
        self.description = description

    DEV = ("DEV", "dev")
    UAT = ("UAT", "uat")
    PROD = ("PROD", "prod")


@unique
class HierarchyLevel(Enum):

    def __init__(self, code, level_name):
        self.code = code
        self.level_name = level_name

    COMPANY = (1, "company")
    SPONSOR = (2, "sponsor")
    STUDY = (3, "study")


@unique
class AppEnum(Enum):

    def __init__(self, system_id, code, description, alais=None):
        self.id = system_id
        self.code = code
        self.description = description
        self.alais = alais

    ADMIN = (1, "admin", "ADMIN")
    CTMS = (2, "ctms", "CTMS")
    ETMF = (3, "etmf", "eTMF")
    DESIGN = (4, "design", "DESIGN")
    EDC = (5, "edc", "EDC")
    IWRS = (6, "iwrs", "IWRS")
    E_CONSENT = (7, "econsent", "eConsent")
    PV = (8, "pv", "PV")
    CODING = (10, "coding", "CODING")
    IMAGING = (11, "imaging", "Eclinical IMAGING System")
    CMD = (12, "cmd", "Eclinical CMD System", "ecmd")
    IRC = (13, "irc", "Eclinical IRC System")

    @classmethod
    def get_by_code(cls, code):
        if isinstance(code, str):
            for member in cls:
                if member.code == code.lower():
                    return member
        return None

    @classmethod
    def get_system_id_by_code(cls, code):
        member = cls.get_by_code(code)
        if member is not None:
            return member.id
        raise ValueError(f"No member found with code: {code}")


@unique
class BizSqlType(Enum):

    def __init__(self, code, description):
        self.code = code
        self.description = description

    INITIAL = (1, "initial")
    INCREMENTAL = (2, "incremental")
