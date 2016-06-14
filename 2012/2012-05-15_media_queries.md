<!--
Title: media queries 笔记
Tag: tips css
-->

media queries
=============

写样式的想兼顾手机，就顺便看了下media queries。

还是先上参考 <http://www.w3.org/TR/css3-mediaqueries/>

* * * * *

要想在手机上有效果，要在html里加上一句

~~~~ {.html}
<meta name="viewport" content="width=device-width">
~~~~

这个具体可以看一下

-   <http://dev.opera.com/articles/view/an-introduction-to-meta-viewport-and-viewport/>
-   <https://developer.mozilla.org/en/mobile/viewport_meta_tag>

* * * * *

我感觉css里有用的就几个

~~~~ {.css}
/* 宽度在960px以上 */
@media only screen and (min-width: 960px) {}

/* 宽度在960px以下 */
@media only screen and (max-width: 960px) {}

/* 横屏 & 竖屏 */
@media only screen and (orientation: landscape) {}
@media only screen and (orientation: portrait) {}

/* 高分屏? */
/* <https://github.com/h5bp/mobile-boilerplate/blob/master/css/style.css#L222> */
@media only screen and (min-device-pixel-ratio: 1.5) {}
~~~~
