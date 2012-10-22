#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

import os
import sys
from os.path import join, exists
import filecmp
import shutil
import sqlite3

import markdown
from tornado.template import Loader

from config import path as PATH


#TODO 判断函数有误 需修改
class Application():
    def clear(self):
        def _rm(path, command=os.remove):
            if exists(path):
                command(path)
                print('delete {}.'.format(path))
        _rm(PATH['post'], shutil.rmtree)
        _rm(PATH['data'])
        _rm(join(PATH['app'], 'index.html'))
        _rm(join(PATH['app'], 'category.html'))
        _rm(join(PATH['app'], 'tag.html'))
        _rm(join(PATH['app'], 'link.html'))
        _rm(join(PATH['app'], 'about.html'))
        print('clean.')

    def build(self):
        self.initial() # 创建缺失的目录，连接配置文件
        self.generate_posts() # 生成文章
        self.generate_pages() # 生成页面 index category tag link about
        self.finish() # 关闭打开的连接
        print('build.')

    def initial(self):
        # 检查目录是否存在
        self._mkdir(PATH['source'])
        self._mkdir(PATH['post'])
        # 读取原来保存的数据数据
        self.data = Data(PATH['data'])
        # 读取模板
        self.template = Loader(PATH['template'], autoescape=None)
        # 是否重建页面
        self.rebuild_pages = False

    def generate_posts(self):
        def _parser_filename(filename):
            """解析源文件文件名"""
            # date_title.md -> (date, title)
            name = filename.rsplit('.', 1)[0]
            date_title = name.split('_', 1)
            post_data = {
                'source_name': filename,
                'source_path': join(PATH['source'], filename),
                'post_dir': join(PATH['post'], date_title[0]),
                'post_name': date_title[1] + '.html',
                'date': date_title[0],
            }
            post_data['post_path'] = join(post_data['post_dir'],
                                          post_data['post_name'])
            post_data['mtime'] = os.stat(post_data['source_path']).st_mtime
            return post_data

        def _check_status(post_data):
            """检查文件是否修改过
            0 无记录 新文件
            1 有修改 旧文件
            2 无修改 旧文件
            """
            if exists(post_data['post_path']):
                mtime_record = self.data.query_mtime(post_data['source_name'])
                if mtime_record == post_data['mtime']:
                    return 2
                else:
                    return 1
            else:
                return 0

        self.post_t = self.template.load('post.html')
        source_list = os.listdir(PATH['source']) # 获取源文件列表
        for source in source_list:
            post_data = _parser_filename(source) # 解析文件名
            status = _check_status(post_data) # 检查文章
            if status == 0: # 新文章 新建
                self._gen_post(post_data) # 生成文章
                self.data.insert_post(post_data) # 插入记录
                print('[post] "{}" built.'.format(post_data['source_name']))
            elif status == 1: # 有修改 覆盖
                self._gen_post(post_data) # 更新文章
                self.data.update_post(post_data) # 更新记录
                print('[post] "{}" updated.'.format(post_data['source_name']))
            else: # 无修改 不变
                self.data.move_post(post_data) # 移动记录
        for row in self.data.query_old_post(): # 删除旧文章
            if exists(row['post_path']):
                os.remove(row['post_path']) # 删除文章
                print('remove post {}.'.format(row['post_path']))
                if not os.listdir(row['post_dir']):
                    os.removedirs(row['post_dir']) # 若为空目录则删除目录
                    print('remove dir {}.'.format(row['post_dir']))

    def generate_pages(self):
        def _get_post_data():
            index = {}
            category = {}
            tag = {}
            for row in self.data.query_posts():
                post = {
                    'date': row['date'],
                    'title': row['title'],
                    'url': row['url'],
                }
                ilist = index.setdefault(row['year'], [])
                ilist.append(post)
                clist = category.setdefault(row['category'], [])
                clist.append(post)
                for t in row['tag'].split():
                    tlist = tag.setdefault(t, [])
                    tlist.append(post)
            return (index, category, tag)

        (index, category, tag) = _get_post_data()
        self._gen_page('index.html', 'Index', index)
        self._gen_page('category.html', 'Category', category)
        self._gen_page('tag.html', 'Tag', tag)

        def _gen_html(name):
            path = join(PATH['app'], name)
            if not exists(path):
                return
            with open(path) as f:
                html = markdown.markdown(f.read(), ['fenced_code'])
                return html

        self._gen_page('link.html', 'Link', _gen_html('link.md'))
        self._gen_page('about.html', 'About', _gen_html('about.md'))

    def finish(self):
        self.data.close()

    def _mkdir(self, path):
        """检查目录是否存在，不存在就创建相应目录"""
        if not exists(path):
            os.mkdir(path)
            print('mkdir {}.'.format(path))

    def _gen_post(self, post_data):
        """生成页面 添加页面信息"""
        title = '未命名'
        category = '未分类'
        tag = '无标签'
        with open(post_data['source_path']) as source:
            for line in source:
                if line == '-->\n':
                    break
                elif line.startswith('Title:'):
                    _tmp = line.replace('Title: ', '').replace('\n', '')
                    title = _tmp or title
                elif line.startswith('Category:'):
                    _tmp = line.replace('Category: ', '').replace('\n', '')
                    category = _tmp or category
                elif line.startswith('Tag:'):
                    _tmp = line.replace('Tag: ', '').replace('\n', '')
                    tag = _tmp or tag
            self._mkdir(post_data['post_dir'])
            with open(post_data['post_path'], 'w') as post:
                html = markdown.markdown(source.read(), ['fenced_code'])
                b = self.post_t.generate(title=title, html_code=html)
                post.write(b.decode())
        post_data['title'] = title
        post_data['category'] = category
        post_data['tag'] = tag

    def _gen_page(self, name, title, data):
        path = join(PATH['app'], name)
        template = self.template.load(name)
        with open(path, 'w') as page:
            b = template.generate(title=title, archive=data)
            page.write(b.decode())
        print('[page] "{}" built'.format(name))


