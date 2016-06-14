<!--
Title: 开始造轮子吧
Tag: python tornado template
-->

# 开始造轮子吧

想着重复造个轮子，自己写一个模板系统，之前以为不是很难，
现在发现完整实现一个模板还是相当复杂的。

断断续续看了两天，才把`tornado.template`的整体结构都搞明白。剩下一些细节，
等之后再研究了，先把看懂的记下来。基本是照着我自己看代码的顺序，再整理了一下。

最开始的想法就是写一个`Template`类，读取模板，然后替换，最后输出。
开始连是传入文件路径还是字符串都没考虑好，乱七八糟的东西不提也罢，
直接开始研究 tornado。


## 使用 tornado.template

```python
# tornado 中 Template 类的使用
t = template.Template("<html>{{ myvalue }}</html>")
print t.generate(myvalue="XXX")

# tornado 中 Loader 类的使用
loader = template.Loader("/home/btaylor")
print loader.load("test.html").generate(myvalue="XXX")
```

要在非 tornado 的应用中使用 tornado 的模板，上面就是基本用法了。
`Template`类接受字符串，然后替换输出。而`Loader`类接受的是路径，
读取路径下的模板文件，替换输出。很明显，调用`load`方法应该是生成了一个
`Template`的实例。

要注意的一点，在自己的程序中使用 tornado 的模板时，
如果直接用字符串实例化`Template`，是不支持`extends`之类的语句的。
多个模板文件的情况下，应该使用`Loader`。

使用 tornado 写 web 应用时，不用自己调用`Loader`，
程序会自动加载`settings['template_path']`，
直接使用`tornado.web.RequestHandler`的`render`方法就可以了。


## tornado.template 的实现

接下来研究具体实现。开始没看仔细，说明文档在第一行就说了，
tornado 的模板实现是把模板文件编译成 python 代码，再执行这个代码，
基本上把代码看完了，才知道是这样。
（A simple template system that compiles templates to Python code.）


### Loader

首先是`Loader`的实现。代码还算简单。主要就做了一件事情，读取路径。
为了提高解析模板的效率，`Loader`的实例有个`template`属性，以模板名为关键字，
保存着编译好的模板实例。每次读取模板，都是在这个`template`中读取，
如果没有编译好的模板，`Loader`实例会生成相应的模板，保存在该属性中。
由于每次读取`template`时，可能会往里面添加新的模板，
所以 tornado 在每次读取时都会加锁（`threading.RLock()`），避免发生重复编译。

另外值得一提的是`Loader`不检查文件路径是否存在，
文件不存在的错误在`open`试图读取文件是抛出的。
还有`open`是将模板文件当作二进制文件读取的，我自己试了下，当作二进制文件读取，
返回的是`bytes`类型，而当作文本文件读取，返回的是`str`类型。
tornado 的模板实现里，进行了多次的字符串类型转换，这个等之后再具体研究。


### Tempalte

在生成实例化`Tempalte`的时候，对模板的编译就完成了，
也就是说已经生成了 python 代码，剩下的只是执行和输出。
大部分工作在`__init__`中就完成了，下面挑要点来讲。

`__init__`中有个`reader`属性，这是`_TempalteReader`的实例，用于读取模板文件。

之后执行了`_parse(reader, self)`，`_parse`用于解析模板文件，将模板内容分块，
然后用这个执行结果实例化一个`_File`类。

接下来调用`_generate_python`就是将这些块转换成相应的 python 代码，
把代码保存在了`self.code`属性中。

接下来就是编译生成的 python 代码，并保存在`self.compiled`属性里。

实例化的工作到此结束。

在输出也就是调用`generate`方法时，tornado 将用户变量保存在一个命名空间里，
在命名空间中执行刚才编译好的 python 代码，执行的结果是生成一个`_execute`函数，
执行该方法，就输出了模板。

------

知道了大致流程，下面一点点具体研究。


#### \_TempalteReader

`_TempalteReader`类用于实现读取文件内容，`find`方法来查找字符位置，
`consume`方法返回读取的字符串，`__getitem__`实现了取某个位置的字符，
即`reader[key]`。


#### \_parse

`_parse`方法用于解析文件内容。将结果保存在一个`_ChunkList`实例中，
当作列表理解就可以了。

就流程来说，先判断文件是否结束，结束就返回。然后根据模板的语法，先寻找`{`，
将`{`之前的文件内容保存为文本块（`_Text`）。
然后判断`{`的类型，转义（`{{!`）会保存为文本块，注释（`{#`）则直接丢弃，
直接输出的变量（`{{`）保存为语句块（`_Expression`）。

接下来是对其他语法的处理，对于`apply`、`block`、`try`、`if`、`for`、`while`
这几个要跟`end`成对使用的语句，采用了递归处理的办法。
用剩下的内容调用`_parse`，遇到`end`时返回解析结果。

其他语句也差不多，就是顺序执行，没仔细看，就先分析到这里。


#### \_File

第一个参数是`Tempalte`实例，第二个参数是`_ChunkList`实例。
编译出来的 python 代码只有一个`_execute`函数，就是`generate`方法生成的。
这个方法遍历整个`_ChunkList`，调用各个块的`generate`方法，
生成完整的`_execute`。


#### \_generate_python 和 \_get_ancestors

从名字就知道`_generate_python`用于生成 python 代码。
`_generate_python`先调用`_get_ancestors`，
在返回的`_File`实例中查找`_ExtendsBlock`，也就是查找父模板，这是一个递归过程，
直到找到最初的模板，返回模板列表，列表是子模板到父模板的顺序。
之后将模板列表逆序，递归查找其中的`_NamedBlock`块（即`block`语句），
将找到的块保存在变量中。

简单解释一下，这个过程其实是完成模板的继承。
首先找到父模板，然后查找父模板的`block`块，保存在变量`named_block`中。
再查找子模板的`block`块，同样保存在`named_block`中，并且会覆盖父模板的同名块。
这就实现了父模板中`block`有默认值，而子模板的`block`会覆盖相应的值。

之后`_generate_python`实例化一个`_CodeWriter`，父模板调用`generate`方法，
将各个块转换成 python 代码。

注意下，父模板的`template`属性和`generate`方法都是从`_File`继承来的。


#### \_CodeWriter

python 使用缩进，所以`_CodeWriter`的一项任务就是保证输出的代码中缩进正确。
此外还实现了一个栈，用于`_IncludeBlock`块，还没搞明白。


### rest

剩下的就是一个语法错误类和各个块的实现，还没看完。所以就到此为止了。


## 拓展阅读

这是中午偶然找到的文章，
[Code Generation in Python — Dismantling Jinja](http://pocoo.org/~mitsuhiko/codegenjinja.pdf)，
来自 pocoo 的 Armin Ronacher。

其实还有好几个地方要再仔细看下，特别是编码的问题。
之后应该还会看一下 js 的模板怎么实现。所以应该还会写点相关的文章。

关于重复造轮子的问题，不管怎么样，先看懂别人怎么造轮子再说吧。
