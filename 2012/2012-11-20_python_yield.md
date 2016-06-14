<!--
Title: python yield 研究
Tag: python yield
-->

# python yield 研究

自己一直对 yield 语句存在误解，
网上似乎也没有把 yield 讲解得非常深入的文章。
果然努力研究文档才是正道。

下面算是我自己看文档的理解吧。

```python
# example 1.1

def func():
    return 1

def gen():
    yield 1

print(type( func )) # <class 'function'>
print(type( gen )) # <class 'function'>

print(type( func() )) # <class 'int'>
print(type( gen() )) # <class 'generator'>
```

从例 1.1 可以看到，`func`和`gen`都是函数，
但前者返回数字 1，后者返回的是个生成器（generator）。

```python
# example 1.2

print(type( (i for i in range(10)) )) # <class 'generator'>
```

其实平常接触更多的是像例 1.2 这样的生成器，
由一个生成器表达式（generator expression）生成。

但两者是不同的东西，看下面这个例子。

```python
# example 1.3

gen1 = (i for i in range(10))

def gen():
    for i in range(10):
        yield i
gen2 = gen()

print(gen1) # <generator object <genexpr> at 0x00000000>
print(gen2) # <generator object gen at 0x00000000>
```

例 1.3 中，两个生成器的作用完全相同，但还是有些区别，不知道怎么描述？
一个是生成器，一个是生成器表达式，但都属于生成器类型……感觉好别扭。

不管怎样，要理解 yield 语句，关键就是了解 python 的生成器。
用官网的说法[1][py_gen_1]、[2][py_gen_2]，
生成器就是一个返回迭代器（iterator）的函数。
和普通函数唯一的区别就是这个函数包含 yield 语句。

使用生成器，有两种方法。

```python
# example 2.1

def gen():
    yield 1

# 2.1.1
g1 = gen()
for i in g1:
    print(i)

# 2.1.2
g2 = gen()
print( next(g2) )
```

像例 2.1 里的代码一样，
可以用`for`语句遍历生成器（注意是遍历生成器`gen()`，而不是函数`gen`），
也可以手动使用`next`函数获取生成器的值。
两者都是使用生成器的`__next__`方法来获取生成器的值的（？）。

下面再深入一点点。

```python
# example 3.1

def gen():
    yield 1
    yield 2

generator = gen()

for value in generator:
    print(value)
```

虽然例 3.1 的生成器实在傻的可以，但是用来解释生成器工作还是可以的。

for 语句在碰到生成器 generator 的时候，
调用`generator.__next__()`获取生成器的返回值
（不知道底层是不是这样，总之这么理解吧）。
`__next__()`每次调用，可以理解为执行了一次`generator()`
执行到 yield 的时候，生成器返回了 i 的值（本例中也就是 1）并停止。
这就像普通函数碰到 return 时一样，剩下的代码都被忽略了。
不同的地方在于，python 会记录这个停止的位置。
当再次执行`generator()`的时候，python 从这个停止位置开始执行而不是开头，
也就是说这次返回了 2。再执行`generator()`，已经没有 yield 语句了，
就抛出了 StopIteration 。这和其他迭代器是类似的。

要点就一个，python 会记录停止的位置，并且下次从这个位置继续执行。
可以去回顾下例 1.3，就是循环，暂停，再循环的过程。

知道这点，然后可以再深入一点。下面可以算是生成器的高级用法了吧。

```python
# example 4.1

""" output "WHT!" """

def gen():
    while True:
        hello_world = yield
        print(hello_world)

g = gen()

next(g)

g.send("WTF!")
g.send("what the fuck!!")
```

第一次看到这种代码肯定不知道发生了什么……至少我不知道。
不过我之前就提示了一点，要理解 yield，就必须了解 python 的生成器。

生成器有[这么几个方法][gen_method]：

+ `__next__` 不用说了，每次 for 还有 next 都是调用这个方法。
+ `send(value)` 用 value 对 yield 语句赋值，再执行接下来的代码直到下个 yield。
+ `throw(type[, value[, traceback]])` 抛出错误，类似于 raise 吧。
+ `close()` 告诉生成器，你已经死了。再调用会抛出 StopIteration。

其实还有这么几个属性没列出来：

+ `gi_code` 不知道啥用，生成器的代码？
+ `gi_frame` 不知道啥用，环境变量？
+ `gi_running` 总算知道了，查看生成器是否再运行。

知道了上面这些，就可以理解例 4.1 的代码了。
其实就是用`send`方法对`hello_world`进行了赋值……

python 的代码还是很清晰的，但这里还是解释下那个 next 调用和 while。
在调用`send`方法前，必须先调用一次`__next__`，让生成器执行到 yield 语句处，
才能进行赋值。外面加上 while 循环是为了避免出现`send`之后，
生成器没有 yield 语句了，抛出 StopIteration 的情况。

其实我都没碰到过这么使用生成器的场景，似乎写协程时用的上，这里就先不提了。

另外，每次调用 next 还是挺麻烦的事情，这个工作可以交给修饰器。
代码见例 4.2。

```python
# example 4.2

from functools import wraps

def coroutine(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        next(f)
        return f
    return wrapper
```

------

目前就了解到这么多，就先写到这里了。研究过协程，再看看能否继续扩展吧。

总结一下：

1. 使用 yield 语句的函数返回的是生成器。
2. 用`__next__`获取生成器的值。
3. 每次碰到 yield 语句会返回并记录当前位置。
4. 可以对 yield 语句进行赋值。

另外，除了官方文档，
还可以看下[这篇][coroutine]讲协程的文档。


[py_gen_1]: http://docs.python.org/3/glossary.html#term-generator
[py_gen_2]: http://docs.python.org/3/library/stdtypes.html#generator-types
[gen_method]: http://docs.python.org/3/reference/expressions.html#generator-iterator-methods
[coroutine]: http://www.dabeaz.com/coroutines/index.html
