# -*- coding: utf-8 -*-

import os.path

# 源文件存放文件夹
# ~/source => /home/user/source
# source => application_path/source
SOURCE_DIR = '_source'

# 主题
THEME = 'default'

##################################################
path = {}
path['pieh'] = os.path.dirname(os.path.abspath(__file__))
path['application'] = os.path.dirname(path['pieh'])
if SOURCE_DIR.startswith(('/', '~')):
    path['source'] = os.path.expanduser(SOURCE_DIR)
else:
    path['source'] = os.path.join(path['application'], SOURCE_DIR)
path['post'] = os.path.join(path['application'], 'post')
path['data'] = os.path.join(path['pieh'], 'posts_data.db')
path['theme'] = os.path.join(path['application'], THEME)
path['template'] = os.path.join(path['theme'], 'template')
path['static'] = os.path.join(path['theme'], 'static')
##################################################

##################################################
version = {}
version['version'] = '0.1.1'
version['major'] = 0
version['minor'] = 1
version['micro'] = 1
##################################################

