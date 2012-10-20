# -*- coding: utf-8 -*-

import os.path

# 源文件目录
# '~/.../source' => '/home/username/.../source'
# 'source' => 'application_path/source'
SOURCE_DIR = '_source'

##################################################
path = {}
# 程序目录
path['pieh'] = os.path.dirname(os.path.abspath(__file__))
path['app'] = os.path.dirname(path['pieh'])

# 源文件目录
if SOURCE_DIR.startswith(('/', '~')):
    path['source'] = os.path.expanduser(SOURCE_DIR)
else:
    path['source'] = os.path.join(path['app'], SOURCE_DIR)

# 文章目录
path['post'] = os.path.join(path['app'], 'post')

# 数据库
path['data'] = os.path.join(path['pieh'], 'posts_data.db')

# 模板
path['template'] = os.path.join(path['theme'], 'theme', 'template')
##################################################
