<!--
Title: 再一次，重装系统
Tag: archlinux software
-->

# 再一次，重装系统

写篇主要是是记录下自己常用的软件，免得每次重装总觉得好像漏了什么。

其实 arch 是个很稳定的发行版，有了 aur 的存在，各种软件都很齐全，
用起来是很惬意的事情。这次会重装，因为我在国庆期间把 i686 换成了 x86_84，
估计系统内存不够了，玩着玩着内存就用没了，然后卡得受不了。所以决定换回 i686。

按着安装顺序来说吧，我自己用的 KDE，如果有 GNOME 爱好者参考的话，
换成相应软件的就可以了。

安装系统时，base 和 base-devel 就不用说了，然后是 grub-bios 和 os-prober。
如果不是双系统，os-prober 也省了。syslinux 和 EFI 之类的，没用过……

装好系统之后先装个 sudo 再添加权限，就可以切换到用户账户继续干了。

关于联网，安装好 networkmanager，再装个 kdeplasma-applets-networkmanagement
就好了。有几个补丁，有用到就打上把。

xorg，xf86-video，alsa 看着装就可以了。
触摸板可以装个 synaptiks 来设置相关选项。

之后装好 kdebase，arch 的包打得很散，还要加不少其他东西。

+ kde-l10n-zh_cn 中文。
+ kdemultimedia-kmix 音量。
+ kde-gtk-config，oxygen-gtk2，oxygen-gtk3 调整gtk程序界面。
+ kdegraphics-ksnapshot 截图。
+ kdeutils-ark 解压，再装上 p7zip unzip unrar。
+ kdegraphics-okular，kdegraphics-mobipocket 看 pdf、epub、chm 之类的。
+ kuickshow 看图。
+ kcm-qt-graphicssystem qt 程序界面？
+ k3b 刻录。
+ amarok 听歌。
+ calligra-krita + calligra-sheets + calligra-words 
    不得不说 linux 下面办公画图战斗力都只有 5。

基本的系统就装好了。然后把 shell 换成 zsh。
看网页用 opera + flashplugin 和 chrome，firefox 基本上就是摆设。
看视频用 smplayer。
写代码用 gvim，再加上 git 和 openssh。
字体我是用雅黑，等宽是 monaco 加上雅黑，其他字体个人感觉都不能打。
关于 opera 的字体，可以自己动手改 .Xresources，
我是直接用了 ubuntu 的 fontconfig 补丁。
输入法用 fcitx，补上 kimtoy。

下面就只是我自己偶尔用的到的。

+ axel 下载。
+ soundKonverter 装换音频格式。
+ kid3 编辑音乐标签。
+ mp3splt 分割音频文件。
+ aafm、android-udev、android-sdk-platform-tools  连接 android 机器。
+ mentohust 万恶的锐捷。
+ ntp 更新时间，没什么存在感。
+ lftp、tmux 装了没怎么用到。
+ ctags、v8、bpython……

如果遗漏了什么，发现了再补全吧。
