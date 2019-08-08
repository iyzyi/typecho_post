# typecho_post

 批量向typecho博客发送文章

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

然后在**post.py**中修改后台的用户名和密码，同时将所有的网址全部改成你的（通过抓包获取token）

在**chapter.py**中按照目标小说的章节分段的样式修改相应的正则表达式

最后在**posts.py** 中填写小说路径，并运行程序

## 文件简介

**post.py** 登录博客，创建/查找标签，发送文章

**posts.py** 将小说按章节分段，批量向博客发送

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

