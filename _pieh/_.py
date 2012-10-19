#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import filecmp
import sqlite3

import markdown2

import config

class Application():
    def run(self):
        # 前期准备
        # 创建缺失的目录，连接配置文件
        self.initial()
        # 生成文章
        self.generate_posts()
        # 生成页面 index category tag link about resume
        self.generate_pages()
        # 关闭打开的连接
        self.finish()

    def initial(self):
        # 检查目录是否存在
        self._check_dir(config.path['source'])
        self._check_dir(config.path['post'])
        # 读取原来保存的数据数据
        self.data = Data(config.path['data'])

    def generate_posts(self):
        source_list = os.listdir(config.path['source']) # 获取源文件列表
        for source in source_list:
            post_data = Utils.parser_source(source) # 解析文件名
            status = self._check_status(post_data) # 检查文章
            if status == 0:
                self._insert_post(post_data) # 新文章 新建
            elif status == 1:
                self._update_post(post_data) # 有修改 覆盖
            else:
                self._move_post(post_data) # 无修改 不变
        self._delete_post() # 旧文章 删除

    def generate_pages(self):
        # 根据文章信息，生成index category tag页面
        # 生成link页面
        # 生成about页面
        # 生成resume页面
        pass

    def finish(self):
        self.data.close()

    def _check_status(self, post_data):
        """检查源文件情况
        0 新文件，新建
        1 有修改，覆盖
        2 无修改，不变
        """
        if os.path.exists(post_data['post_path']):
            if filecmp.cmp(post_data['source_path'], post_data['post_path']):
                return 2
            else:
                return 1
        else:
            return 0

    def _check_dir(self, path):
        """检查目录是否存在，不存在就创建一个"""
        if not os.path.exists(path):
            os.mkdir(path)

    def _insert_post(self, post_data):
        # 生成文章
        self._gen_post(post_data)
        # 插入记录
        self.data.insert_post(post_data)

    def _update_post(self, post_data):
        # 更新文章
        self._gen_post(post_data)
        # 更新记录
        self.data.update_post(post_data)

    def _move_post(self, post_data):
        # 移动记录
        self.data.move_post(post_data)

    def _delete_post(self):
        for row in self.data.query_old_post:
            os.remove(row['post_path'])
            if not os.listdir(row['post_dir']):
                os.removedirs(row['post_dir'])

    def _gen_post(self, post_data):
        """生成页面 添加页面信息"""
        category = ''
        tag = ''
        with open(post_data['source_path']) as source:
            for line in source.readline():
                if line == '-->': break
                if line.startswith('Category: '):
                    category = line.strip('Category: ')
                if line.startswith('Tag: '):
                    tag = line.strip('Tag: ')
            self._check_dir(post_data['post_dir'])
            with open(post_data['post_path'], 'w') as post:
                post.write(markdown2.markdown(source.read()))
        post_data['category'] = category
        post_data['tag'] = tag


class Utils():
    @classmethod
    def parser_filename(cls, filename):
        """解析源文件文件名"""
        # date_title.md -> (date, title)
        name = filename.rsplit('.', 1)[0]
        date_title = name.split('_', 1)
        post_data = {
            'source_name': filename,
            'source_path': os.path.join(config.path['source'], filename),
            'post_dir': os.path.join(config.path['post'], date_title[0]),
            'post_name': date_title[1],
        }
        post_data['post_path'] = os.path.join(
            post_data['post_dir'], post_data['post_name'])
        return post_data


class Data():
    # 记录文件的读写
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.isolation_level = None
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript('''
            CREATE TABLE IF NOT EXISTS posts (
                source_name TEXT NOT NULL,
                post_dir TEXT NOT NULL,
                post_path TEXT NOT NULL,
                category TEXT NOT NULL,
                tag TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS temporary (
                source_name TEXT NOT NULL,
                post_dir TEXT NOT NULL,
                post_path TEXT NOT NULL,
                category TEXT NOT NULL,
                tag TEXT NOT NULL
            );
            ''')

    def _drop_table(self, table_name):
        self.conn.execute('DROP TABLE IF EXISTS ?', (table_name,))

    def _raname_table(self, old_name, new_name):
        self.conn.execute('ALTER TABLE ? RENAME TO ?', (old_name, new_name))

    def insert_post(self, data):
        self.conn.execute('''
            INSERT INTO
            temporary (source_name, post_dir, post_path, category, tag)
            VALUES (?, ?, ?, ?, ?)''',
            (data['source_name'], data['post_dir'], data['post_path'],
             data['category'], data['tag']))

    def update_post(self, data):
        self.insert_post(data)
        self.conn.execute('DELETE FROM posts WHERE source_name=?',
                          (data['source_name'],))

    def move_post(self, data):
        cursor = self.conn.cursor
        cursor.execute(
            'SELECT category, tag FROM posts WHERE source_name=?',
            (data['source_name'],))
        r = cursor.fetchone()
        data['category'] = r['category']
        data['tag'] = r['tag']
        cursor.execute('DELETE FROM posts WHERE source_name=?',
                       (data['source_name'],))
        cursor.close()
        self.insert_post(data)

    def query_old_post(self):
        for row in self.conn.execute('SELECT post_path, post_dir FROM posts'):
            yield row

    def close(self):
        self._drop_table('posts')
        self._rename_table('temporary', 'posts')
        self.conn.close()

