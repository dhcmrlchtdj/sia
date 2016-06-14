<!--
Title: 计时攻击
Tag: security hash
-->

# 计时攻击

找 bcrypt 的 python 库时，找到了[python-pbkdf2][python-pbkdf2]，
准备使用时突然发现这是 python2 版的。理所当然准备移植到 python3。

看说明文档时，碰到了个问题。`safe_str_cmp`这个函数是干什么用的？
隐约有点印象，在 tornado 的代码有长相类似的函数，
好像在 v2ex 看人提过，还给了 stackoverflow 的链接。
可惜在 v2ex 和 stackoverflow 的相关链接都找不着了。

又搜了半天，终于把问题给理清楚了。

------

上面都是废话……

放上几个链接：

+ [Advanced Security Topics][SecurityTopics]
+ [PyCon 2012 Notes – Advanced Security Topics][notes]
+ [A Lesson In Timing Attacks][TimingAttacks]
+ [Tornado][Tornado]
+ [Use constant-time string comparison algorithm][bcrypt-ruby]

第一个是 pycon2012 上的讲稿，提到了这个问题。
光看讲稿，说的不是很明白，英语好的同学看视频去吧。

第二个和第三个资料讲得挺清楚的。
简单来说，这个安全比较函数是用来比较加密后的字符串的。
直接使用原生的比较函数，也可以正确判断两字符串。问题在于，
不同的输入字符串需要的比较时间是不一样的。所以某些有心人可以靠这个时间差，
来判断密码。（时间越长，说明和密码越接近）。
这也就是为什么这种攻击被称为*计时攻击*（Timing attack）。

面对计时攻击的挑战，安全比较函数应运而生，这个函数特点在于比较时间是常量。
第四个链接是 tornado 中的实现，叫做`_time_independent_equals`。
看了才知道 python3 的标准库里也实现了个
常数时间的字符串比较函数（constant-time string comparison function）。

归结起来，也就是说：**对加密字符串的比较，应该使用比较时间为常数的比较函数，
避免受到计时攻击。**

最后的一个链接是来自 bcrypt-ruby 的讨论。
我们有没有必要使用专门的比较函数来规避计时攻击？
结论是对于某些加密算法（比如 bcrypt）来说，
<strike>不需要（具体自己看链接吧）。</strike>
why risk it if I can easily avoid it。
还是乖乖用`hmac.compare_digest`来比较吧。（2013/01/17）

------

这应该是对博客动刀前的最后一篇了吧……

移植 python-pbkdf2 去。



[python-pbkdf2]: https://github.com/mitsuhiko/python-pbkdf2
[TimingAttacks]: http://codahale.com/a-lesson-in-timing-attacks/
[SecurityTopics]: https://github.com/PaulMcMillan/advanced_security_pycon_2012
[notes]: http://brianrue.wordpress.com/2012/03/09/pycon-2012-notes-advanced-security-topics/
[Tornado]: https://github.com/facebook/tornado/blob/master/tornado/web.py#L2074
[bcrypt-ruby]: https://github.com/codahale/bcrypt-ruby/pull/43
