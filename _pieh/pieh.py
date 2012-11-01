#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from os.path import exists, join, dirname, abspath, expanduser
import shutil
import sqlite3

from tornado.template import Loader
from markdown import markdown


SOURCE_DIR = "_source"
PATH = {}
# 程序目录
PATH["pieh"] = dirname(abspath(__file__))
PATH["app"] = dirname(PATH["pieh"])
# 源文件目录
if SOURCE_DIR.startswith(("/", "~")):
    PATH["source"] = expanduser(SOURCE_DIR)
else:
    PATH["source"] = join(PATH["app"], SOURCE_DIR)
# 文章目录
PATH["post"] = join(PATH["app"], "post")
# 数据库
PATH["database"] = join(PATH["pieh"], "posts.db")
# 模板目录
PATH["template"] = join(PATH["app"], "theme", "template")


class Application():
    def build(self):
        # 检查目录是否存在
        self._mkdir(PATH["post"])
        # 连接数据库
        self.data = Database(PATH["database"])
        # 读取模板
        self.template = Loader(PATH["template"], autoescape=None)
        # 生成页面
        self.generate_posts()
        self.generate_pages()
        # 关闭数据库
        self.data.close()

    def clear(self):
        self._rm(PATH["post"], shutil.rmtree)
        self._rm(PATH["database"])
        self._rm(join(PATH["app"], "index.html"))
        self._rm(join(PATH["app"], "tag.html"))
        self._rm(join(PATH["app"], "link.html"))
        self._rm(join(PATH["app"], "about.html"))

    def _mkdir(self, path):
        if not exists(path):
            os.mkdir(path)
            print("mkdir {}.".format(path))

    def _rm(self, path, command=os.remove):
        if exists(path):
            command(path)
            print("delete {}.".format(path))

    def generate_pages(self):
        index = {}
        tag = {}
        for row in self.data.query_posts():
            post = {
                'date': row['date'],
                'title': row['title'],
                'url': row['url'],
            }
            ilist = index.setdefault(row['year'], [])
            ilist.append(post)
            for t in row['tag'].split():
                tlist = tag.setdefault(t, [])
                tlist.append(post)
        self._gen_page('index.html', 'Index', index)
        self._gen_page('tag.html', 'Tag', tag)

        def gen_html(name):
            path = join(PATH['app'], name)
            if not exists(path): return
            with open(path) as f:
                return markdown(f.read(), ['fenced_code', 'codehilite'])
        self._gen_page('link.html', 'Link', gen_html('link.md'))
        self._gen_page('about.html', 'About', gen_html('about.md'))

    def generate_posts(self):
        def parse_filename(source_name):
            """解析源文件文件名"""
            # date_title.md -> (date, title)
            name = source_name.rsplit(".", 1)[0]  # date_title
            date_title = name.split("_", 1)  # [date, title]
            post_data = {
                "source_name": source_name,
                "source_path": join(PATH["source"], source_name),
                "post_dir": join(PATH["post"], date_title[0]),
                "post_name": date_title[1] + ".html",
                "date": date_title[0],
            }
            post_data["post_path"] = join(
                post_data["post_dir"], post_data["post_name"])
            post_data["mtime"] = os.stat(post_data["source_path"]).st_mtime
            return post_data

        def check_status(post_data):
            """检查文件是否修改过"""
            if exists(post_data["post_path"]):
                mtime_record = self.data.query_mtime(post_data["source_name"])
                if mtime_record == post_data["mtime"]: return 2  # 页面无修改
                else: return 1  # 页面有修改
            else:
                return 0  # 新页面

        self.post_t = self.template.load("post.html")
        source_list = os.listdir(PATH["source"])  # 获取源文件列表
        for source in source_list:
            post_data = parse_filename(source)  # 解析文件名
            status = check_status(post_data)  # 检查文章
            if status == 0:  # 新文章 新建
                self._gen_post(post_data)  # 生成文章
                self.data.insert_post(post_data)  # 插入记录
                print("[post] '{}' built.".format(post_data["post_name"]))
            elif status == 1:  # 有修改 覆盖
                self._gen_post(post_data)  # 更新文章
                self.data.update_post(post_data)  # 更新记录
                print("[post] '{}' updated.".format(post_data["post_name"]))
            else:  # 无修改 不变
                self.data.move_post(post_data)  # 移动记录
        for row in self.data.query_old_post():  # 删除旧文章
            self._rm(row["post_path"])  # 删除文章
            if not os.listdir(row["post_dir"]):
                os.removedirs(row["post_dir"])  # 若为空目录则删除目录
                print("remove dir '{}'.".format(row["post_dir"]))

    def _gen_page(self, name, title, data):
        path = join(PATH["app"], name)
        template = self.template.load(name)
        with open(path, "w") as page:
            b = template.generate(title=title, archive=data)
            page.write(b.decode())
        print("[page] '{}' built".format(name))

    def _gen_post(self, post_data):
        """生成页面 添加页面信息"""
        title = ""
        tag = ""
        with open(post_data["source_path"]) as source:
            for line in source:
                if line == "-->\n":
                    break
                elif line.startswith("Title:"):
                    title = line.replace("Title:", "").strip()
                elif line.startswith("Tag:"):
                    tag = line.replace("Tag:", "").strip()
            self._mkdir(post_data["post_dir"])
            with open(post_data["post_path"], "w") as post:
                html = markdown(source.read(), ["fenced_code", "codehilite"])
                b = self.post_t.generate(title=title, html_code=html)
                post.write(b.decode())
        post_data["title"] = title
        post_data["tag"] = tag

