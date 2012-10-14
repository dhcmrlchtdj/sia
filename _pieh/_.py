#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import sqlite3
import filecmp
import hashlib

import markdown2
import config

# TODO
# 新文件/修改文件 新建
# 旧文件 不变
# 丢失文件 删除

# 生成html

class Application():
    def main(self):
        self.initial()
        self.generate_posts()

    def initial(self):
        """创建各种文件夹"""
        pass

    def generate_posts(self):
        source_list = os.listdir(config.path['source'])
        for source in source_list:
            status = self._check_status(source)
            if status == 1:
                continue
            elif status == 0:
                self._update_post(source)
            else:
                self._insert_post(source)

    def _insert_post(self, filename):
        date, title = self._parser_filename(filename)
        directory = os.path.join(config.path['post'], date)
        if not os.exists(directory):
            os.mkdir(directory)
        source_file = self._source_path(filename)
        post_file = self._post_path(filename, date, title)
        with open(post_file, 'w') as post:
            post.write(markdown2.markdown_path(source_file))
        # TODO
        # 数据库存储信息

    def _update_post(self, source): pass
    def _delete_post(self, source): pass

    def _source_path(self, filename):
        return os.path.join(config.path['source'], filename)

    def _post_path(self, filename, date=None, title=None):
        if not (date and title):
            date, title = self._parser_filename(filename)
        return os.path.join(config.path['post'], date, title)

    def _parser_filename(self, filename):
        """return (date, title)"""
        name = filename.rsplit('.', 1)[0]
        return tuple(name.split('_', 1))


    def _check_status(self, filename):
        """return
        1 => equal
        0 => not equal
        -1 => post not found
        """
        source_file = self._source_path(filename)
        post_file = self._post_path(filename)
        if os.path.exists(post_file):
            if filecmp.cmp(source_file, post_file):
                return 1
            else:
                return 0
        else:
            return -1

    def _new_page(self, page): pass
    def generate_pages(self): pass


class Database():
    """数据库读写操作"""

    db = config.path['sqlite']

    @classmethod
    def prepare_database(cls):
        if os.path.exists(cls.db):
            conn = sqlite3.connect(cls.db)
            query = conn.execute('''
                SELECT count(*) FROM sqlite_master
                WHERE tbl_name in ("Posts", "Pages")
                ''')
            if query.fetchone()[0] == 2:
                return
        cls.initial_database()

    @classmethod
    def initial_database(cls):
        conn = sqlite3.connect(cls.db)
        conn.executescript('''
            DROP TABLE IF EXISTS Pages;
            DROP TABLE IF EXISTS Posts;
            CREATE TABLE Pages (
                id INTEGER PRIMARY KEY, --id
                sha1 TEXT NOT NULL, -- 页面sha1
                name TEXT NOT NULL, -- 页面名
                update_time TEXT NOT NULL -- 页面更新时间
            );
            CREATE TABLE Posts (
                sha TEXT NOT NULL,
                -- 文章的唯一标识
                key TEXT NOT NULL,
                -- 源文件 目标文件 标题 作者分类 标签 发布时间 更新时间
                -- source post title author category tag publish update
                value TEXT NOT NULL
                -- 值
            );
            ''')


if __name__ == '__main__':
    Application().main()
