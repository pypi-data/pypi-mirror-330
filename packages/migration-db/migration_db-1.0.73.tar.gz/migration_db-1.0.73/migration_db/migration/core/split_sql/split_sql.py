# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 12/21/2022 4:22 PM
@Description: Description
@File: split_sql.py
"""
import re
from enum import Enum, unique

from common_utils.calc_time import calc_func_time
from common_utils.constant import AppEnum

REGEX_INSERT_INTO = r"INSERT INTO (()|(`)){0}(()|(`)) VALUES \(.*"
REGEX_CREATE_TABLE = r"CREATE TABLE (()|(`)){0}(()|(`)) \(.*"
RELATE_INFOS = ["INSERT INTO", "CREATE TABLE"]
SPLIT_FLAG = b";\n"


class RegexType:
    complete = "Complete"
    incomplete = "Incomplete"


@unique
class BaseEnum(Enum):
    def __init__(self, pattern, flags, table):
        self.pattern = pattern.format(table)
        self.flags = flags
        self.table = table


class EDCRegexEnum(BaseEnum):
    STUDY_SITE_INSERT_INTO = (REGEX_INSERT_INTO, re.I, "eclinical_study_site")
    STUDY_INSERT_INTO = (REGEX_INSERT_INTO, re.I, "eclinical_study")
    STUDY_SITE_CREATE_TABLE = (REGEX_CREATE_TABLE, re.I | re.M, "eclinical_study_site")
    STUDY_CREATE_TABLE = (REGEX_CREATE_TABLE, re.I | re.M, "eclinical_study")


class IWRSRegexEnum(BaseEnum):
    STUDY_SITE_INSERT_INTO = (REGEX_INSERT_INTO, re.I, "eclinical_iwrs_site")
    STUDY_INSERT_INTO = (REGEX_INSERT_INTO, re.I, "eclinical_iwrs_study")
    STUDY_SITE_CREATE_TABLE = (REGEX_CREATE_TABLE, re.I | re.M, "eclinical_iwrs_site")
    STUDY_CREATE_TABLE = (REGEX_CREATE_TABLE, re.I | re.M, "eclinical_iwrs_study")

    DEPOT_INSERT_INTO = (REGEX_INSERT_INTO, re.I, "eclinical_iwrs_depot")
    DEPOT_CREATE_TABLE = (REGEX_CREATE_TABLE, re.I | re.M, "eclinical_iwrs_depot")


class DesignRegexEnum(BaseEnum):
    STUDY_INSERT_INTO = (REGEX_INSERT_INTO, re.I, "eclinical_study")
    STUDY_CREATE_TABLE = (REGEX_CREATE_TABLE, re.I | re.M, "eclinical_study")


class CtmsRegexEnum(BaseEnum):
    STUDY_INSERT_INTO = (REGEX_INSERT_INTO, re.I, "eclinical_ctms_study")
    STUDY_CREATE_TABLE = (REGEX_CREATE_TABLE, re.I | re.M, "eclinical_ctms_study")
    DEPOT_INSERT_INTO = (REGEX_INSERT_INTO, re.I, "eclinical_ctms_depot")
    DEPOT_CREATE_TABLE = (REGEX_CREATE_TABLE, re.I | re.M, "eclinical_ctms_depot")
    STUDY_DEPOT_INSERT_INTO = (REGEX_INSERT_INTO, re.I, "eclinical_ctms_study_depot")
    STUDY_DEPOT_CREATE_TABLE = (REGEX_CREATE_TABLE, re.I | re.M, "eclinical_ctms_study_depot")
    SITE_INSERT_INTO = (REGEX_INSERT_INTO, re.I, "eclinical_ctms_site")
    SITE_CREATE_TABLE = (REGEX_CREATE_TABLE, re.I | re.M, "eclinical_ctms_site")
    STUDY_SITE_INSERT_INTO = (REGEX_INSERT_INTO, re.I, "eclinical_ctms_study_site")
    STUDY_SITE_CREATE_TABLE = (REGEX_CREATE_TABLE, re.I | re.M, "eclinical_ctms_study_site")


APP_REGEX_MAP = {
    AppEnum.EDC.code: EDCRegexEnum,
    AppEnum.IWRS.code: IWRSRegexEnum,
    AppEnum.DESIGN.code: DesignRegexEnum,
    AppEnum.CTMS.code: CtmsRegexEnum,
}


class StudySiteSQLDto:

    def __init__(self, sql=None, tables=None, has_generate=False):
        self.sql = sql
        self.tables = tables or list()
        self.has_generate = has_generate


def read_in_block(file_path):
    block_size = 1024 * 10
    with open(file_path, "rb") as f:
        pre_items = []
        while True:
            block = f.read(block_size)  # 每次读取固定长度到内存缓冲区
            if block:
                result = []
                if SPLIT_FLAG in block:
                    has_split_symbol = True
                else:
                    has_split_symbol = False
                if len(pre_items) > 0:
                    if has_split_symbol:
                        result.append(pre_items[-1] + block.split(SPLIT_FLAG)[0])
                        result.extend(block.split(SPLIT_FLAG)[1:-1])
                        pre_items = block.split(SPLIT_FLAG)
                    else:
                        pre_items = [pre_items[-1] + block]
                else:
                    if has_split_symbol:
                        result.extend(block.split(SPLIT_FLAG)[:-1])
                        pre_items = block.split(SPLIT_FLAG)
                    else:
                        pre_items = [block]
                yield result
            else:
                return  # 如果读取到文件末尾，则退出


@calc_func_time
def generate_study_site_sql_dto(file_path, app) -> StudySiteSQLDto or None:
    regex_enum = APP_REGEX_MAP.get(app)
    if regex_enum is None:
        return None
    tables = list({i.table for i in regex_enum})
    check_num = len(tables) * 2
    dto = StudySiteSQLDto()
    result = list()
    for block in read_in_block(file_path):
        for item in block:
            try:
                text = item.decode("utf-8").replace("\n", "").replace("\r", "")
                if all(i not in text for i in RELATE_INFOS):
                    continue
                if len(result) >= check_num:  # //todo 校验跳出循环的条件
                    break
                if all(i not in text for i in tables):
                    continue
                for regex in regex_enum:
                    m = re.match(regex.pattern, text, regex.flags)
                    if m:
                        result.append(item + SPLIT_FLAG)
                        if dto.has_generate is False:
                            dto.has_generate = True
                        if regex.table not in dto.tables:
                            dto.tables.append(regex.table)
                        break
            except BaseException as e:
                print(e)
        if len(result) >= check_num:  # //todo 校验跳出循环的条件
            break
    dto.sql = b"".join(result)
    return dto.has_generate is True and dto or None
