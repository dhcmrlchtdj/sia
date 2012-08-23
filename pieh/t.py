#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import os.path

def main():
    # 获取程序路径
    cur_file_path = os.path.abspath(__file__)
    pieh_path = os.path.dirname(cur_file_path)
    blog_path = os.path.dirname(pieh_path)

    # 检查src目录是否存在
    if 'src' not in os.listdir(blog_path):
        print 'not found src'
        #os.mkdir(os.path.join(app_path, 'src')
        return

    # 进入源文件目录
    src_path = os.path.join(blog_path, 'src')
    # 获取源文件
    src_list = os.listdir(src_path)
    src_files = (f for f in src_list if f.endwith('.md'))

    # TODO
    # 检查是否为新文件
    # 将新文件转换为html代码
    # 插入模板 生成目标文件
    for f in src_files:
        pass


if __name__ == '__main__':
    main()
