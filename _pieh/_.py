#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import filecmp
import csv
import tempfile

import markdown2
import config


# 生成page
# 将markdown生成的html插入template

class Application():
    def main(self):
        self.initial()
        self.generate_posts()
        self.remove_old_posts()
        self.generate_pages()
        self.finish()

    def initial(self):
        """创建缺失的文件夹 读取数据"""
        cp = config.path
        if not os.path.exists(cp['source']):
            os.mkdir(cp['source'])
        if not os.path.exists(cp['post']):
            os.mkdir(cp['post'])

        # 读入csv文件
        self.csv = Content()

    def finish(self):
        """保存记录 并 关闭打开的文件"""
        self.csv.save()
        self.csv.close()

    def generate_pages(self):
        """删除旧文件 生成新文件"""
        # 生成index about category tag link
        pass

    def generate_posts(self):
        source_list = os.listdir(config.path['source'])
        for source in source_list:
            status = self._check_status(source)
            if status == 1: # 已存在
                self.csv.add(source)
            elif status == 0: # 修改
                self._update_post(source)
            else: # 新文件
                self._insert_post(source)

    def remove_old_posts(self):
        for post in self.csv.csv_remaining:
            self._delete_post(post)

    def _insert_post(self, filename):
        """添加新文章"""
        date, title = Filename.parser_filename(filename)
        directory = os.path.join(config.path['post'], date)
        if not os.exists(directory):
            os.mkdir(directory)
        source_file = Filename.source_file_path(filename)
        post_file = Filename.post_file_path(filename, date, title)
        with open(post_file, 'w') as post:
            post.write(markdown2.markdown_path(source_file))
        # 添加记录
        self.csv.add(filename, date, title)

    def _update_post(self, filename):
        """修改文章（覆盖）"""
        source_file = Filename.source_file_path(filename)
        post_file = Filename.post_file_path(filename)
        with open(post_file, 'w') as post:
            post.write(markdown2.markdown_path(source_file))
        # 添加记录
        self.csv.add(filename)

    def _delete_post(self, post):
        """删除旧文章
        post == 'date/title'
        """
        post_file = os.path.join(config.path['post'], post)
        os.remove(post_file)
        directory = os.path.dirname(post_file)
        if not os.listdir(directory):
            os.removedirs(directory)

    def _check_status(self, filename):
        """input date_title.md
        1 => equal
        0 => not equal
        -1 => post not found
        """
        source_file = Filename.source_file_path(filename)
        post_file = Filename.post_file_path(filename)
        if os.path.exists(post_file):
            if filecmp.cmp(source_file, post_file):
                return 1
            else:
                return 0
        else:
            return -1


class Filename():
    @classmethod
    def parser_filename(cls, filename):
        """date_title.md => (date, title)"""
        name = filename.rsplit('.', 1)[0]
        return tuple(name.split('_', 1))

    @classmethod
    def source_file_path(cls, filename):
        """date_title.md => source_path/date_title.md"""
        return os.path.join(config.path['source'], filename)

    @classmethod
    def post_file_path(cls, filename, date=None, title=None):
        """date_title.md => post_path/date/title"""
        if not (date and title):
            date, title = cls.parser_filename(filename)
        return os.path.join(config.path['post'], date, title)


class Content():
    def __init__(self):
        kwargs = {'mode': 'w+', 'newline': '', 'encodeing': 'utf-8'}
        self.tempfile = tempfile.TemporaryFile(**kwargs)
        self.csvfile = open(config.path['contents'], **kwargs)
        self.old_record = [value for row in csv.reader(self.csvfile)
                           for value in row]
        self.new_record = csv.writer(self.tempfile)

    @property
    def csv_remaining(self):
        return self.old_record

    def add(self, source_name, date=None, title=None):
        if not (date and title):
            date, title = Filename.parser_filename(source_name)
        post = os.path.join(date, title)
        self.new_record.writerow(post)
        if post in self.old_record:
            self.old_record.remove(post)

    def save(self):
        self.csvfile.seek(0)
        self.tempfile.seek(0)
        self.csvfile.write(self.tempfile.read())

    def close(self):
        self.csvfile.close()
        self.tempfile.close()


if __name__ == '__main__':
    Application().main()
