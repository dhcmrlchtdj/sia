# js里的高度

最近在写一个带iframe的页面，要求根据iframe内容调整高度，也就是说自适应。

接着就对js绝望了，不仅仅是ie，每个浏览器都是按着自己的一套来解释。

结论就是，应该合理使用jquery，yui等现成的框架类库，
浏览器的兼容性问题根本就是前端的地狱。

------

总结下关于js里面和宽度高度有关的属性。

一样先是参考资料

+ <http://www.quirksmode.org/mobile/viewports.html>
+ <http://www.quirksmode.org/dom/w3c_cssom.html>

------
```javascript
// 1. window

// ie678 不支持 1.1 - 1.4
// opera 不支持 1.4

// 1.1 浏览器显示的页面大小（浏览器大小 减去 浏览器面板大小）
window.innerWidth
window.innerHeight

// 1.2 浏览器大小
window.outerWidth
window.outerHeight

// 1.3 浏览器显示的页面 和 整个html页面 边界的距离
window.pageXOffset
window.pageYOffset

// 1.4 浏览器 相对 显示器 的距离
window.screenX
window.screenY

// 1.5 显示器的大小
// screen === window.screen
screen.availWidth
screen.availHeight
screen.width
screen.height
```
感觉比较实用的只有`innerHeight`和`pageYOffset`。

------

```javascript
// 2. element
// 列举几个相关属性，2.1 - 2.5 都是只读属性
// 下面用e表示element

// 2.1 相对父元素（offsetParent）的位置
// ie67 下有问题
e.offsetTop
e.offsetLeft

// 2.2 元素的宽/高度
// 包括border在内，不含margin
e.offsetWidth
e.offsetHeight

// 2.3 元素的宽/高度
// 包括width和padding，不包括滚动条和border
e.clientWidth
e.clientHeight

// 2.4 border-top和border-left的大小
// 在文字是 右往左 的情况下，clientLeft会包括滚动条的宽度
e.clientTop
e.clientLeft

// 2.5 元素的实际大小
// 包括padding，无视boder，不含margin
// 在有即使有滚动条，也是返回元素的实际大小
// 没有滚动条就和clientWidth/clientHeight一样了
// ie67 和 opera10.6以下 可能有问题
e.scrollWidth
e.scrollHeight

// 2.6 元素可见部分 和 元素边界 的距离
// scrollTop = scrollHeight - clientHeight
// 没有滚动条时等于clientWidth/clientHeight
// 可以赋值，相当于移动滚动条了
e.scrollTop
e.scrollLeft
```

上面一堆看着可能乱了点，要获取页面高度。
首先是获取2个元素`document.documentElement`和`document.body`，
前者表示整个html文档，后者是整个body元素。
要获取页面高度也就是获取这两者的高度了，而且是必须两个都获取。
因为不同浏览器在处理上有差异，
使用的时候最好在多个浏览器上进行测试。

我自己写的自适应的代码蛮贴出来好了

```javascript
function setHeight() {
    var iframe = document.getElementById('#iframe');
    var iframe_doc = iframe.contentDocument || iframe.contentWindow.document;
    var _height = Math.min(iframe_doc.documentElement.scrollHeight,
        iframe_doc.body.scrollHeight);
    iframe.height = _height;
}
```

------

下面这个算附加的吧

```javascript
// 3. mouse event
// 鼠标点击的位置

// 3.1 相对整个html
// ie不支持
event.pageX
event.pageY

// 3.2 相对浏览器窗口
event.clientX
event.clientY

// 3.3 相对显示器
event.screenX
event.screenY

// 3.4 相对元素本身
// 各个浏览器实现都不一样？
event.offsetX
event.offsetY

// 4
// 4.1 在页面内移动
x = document.querySelector(str);
x.scrollIntoView();
```

------

最后来黑一下chrome，在本地调试js的时候，老说访问iframe（同样在本地）跨域了，
完全没法子，这根本就是bug吧？

