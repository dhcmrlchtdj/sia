<!--
Title: python 单元测试笔记（坑）
Tag: python unittest
-->

python unittest
===============

程序员应该学会写测试代码，进行自动化测试。
网上可以找到一堆单元测试啊，测试驱动开发之类的东西，
可惜我一直不知道到底测试什么玩意儿。

直到我想写个markdown.py。

我脑袋里自然而然地冒出了写测试的想法。
先写测试代码，然后实现某个功能，下个测试，下个功能……
这个就是所谓的突然开窍了么。

* * * * *

这篇文章的主要内容是unittest模块的学习笔记。
按计划是我自己写了测试代码，这个文章就更新相应的内容。

官方文档在

<http://docs.python.org/library/unittest.html>

* * * * *

下面进入正题，先开始项目再说。

整个项目就2个文件，`markdown.py`和`markdown_test.py`。

~~~~ {.python}
# markdown_test.py

import unittest
from markdown import Markdown

# 测试的类要继承unittest.TestCase
class MarkdownTest(unittest.TestCase):
    # 测试 是以'test_'开头的方法
    def test_h1(self):
        text = '# h1'
        html = Markdown.convert(text)
        # 这个很好理解吧，比较结果是否相等
        self.assertEqual(html, '<h1>h1</h1>\n')

if __name__ == '__main__':
    # 执行上面的测试
    unittest.main()
~~~~

执行`python markdown_test.py`就会输出测试结果。

顺便把`markdown.py`也贴出来看一下。

~~~~ {.python}
# markdown.py

class Markdown(object):
    @staticmethod
    def convert(text):
        html = '<h1>h1</h1>\n'
        return html
~~~~

细节就不要在意了。总之，整个项目开始起步了。
`assertEqual()`应该是最常用的测试了吧。

然后可以开始下个测试了（毫无疑问，失败了）。

~~~~ {.python}
def test_h2(self):
    text = '## h2'
    html = Markdown.convert(text)
    self.assertEqual(html, '<h2>h2</h2>\n')
~~~~

最后说两句， 刚开始，我也想按照markdown的语法把测试先写好，具体实现慢慢来。
可是想一想，在完成所有功能前，每次测试都是失败的，也太打击人了。
还是测试写一点，功能实现一点更能带来成就感吧。

这个想法倒也不是我自己拍脑袋想出来的，
以前翻过一本叫《测试驱动开发的艺术》，这种直接返回`'<h1>h1</h1>\n'`
的做法就是这书上看来的。
看网上的豆瓣上评价还可以，我自己随便翻了点，可惜看不下去。
但这种作弊式的做法我倒是记下来了。

说到作弊，突然想到了插值逼近，基函数这种东西在我看来，
也是典型的作弊啊，居然还能把基函数算出来，这个可以说是数学之美么？
