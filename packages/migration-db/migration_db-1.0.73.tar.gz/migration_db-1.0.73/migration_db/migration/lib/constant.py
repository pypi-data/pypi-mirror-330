# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 2021/8/5 10:11
@Description: Description
@File: constant.py
"""
from enum import Enum, unique

OR_PLACEHOLDER = "||"
AND_PLACEHOLDER = "&&"
NEWLINE_PLACEHOLDER_PATTERN = "\r\n|\n"
MAPPING_DATA = "##MAPPING_DATA##"
DOT_PLACEHOLDER = "."
SOURCE_FILE_BASENAME = "source"
SOURCE_FILENAME = "{}.json".format(SOURCE_FILE_BASENAME)
INCREMENTAL_EXTRA = "incremental_extra"


@unique
class DataType(Enum):
    def __init__(self, code, label, description=None):
        self.code = code
        self.label = label
        self.description = description

    INT = (1, "Integer")
    STRING = (2, "String")
    BOOL = (3, "Boolean")

    @classmethod
    def from_code(cls, code):
        for member in cls:
            if member.code == code:
                return member
        return None


class BoolData(str):
    TRUE = "True"
    FALSE = "False"


TABLE_SCHEMA_HISTORY = "eclinical_schema_history"


@unique
class ValTypeEnum(Enum):

    def __init__(self, code, val, variable, label=None, is_show=False):
        self.code = code
        self.val = val
        self.variable = variable
        self.label = label
        self.is_show = is_show

    STUDY_ID = (3, None, "@study_id", "Local Study ID")
    SPONSOR_ID = (4, None, "@sponsor_id", "Local Sponsor ID")
    ENV_ID = (6, None, "@env_id", "Local Env ID")
    ASSIGNED_REPLACE_STUDY_ID = (7, None, "@assigned_replace_study_id", "Prod Study ID", True)
    IS_NOT_NULL = (8, "IS NOT NULL", "IS NOT NULL", "Not Null", True)
    PV_RECORD = (10, None, "pv.eclinical_entry_form_item_record.current_value")
    COMPANY_ID = (11, None, "@company_id", "Local Company ID")
    ID_REPLACE_VALUE = (12, "@replace_value", "@replace_value is int")
    STRING_REPLACE_VALUE = (
        13, "CONVERT(@replace_value USING utf8mb4) COLLATE utf8mb4_general_ci", "@replace_value is string")
    SITE_ID = (15, MAPPING_DATA, "@site_id", "Prod Site ID", True)
    CONSTANT = (16, None, "Constant", "Constant", True)

    # STUDY = (9, "study", "@study", "Constant")
    # SITE = (14, "site", "@site", "Constant")
    # FALSE = (99, False, "False", "Constant")
    # TRUE = (100, True, "True", "Constant")

    @classmethod
    def from_code(cls, code):
        for member in cls:
            if member.code == code:
                return member
        return None


ValTypeDesc = sorted({(item.code, item.label) for item in ValTypeEnum if item.is_show}, key=lambda x: x[1])


@unique
class AdminFieldEnum(Enum):

    def __init__(self, _id, code):
        self.id = _id
        self.code = code

    SITE_CODE = (1, "site_code")
    SITE_ID = (2, "site_id")
    STUDY_ID = (3, "study_id")
    SPONSOR_ID = (4, "sponsor_id")
    STUDY_NAME = (5, "study_name")


@unique
class TableActionEnum(Enum):

    def __init__(self, _id, description):
        self.id = _id
        self.description = description

    SET_FIELD_VALUE_TO_NULL = (1, "Set the value of the field to null")
    DELETE_ALL_DATA_IN_THE_TABLE = (2, "Delete all the data in the table")


@unique
class MigrationTypeEnum(Enum):

    def __init__(self, code, description):
        self.code = code
        self.description = description

    MYSQL = ("mysql", "migration by mysql")
    MYSQL_SHELL = ("mysqlsh", "migration by mysqlsh")
    MYSQL_CONNECTOR = ("mysql_connector", "migration by mysql-connector-python")


@unique
class IncrementalExtraEnum(Enum):

    def __init__(self, code, description):
        self.code = code
        self.description = description

    SQL = ("SQL", "Execute SQL files to process historical data")
    API = ("API", "Call the interface to process historical data")


@unique
class ExecutionOrderEnum(Enum):

    def __init__(self, code, description):
        self.code = code
        self.description = description

    BEFORE = ("Before", "Executes the script before executing the incremental script.")
    AFTER = ("After", "Execute the script after the incremental script has been executed.")
