<!--
Title: python 中展开嵌套列表
Tag: tips python
-->

如何把一个 `[ [a], [b], [c] ]` 转化为 `[a, b, c]`。

```python
l = [[1,2,3], [4,5,6], [7], [8,9]]

# method 0
[item for sublist in list for item in sublist]

# method 1
sum(l, [])

# method 2.11
reduce(lambda x,y: x+y, l)
# method 2.12
reduce(lambda x,y: x.extend(y) or x, l)

# method 2.2
import operator
reduce(operator.add, l)

# method 3.1
import itertools
list(itertools.chain(*l))

# method 3.2
import itertools
list(itertools.chain.from_iterable(l))
```
