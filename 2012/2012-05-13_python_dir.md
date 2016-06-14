<!--
Title: python 下删除文件和目录
Tag: tips python
-->

python操作文件
==============

主要是两个东西`os`和`os.path`。

参考资料

-   <http://docs.python.org/library/os.html#os-file-dir>
-   <http://docs.python.org/library/os.path.html>

~~~~ {.python}

# pwd
os.getcwd()
os.getcwdu() # unicode

# cd
os.chdir(path)

# ls
os.listdir(path)

# mkdir
os.mkdir(path)
os.makedirs(path) # 递归地创建目录，更实用些

# rm
os.remove(path) # 只能删除文件
os.rmdir(path) # 只能删除空目录
shutil.rmtree(path) # 删除目录

# rename
os.rename(src, dst) # 重命名文件

# path
os.path.abspath(file)
os.path.basename(path)
os.path.dirname(path)
os.path.join(path, path, ...)
~~~~