class Database():
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.isolation_level = None
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS posts (
                source_name TEXT NOT NULL PRIMARY KEY ON CONFLICT REPLACE,
                post_dir TEXT NOT NULL,
                post_path TEXT NOT NULL,
                url TEXT NOT NULL,
                date TEXT NOT NULL,
                title TEXT NOT NULL,
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
                tag TEXT NOT NULL,
                mtime REAL NOT NULL
            );
            """)

    def close(self):
        self.conn.execute("DROP TABLE IF EXISTS posts")
        self.conn.execute("ALTER TABLE temporary RENAME TO posts")
        self.conn.close()

    def insert_post(self, data):
        self.conn.execute(
            """INSERT INTO temporary
            (source_name, post_dir, post_path, url, date, title, tag, mtime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (data["source_name"], data["post_dir"], data["post_path"],
             join(".", "post", data["date"], data["post_name"]),
             data["date"], data["title"], data["tag"], data["mtime"]))

    def remove_post(self, data):
        self.conn.execute("DELETE FROM posts WHERE source_name=?",
                          (data["source_name"],))

    def update_post(self, data):
        self.insert_post(data)
        self.remove_post(data)

    def move_post(self, data):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT title, tag FROM posts WHERE source_name=?",
            (data["source_name"],))
        r = cursor.fetchone()
        data.update(r)
        cursor.close()
        self.remove_post(data)
        self.insert_post(data)

    def query_mtime(self, source_name):
        cursor = self.conn.execute(
            "SELECT mtime FROM posts WHERE source_name=?", (source_name,))
        return cursor.fetchone()["mtime"]

    def query_old_post(self):
        for row in self.conn.execute("SELECT post_path, post_dir FROM posts"):
            yield row

    def query_posts(self):
        for row in self.conn.execute(
            """SELECT substr(date, 0, 5) AS year, tag, date, title, url
            FROM temporary ORDER BY date(date) DESC"""):
            yield row


def main():
    if len(sys.argv) != 2:
        print("usage: pieh COMMAND")
        return

    app = Application()
    char = sys.argv[1]
    if char == "b":
        app.build()
    elif char == "c":
        app.clear()
    else:
        print("unknown command")

if __name__ == "__main__":
    main()