class Data():
    """读写操作"""
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.isolation_level = None
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(
            '''
            CREATE TABLE IF NOT EXISTS posts (
                source_name TEXT NOT NULL PRIMARY KEY ON CONFLICT REPLACE,
                post_dir TEXT NOT NULL,
                post_path TEXT NOT NULL,
                url TEXT NOT NULL,
                date TEXT NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                tag TEXT NOT NULL,
                mtime REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS temporary (
                source_name TEXT NOT NULL PRIMARY KEY ON CONFLICT REPLACE,
                post_dir TEXT NOT NULL,
                post_path TEXT NOT NULL,
                url TEXT NOT NULL,
                date TEXT NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                tag TEXT NOT NULL,
                mtime REAL NOT NULL
            );
            ''')

    def close(self):
        self._drop_table('posts')
        self._rename_table('temporary', 'posts')
        self.conn.close()

    def _drop_table(self, table_name):
        self.conn.execute('DROP TABLE IF EXISTS {}'.format(table_name))

    def _rename_table(self, old_name, new_name):
        self.conn.execute(
            'ALTER TABLE {} RENAME TO {}'.format(old_name, new_name))

    def insert_post(self, data):
        self.conn.execute(
            '''INSERT INTO temporary
            (source_name, post_dir, post_path,
            url, date, title, category, tag, mtime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (data['source_name'], data['post_dir'], data['post_path'],
             join('.', 'post', data['date'], data['post_name']), data['date'],
             data['title'], data['category'], data['tag'], data['mtime']))

    def update_post(self, data):
        self.insert_post(data)
        self.conn.execute('DELETE FROM posts WHERE source_name=?',
                          (data['source_name'],))

    def move_post(self, data):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT title, category, tag FROM posts WHERE source_name=?',
            (data['source_name'],))
        r = cursor.fetchone()
        data['title'] = r['title']
        data['category'] = r['category']
        data['tag'] = r['tag']
        cursor.execute('DELETE FROM posts WHERE source_name=?',
                       (data['source_name'],))
        cursor.close()
        self.insert_post(data)

    def query_old_post(self):
        for row in self.conn.execute('SELECT post_path, post_dir FROM posts'):
            yield row

    def query_posts(self):
        for row in self.conn.execute(
            '''SELECT
            substr(date, 0, 5) AS year, category, tag, date, title, url
            FROM temporary ORDER BY date(date) DESC'''):
            yield row

    def query_mtime(self, source_name):
        cursor = self.conn.execute('SELECT mtime FROM posts WHERE source_name=?',
                                (source_name,))
        return cursor.fetchone()['mtime']


def main():
    if len(sys.argv) != 2:
        print('usage: pieh command')
        return
    app = Application()
    if sys.argv[1] in ('b', 'build'):
        app.build()
    elif sys.argv[1] in ('c', 'clear'):
        app.clear()
    else:
        print('unknown command')

if __name__ == '__main__':
    main()
