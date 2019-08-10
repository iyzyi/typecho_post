# typecho_post

* 将小说按章节分段成单独的文章，并批量向typecho发送

* 将有道云笔记中的笔记复制到空白markdown文档中，可向typecho发送包括图片在内的笔记

## 使用介绍

首先对服务器上的typecho的/var/Widget/Security.php改动一处地方(修改token)：

```
public function execute()
{
    $this->_options = $this->widget('Widget_Options');
    $user = $this->widget('Widget_User');

    $this->_token = $this->_options->secret;
    if ($user->hasLogin()) {
        $this->_token .= '&' . $user->authCode . '&' . $user->uid;
    }
->> $this->_token = "I need to change part of token for up files easy by python.";
}
```

添加->>处所在的那一行（也可以改成你自己喜欢的，或者不改动，反正之后还要抓包获取token）

#### 发送小说

然后在**post.py**中修改后台的用户名和密码，以及你的博客网址

在**chapter.py**中按照目标小说的章节分段的样式修改相应的正则表达式

最后在**post_novel.py** 中填写分类及其缩略名、小说路径，并运行程序

#### 发送有道云笔记

手动将有道云笔记中的笔记复制到空白markdown文档中（这样才能将笔记中的图片也插入到笔记中），看个人喜欢习惯一下样式，比如加粗、标题之类

然后在**post.py**中修改后台的用户名和密码，以及你的博客网址

在**post_youdao.py** 中填写分类及其缩略、文章标题、笔记路径，并运行程序

## 文件简介

**post.py** 登录博客，创建/查找标签，发送文章

**post_novel.py** 将小说按章节分段，批量向博客发送

**post_youdao.py** 发送有道云笔记

**chapter.py** 将小说按章节分段

## TODO

完善token

图片的插入

人工智能识别非常规的章节标题，如“请假条”，”上架感言“等

小说文本的广告过滤

## 关于正则

**chapter.py**中的正则表达式只负责提取形如”第XX章“+1个空格+”名称“的标题，其他形式请相应额外修改后再使用。

其他形式包括不限于：章五，卷二，推本书，上架感言，1-3节

## 最后

考虑了一下，最终并没有把网址打码，答应我，小师傅们别去攻击我的服务器，好咩U•ェ•*U

毕竟我这一改，token没了，很容易受到攻击，U•ェ•*U



为什么token改成固定的而不是动态的？

**~~懒得具体修改~~** 　　**菜的不会修改**

## 更新

* 2019.8.11

  增加post_youdao.py

* 2019.8.9 

  初版