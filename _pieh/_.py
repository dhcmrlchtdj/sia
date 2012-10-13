#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os.path

import config

def main():
    # TODO
    # 查找本地文件
    # 查找记录文件
    # 对比文件记录

    # 新文件/修改文件 新建
    # 旧文件 不变
    # 丢失文件 删除

    # 生成html
    Database.prepare_database()

class Database():
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
                id INTEGER PRIMARY KEY, -- id
                sha1 TEXT NOT NULL, -- 源文件sha1
                source TEXT NOT NULL, -- 源文件文件名
                post TEXT NOT NULL, -- 生成文件地址
                title TEXT NOT NULL, -- 文章标题
                author TEXT NOT NULL, -- 文章作者
                publish_time TEXT NOT NULL, -- 发布时间
                update_time TEXT NOT NULL, -- 更新时间
                category TEXT NOT NULL, -- 分类
                tag TEXT NOT NULL -- 标签
            );
            ''')


if __name__ == '__main__':
    main()
