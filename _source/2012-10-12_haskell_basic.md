<!--
Title: haskell学习笔记（坑）
Category: programming
Tag: haskell
-->

~~~
## 类型

Int Integer Float Double Bool Char
Num 包括Int Integer Float Double
Integral 包括 Int Integer
Floating 包括 Float Double

Num
: 1

Fractional
: 1.0

Bool
: True

Char
: 'c'

[Char]
: "char"

### 查看类型
:t 'a'
:t (==)

### 改变类型

改变为字符串
show 3 == "3" /= '3'

字符串变为其他类型
read "3" :: Int
read "3" :: Float
read "3" + 2 == 5

--------------

## 操作符

	+ - * /
	&& || not
	== /=

---------------------

## 常见函数

	compare 'a' 'b' 返回LT EQ GT
	succ pred 增减1
	max 9 10
	min 9 10
	div 10 3 整除 等价于 10`div`3
	mod 10 3 取余
	odd 1 为奇数
	even 1 为偶数

-----------------

## 编写函数

函数名 参数 = 函数体
doubleIt x = x+x

------------------

## 在命令行载入文件

:l filename

---------------------

## 条件语句

if <condition> then <command> else <command>

---------------------

## 赋值

在hs文件中 x=1
在命令行里 let x=1

---------------------

## 列表

列表只能放相同类型的值

字符串即为字符列表

num = [1, 2, 3, 4]
char = ['h', 'e', 'l', 'l', 'o'] == "hello"

### 列表操作符

++ 连接前后两个列表
[1,2,3] ++ [4,5]
['h','e','l','l','o'] ++ "world"

: 在表头添加元素
1:[2,3]
'a':" cat"

!! 按位置取元素
"hello"!!0
[1,2]!!1

### 列表操作函数

列表是否为空
null "hello

元素是否在列表中
elem 'h' "hello" == 'h' `elem` "hello"

获取列表长度
length "hello" == 5

反转列表
reverse "hello" == "olleh"

截取列表开头几个元素
接受两个参数 长度和列表
当长度为0 返回空列表
长度超过列表 返回整个列表
take 5 "hello world" == "hello"

去掉列表开头几个元素
接受两个参数 长度和列表
当长度为0 返回整个列表
长度超过列表 返回空列表
drop 6 "hello world" == "world"

head "hello" =='h' == "hello"!!0
tail "hello" == "ello" == drop 1 "hello"
init "hello" == "hell" == take ((length "hello" -1) "hello"
last "hello" == "o" == "hello"!!(length "hello" -1)

获取最大/小值
maximum "hello"
minimum "hello"

取和/乘积 只用于数值
sum [1,2]
product [1,2]

### 生成列表
等差
[1..] 无限
[1..20]
['a'..'z']
[1,3..20] == [1,3,5,7,9,11,13,15,17,19]
[20..1] == []
[10,8..1] == [10,8,6,4,2]

重复列表
cycle "hello" --无限循环
重复元素
repeat 5 --无限循环
replicate 3 5 == [5,5,5] --循环3次

列表推导
[ express | condition1, condition2 ]

[x*2 | x <- [1..10]]
[if x<10 then "hello" else "world" | x<-[1..20], x>5, x<14]
[x*y | x<-[1,2], y<-[3,4,5]] == [3,4,5, 6,8,10]
[ [x|x<-xs, even x] | xs<-xxs] --let xxs=[[1,2,3],[4,5,6],[7,8,9]]

----------------------

## 元组

可以有不同类型的元素 长度固定
(1, "hello", 'a')

### 二元组

#### 操作函数
取第一个元素
fst (1,2) == 1

取第二个元素
snd (1,2) == 2

将两个列表合成为一个列表 元素为二元组
zip [1,2,3] ['A','B','C']
当一个比另一个长时 取短的那个


~~~
