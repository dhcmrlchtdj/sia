<!--
Title: python 中异步处理
Tag: python asynchronous
-->

# python 中异步处理

为了提高 yuedu.py 的下载速度，跑去鼓捣异步请求。
从写上一篇文章到现在，课余时间都花在这上面了。

先说下为什么又自己造轮子了……

+ 考虑过学习下 gevent，结果发现不支持 python3。
+ gevent 是基于 greenlet 的，而且 greenlet 支持 python3。
    可是不太明白怎么进行异步处理，而且发现了更好的东西。
+ tornado 可以进行异步请求。但是 pycurl 不支持 python3，所以没法使用 curl 了，
    其实还有个非 pycurl 的默认异步请求工具，在发现了下面这东西后直接放弃了。
+ python 标准库里的 asyncore，虽然是自己操作请求，但写起来超级简单，
    所以有大约三分一时间，都是花在了这上面。可惜只能用 select 或者 poll，
    所以我最后也放弃了。

放弃 asyncore 之后，我就直接自己动手写了。就当是学习使用 epoll 吧。

帮助最大的是这篇文章[How To Use Linux epoll with Python][use_epoll]，
网上有中译，直接看代码也很好理解。
文章里面还有个链接[HTTP Made Really Easy][http]，
我自以为翻过几页 _HTTP: The Definitive Guide_，对请求长什么样还算清楚，
就没仔细看。结果吃了不少亏，要是当初完整看一遍，
就不会被`Transfer-Encoding: chunked`搞得焦头烂额了。

------

题目虽然叫什么异步处理，实际上没什么可写的。
关于套接字还有并行的基础知识，可以看 _CSAPP_ 后三章，
再去翻一翻 _UNIX 网络编程_ 就可以了。
epoll 基础看上面链接的文章，配合官方文档就可以开始写程序了。

下面写一点自己的心得。

+ collections.namedtuple 挺好用的。
+ socket.setblocking(0) 进行非阻塞请求。
+ 服务端设置`backlog`时，可以用`socket.SOMAXCONN`。
+ 可以用 sendall 直接把所有请求发出去，我还是自己一点点 send 的。
+ recv 接收的字节数应该是 2 的幂，文档推荐可以每次接受 8192 个字节，
    其实大部分时候都没这么多。
+ 请求的请求头有几个值必须设置，否则请求经常被重定向什么的，参考上面那篇链接。
+ 请求写 HTTP/1.1 的话，要处理`Transfer-Encoding: chunked`等情况，
    我自己写的程序其实还没完全搞定，只算是勉强可用了。
+ 返回的`Set-Cookie`可能会有多个，不知道还有没有类似的情况。
    准备自己写个 Headers 类处理，又碰到兼容 dict 的问题，要实现好几个接口。
+ 设置个重定向次数上限，避免出现死循环，wiki 上推荐是 5 次。
+ 用个 try 语句来关闭 epoll 和打开的套接字。
+ 可以在请求时才生成 epoll 和套接字，也就是惰性求值，避免套接字没有正常关闭。
    这样做也有个缺点，为了能够在回调函数中添加任务，
    就要在每次循环时检查是否有新任务加入。
    想避免检查的开销，不用惰性求值，而是直接在每次添加任务时创建套接字，
    又可能出现套接字或 epoll 最后没正常关闭的情况。
+ 在读取写入都完成后，要关闭套接字（shutdown），否则 epoll 不会停止。
+ ssl 的非阻塞请求要设置`do_handshake_on_connect=False`。
+ 读取 ssl 时，要检查读写错误，文档有说明。可以自己重写 recv 方法，
    也可以在循环里面处理。我觉得重写个方法更符合逻辑。

------

先写到这里，刚刚发现了个[好东西][tulip]。准备好好研究一下。

另外，虽然不是异步，标准库里的`concurrent.futures`很容易上手。
之前使用过，不过效率的提升不大（不明显？）。

[use_epoll]: http://scotdoyle.com/python-epoll-howto.html
[http]: http://www.jmarshall.com/easy/http/
[tulip]: http://code.google.com/p/tulip/
