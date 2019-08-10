　　刚看完一本欢乐书客上的网络小说《我的网恋女友是妹妹》（后因神秘力量更名为《我的网恋女友》），特别喜欢这本书，想下载下来。github发现了三个python的项目，但都没能成功下载，最后发现了这个golang的项目，虽然没有golang的使用经验，但最终还是成功使用其成功下载了目标小说。

下面为详细过程：

## 零、安装golang

从官网下载对应版本的golang，按照提示安装即可。

注意将安装目录下的\bin放入环境变量。

## 一、安装git

安装（编译）过程中会提示缺少一些扩展包，要通过`go get XXX`语句从网络上下载扩展包，go get语句是通过git实现的，所以需要提前下载git，windows下载64位或32位安装包即可

安装成功后需要配置Git环境变量，在Path变量中增加形如：C:\Program Files\Git\cmd

验证是否配置成功，打开windows命令行，输入`git version`命令，出现信息表示配置成功。

（修改环境变量后要重新打开cmd窗口才会生效）

图为未安装git时使用go get的后果：

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/b06dbcace513498e8ae87ce1edbd305b/clipboard.png)



## **二、源文件**

从github上获取dhbooker源文件。我fork的： <https://github.com/iyzyi/dhbooker> 

解压放入以下两个路径中的其中一个即可

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/00f1dd0b9f8a40dfa06882862d893ae2/clipboard.png)

## 三、安装dbhooker

`go install dhbooker `

会提示以下内容，缺少扩展包

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/7658f7cbacd84ddfb1e4c9b7e281d8a9/clipboard.png)

按提示，用go get 下载即可

```cmd
go get github.com/PuerkitoBio/goquery 
go get github.com/Unknwon/goconfig 
go get github.com/tidwall/gison 
go get gopkg.in/cheggaaa/pb.v1
```

如下图：

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/294a630ddd294ab2adfd6a44c0a92041/clipboard.png)

中间过程中会有一个包下载失败，提示：

> package golang.org/x/net/html: unrecognized import path "golang.org/x/net/html" (https fetch: Get https://golang.org/x/net/html?go-get=1: dial tcp 216.239.37.1:443: connectex: A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond.)

这是因为墙内无法直连提示的那个网站，解决方法是在github上下载安装失败的那个包，然后放到相应的位置即可。

缺失的包的github链接 <https://github.com/golang/net.git>，下载后将html文件夹放入`C:\Users\kljxn\go\src\golang.org\x\net`

下图为为什么要放到该路径的提示：

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/69d84e1821a14a15a8eaa7a066b14f96/clipboard.png)

再次使用`go install dhbooker`，成功安装



**四、使用**

`go run dhbooker -b 100061744 `



![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/fcc5a26df9f34a8ba61c19583500122e/clipboard.png)

conf.ini在C:\Users\kljxn\conf.ini，填写欢乐书客的账号和密码，以及下载的目录和临时目录

再次使用`go run dhbooker -b 100061744 `

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/670b0c7dc6434e6bb880818077326171/clipboard.png)



**参考：**

[golang.org/x/net 安装方法](https://blog.csdn.net/xie1xiao1jun/article/details/79421136)

