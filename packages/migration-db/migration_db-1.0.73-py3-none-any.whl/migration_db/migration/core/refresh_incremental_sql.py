# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 5/6/2024 2:23 PM
@Description: Description
@File: refresh_incremental_sql.py
"""
import os
import shutil
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from common_utils.log import Logger
from common_utils.handle_git import git_add_safe, git_clone_with_credentials, is_latest, git_pull, \
    get_git_directory_structure, configure_git_credentials
from migration.core.incremental_sql import filter_by_pattern, copy_file


class LocalGitRepository:
    prefix = "Git-Repository-"

    def __init__(self):
        self.dir_path = None
        self.need_clone = None
        self.latest = False

    def init(self, is_rm=False, git_document_dir=None):
        git_repositories = self.query(git_document_dir)
        # 确认系统临时目录中是否存在GIT_PREFIX文件夹
        if len(git_repositories) == 0:
            self.need_clone = True
            if git_document_dir is not None:
                self.dir_path = os.path.join(git_document_dir, self.prefix + "8bhz66bi")
                os.makedirs(self.dir_path, exist_ok=True)
            else:
                self.dir_path = tempfile.mkdtemp(prefix=self.prefix)
        elif len(git_repositories) == 1:
            if is_rm is True:
                self.need_clone = True
                os.system(f"rmdir /s /q {self.dir_path}")
            else:
                self.need_clone = False
            self.dir_path = git_repositories[0]
        else:
            for git_repository in git_repositories:
                shutil.rmtree(git_repository)
            if git_document_dir is not None:
                self.dir_path = os.path.join(git_document_dir, self.prefix + "8bhz66bi")
                os.makedirs(self.dir_path, exist_ok=True)
            else:
                self.dir_path = tempfile.mkdtemp(prefix=self.prefix)
            self.need_clone = True

    def query(self, git_document_dir=None):
        temp_dir = git_document_dir or tempfile.gettempdir()
        git_repositories = []
        for root, dirs, files in os.walk(temp_dir):
            for dir_name in dirs:
                if dir_name.startswith(self.prefix):
                    git_repositories.append(os.path.join(root, dir_name))
        return git_repositories


def load_local_git_repository(url, user, pwd, branch_name, incremental_sql_dir, is_rm=False, git_document_dir=None,
                              count=None):
    r = LocalGitRepository()
    Logger().info("The {0} update of the code repository.".format(count))
    if count > 10:
        raise Exception("Tried to update the warehouse 10 times but failed.")
    try:
        r.init(is_rm, git_document_dir)
    except Exception as e:
        Logger().error(e)
    flag = False
    if r.dir_path is not None:
        try:
            if r.need_clone is True:
                Logger().info("Start cloning the repository.")
                git_add_safe(r.dir_path)
                git_clone_with_credentials(url, user, pwd, r.dir_path, branch_name)
                configure_git_credentials(r.dir_path, url, user, pwd)
                Logger().info("The repository was cloned successfully.")
            r.latest = is_latest(r.dir_path, branch_name)
        except Exception as e:
            Logger().error(e)
            flag = True
    else:
        flag = True
    if flag:
        count += 1
        return load_local_git_repository(url, user, pwd, branch_name, incremental_sql_dir, True, git_document_dir,
                                         count)
    return r


def refresh_git_incremental_file(url, user, pwd, branch_name, incremental_sql_dir, git_document_dir=None,
                                 force_update=False):
    count = 1
    r: LocalGitRepository = load_local_git_repository(url, user, pwd, branch_name, incremental_sql_dir,
                                                      git_document_dir=git_document_dir, count=count)
    if r.dir_path is not None and (
            r.latest is False or r.need_clone or len(os.listdir(incremental_sql_dir)) == 0 or force_update):
        if r.latest is False or r.need_clone:
            git_pull(r.dir_path, branch_name)
        copy_incremental_sql(r.dir_path, incremental_sql_dir)
        Logger().info("Updated successfully.")
    Logger().info(
        "refresh_git_incremental_file method ends\nRepository path: {0}\nLatest: {1}".format(r.dir_path, r.latest))


def copy_incremental_sql(local_git_repository_dir, incremental_sql_dir):
    items = get_git_directory_structure(local_git_repository_dir)
    f_result = filter_by_pattern(items)
    copy_file(incremental_sql_dir, local_git_repository_dir, f_result)
