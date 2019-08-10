## **第一道▼古典密码签到**

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/5b502a0fb5ab4bc7a971d940c1767537/clipboard.png)

把密文用base16走一下，可得juttaigykhpmjyreca

我第一反应是凯撒密码的变种，j+6，u+3，一直到最后，key的位数不够的话就在把key在循环几次，构成63756D74 63756D74 6375

写py写到一半，发现我并不会写这种程序，主要是不知道如何用循环语句实现密文的第i个字母加上key的第i个数字。便用c++写的

```c++
#include<iostream> 
using namespace std;
int main()
{
	char s[]="juttaigykhpmjyreca";
	int key[]={6,3,7,5,6,13,7,4,6,3,7,5,6,13,7,4,6,3};
	for (int i=0;i<18;i++)
		if (s[i]+key[i]>122) cout<<char(s[i]+key[i]-26);
		else cout<<char(s[i]+key[i]);
	return 0;
}
```

输出为pxaygvncqkwrplyiid

看着不像flag呀，试了试果然不对

重新想了一下，把key也用base16走了一下，竟然是cumt

百度了一下，可能是维吉尼亚密码

找了个在线解密的网站

<https://www.qqxiuzi.cn/bianma/weijiniyamima.php>

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/62db28000fee4dc698c383d7f1f99a32/clipboard.png)

加上flag{}，提交

##　**第二道▼签到**

逆向第一道题，没有提示

用ida32打开，主函数为

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/3293542159234b5c8ae4bf396e8978ee/clipboard.png)

根据

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/f31f97e1adef41d5af308ed1efcea70e/clipboard.png)

可知flag长度应该为20（严格来说是小于等于20，我一般以为就是上界，但没想到这道的flag长度居然是10，以后要注意一下）

通过sub_401000函数进行变换，第一个形参为输入字符串，第二个形参为v5~v14的数值（严格来说是v5的地址，但我敢肯定函数里面绝对用到了地址的偏移）

sub_401000函数为

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/3614a343b71d491e9a7f6305aaf1e2c8/clipboard.png)

开始时没看懂*v3和v3[1]的关系，以为是v5~v14共十个变量，每个变量里可以分成两个数，如0x1054拆成0x10和0x54，至于谁在前谁在后，还要学一下存储的大头端和小头端。

我以为是这样共有20个数，转化成*(v3+1)^a1[i]==*v3，这样要求的a1[i]=v3[i]+v3[i+1]，可这样只能出来19个数，因为没有v3[21]，而且求出的前十九个字符中有不可见字符，肯定不对。

这样想的错误出现在：v3+=4

如0x1054是四个字节，每次v3地址偏移4个字节，这样，v3[1]和*v就很明显了

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/96b0c509a0264befbe151bd0081b94ba/clipboard.png)

走入误区的原因在于坚信flag一定长度为20

写出py

```python
v=[0x10,0x54,0x20,0x6b,0x30,0x5a,0x40,0x2f,0x50,0x12,
   0x60,0x57,0x70,0x46,0x80,0xe8,0x90,0xd1,0xa0,0xcc]
flag=''
i=0
while (i<20):
    flag+=chr(v[i]^v[i+1])
    i+=2
print(flag)
```

结果为DKjoB76hAl，不像是flag

因为这道题并没有提示，所以也没有加上flag{}还是cumtctf{}，所以我以为跑出来的flag会自带前缀。

以后要注意，没提示什么前缀的题目拿到的flag也并不一定自带前缀。

尝试加上flag{}，成功提交哦

## **第三道▼encode**

没有提示。

百度可知：pyc文件是py文件编译后生成的字节码文件(byte code)。pyc文件经过python解释器最终会生成机器码运行。所以pyc文件是可以跨平台部署的

c++有反编译，这个自然也有。

在线pyc文件进行解密。支持所有Python版本

<https://tool.lu/pyc/>

反编译后的py程序为

```python
import base64

def encode1(ans):
    s = ''
    for i in ans:
        x = ord(i) ^ 36
        x = x + 25
        s += chr(x)
    return s

def encode2(ans):
    s = ''
    for i in ans:
        x = ord(i) + 36
        x = x ^ 36
        s += chr(x)
    return s

def encode3(ans):
    return base64.b32encode(ans)

flag = ' '
print 'Please Input your flag:'
flag = raw_input()
final = 'LOQ2NJFYU5YH2WTUU5VHJIDXLJNVW2LQO52WS2L6PVUVW2TQLJNVSWLJUBN3E==='
if encode3(encode2(encode1(flag))) == final:
    print 'correct'
else:
    print 'wrong'
```

思路非常清晰，倒着写解密程序，如下：

```python
import base64

final='LOQ2NJFYU5YH2WTUU5VHJIDXLJNVW2LQO52WS2L6PVUVW2TQLJNVSWLJUBN3E==='

def decode3(ans):
     return base64.b32decode(ans)

def decode2(ans):
    s=''
    for i in ans:
        x=ord(i)^36
        x=x-36
        s+=chr(x)
    return s;

def decode1(ans):
    s=''
    for i in ans:
        x=ord(i)-25
        x=x^36
        s+=chr(x)
    return s;

print(decode1(decode2(decode3(final))))
```

flag{b38e7b57c2eff432044984f53efdd4cf}

成功拿到flag。不过恕我直言，对于学过一点点puthon的人来讲，这道题200分有点高，毕竟没有难度，2333（我是菜逼一个）

还有一点，最开始用winhex打开的.pyc，发现了

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/3d60e99f5c914f0eba7a9aee516d619f/clipboard.png)

肯定有base32，先把那个字符串用base32解码一下，在线解码居然失败了，用python解码看了一下，解码得到的是[ﾡﾦﾤﾸﾧp}ZtﾧjtﾠwZ[[ipwuii~}i[jpZ[YYiﾠ[ﾲ

后来用反编译拿到源代码后才反应过来，输入的字符串是正常的，但经过第一、二步的加密，使其变成了非标准ascll字符，在此基础上再用base32加密。所以用base32解密时直接得到的字符串必然是含有非标准ascll字符的，在线解密网站可能加入了判断是否为标准ascll字符的部分，而python的base64.b32decode（str）应该没有判断

## **第四道▼Whoami???**



![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/6f0b34a3758a4763a8d8cd84cbd6d19d/clipboard.png)

进入网页一看

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/96f6b78a19d342788622a570dbeff2fd/clipboard.png)

百度了一下如何用python向服务器发送请求

python通过get方式,post方式发送http请求和接收http响应-urllib urllib2

<https://www.cnblogs.com/poerli/p/6429673.html>

复制了其中一端代码，将url改成本题的url

如下：（直接复制拿来用的，现在还不懂原理，有空时要学一下web了）

```python
import urllib
import urllib2

url = "http://202.119.201.199:40106/"

req = urllib2.Request(url)
print req

res_data = urllib2.urlopen(req)
res = res_data.read()
print res
```

输出见下图

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/818b130f89274fc3bcdb7c7e7c7d07a0/clipboard.png)

根据网页的那一段话，最后一句很可疑啊。

我以为I'm a teapot是出题人写的，以为flag就在眼前了，然而上网查了一下，居然是由来已久的，并不是出题人自己写的。

不过还是加上flag{}后试了一下，居然成功进入下一个网页界面，

（后来想了下，题目中的问号写的是who am I，回答I’m teapot不正好回答了这个问题了吗）

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/51d53b4d6d364c1c95cda6c673ce4a57/clipboard.png)

点击提交进入下一界面，拿到flag

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/72068a88cfff461b9244832c9b00005f/clipboard.png)



## **第五道▼Lisp**

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/10c9361da68b47edbfbc7ec4de25a23e/clipboard.png)



![q.ss](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/8d23d85ba8a843a3b1f47c025027128e/attachment.png)

百度了下，lisp也是一种计算机语言，上世纪50年代的，很老了，但貌似是世界上最好的语言（笑）

下载附件，尝试用txt打开

```lisp
;; Author: Iv4n

;; input your flag-string here
(define flag *****)
(define final-string '(97 100 206 218 135 230 70 242 104 107 95 104 97 107 100 206 101 218 137))

(define (process-flag flag)
    (define (convert i)
        (let ([iv-0 #x0c]
              [iv-1 #x2e]
              [iv-2 #x3a])
            (cond ((= (remainder i 3) 1) (+ (* i 2) iv-0))
                  ((= (remainder i 2) 0) (+ (/ i 2) iv-1))
                  ((> i 90) (+ i iv-0))
                  (else (+ i iv-2)))))
    (define (iter lst)
        (cond ((null? lst) '())
              ((not (pair? lst)) (list (convert lst)))
              (else (append (iter (car lst)) (iter (cdr lst))))))
    (iter flag))

(define converted-string (process-flag flag))
(display (if (equal? converted-string final-string)
    "Congratulations!"
    "try again~"))
```

可以分析源代码分三个阶段

第一阶段，输入flag，定义最终final字符串

第二阶段，

​     前半段，对flag加密，并与final比较

​     后半段，推测是将数据转化成字符串（不太清楚，但对解题应该没影响）

第三阶段， "Congratulations!"  or  "try again~"



很明显，主要是第二阶段的前半段。

之前没有接触过lisp，自然不懂它的语法和函数等，遇到不会的地方就百度，加以推测，最终基本搞懂了。

`(define (process-flag flag) `

第一行定义一个变量

`(define (convert i) `

第二行，猜测类似与python的for的迭代，一个一个字符的读入

```lisp
(let ([iv-0 #x0c]
      [iv-1 #x2e]
      [iv-2 #x3a])
```

之后的三行，推测#x0c就是0x0c，iv-0估计就是变量名

```lisp
 (cond ((= (remainder i 3) 1) (+ (* i 2) iv-0))
                  ((= (remainder i 2) 0) (+ (/ i 2) iv-1))
                  ((> i 90) (+ i iv-0))
                  (else (+ i iv-2)))))
```

cond类似于if-elif-else

> 当分两种情况时，使用if函数即可，两种以上的情况时，使用cond函数比较方便。例子1：如果a>0,则b=+1；否则，b=-1
>
> （if（a>0） （setq b +1） （setq b -1））
>
> 例子2：如果a>=100，则b=2；如果10<=a<100,则b=1；如果a<10,b=0
>
> (cond
>
> ((>= a 100) (setq b 2))
>
> ((>= a 10) (setq b 1))
>
> (t (setq b 0))
>
> ）

remainder取余

> ( REMAINDER N1 N2 )取N1除以N2的余数，结果放入N1

另外，lisp语法和c++和python不太一样，它的操作符在首位，后面跟着操作数据

如1+2表示为+ 1 2（中间有空格）

在此基础上（结合：( REMAINDER N1 N2 )取N1除以N2的余数，结果放入N1），我猜测+ a b 是计算a+b并将结果放入a（事实证明我猜对了）

搞明白加密原理后，我写了个等效的python脚本（仅加密部分）

```python
for i in flag:  
    if i%3==1:
        i=i*2+0x0c
    elif i%2==0:
        i=i//2+0x2e
    elif i>90:
        i=i+0x0c
    else:
        i=i+0x3a
```

对应写出解密脚本

注意：正向加密的时候一个明文值仅仅对应一个密文值，但逆向解密的时候，一个密文值可能对应多个明文值（毕竟四种加密方式），这就要结合题中的/[0-9a-z_{}]+/来判断取值。

解密脚本：

```python
def try0x0c_1(n):    #对应if i%3==1: i=i*2+0x0c
    i=n
    n-=0x0c
    if n%2==0 and (n//2)%3==1:
        return n//2
    return 0

def try0x2e(n):    #对应elif i%2==0: i=i//2+0x2e
    i=n
    n-=0x2e
    n*=2
    if n%2==0 and not (n%3==1):
        return n
    return 0

def try0x0c_2(n):    #对应elif i>90: i=i+0x0c
    i=n
    n-=0x0c
    if n>90 and not (n%2==0 or n%3==1):
        return n
    return 0

def try0x3a(n):    #对应else:
    n-=0x3a
    if n<=90 and not (n%2==0 or n%3==1):
        return n
    return 0

final=[97 ,100 ,206 ,218 ,135 ,230 ,70 ,242 ,104 ,
       107 ,95 ,104 ,97 ,107 ,100 ,206 ,101 ,218 ,137]
flag=''
for i in final:
    if try0x0c_1(i)!=0:
        print(chr(try0x0c_1(i)),end=' ')
    if try0x2e(i)!=0:
        print(chr(try0x2e(i)),end=' ')
    if try0x0c_2(i)!=0:
        print(chr(try0x0c_2(i)),end=' ')
    if try0x3a(i)!=0:
        print(chr(try0x3a(i)),end=' ')
    print ("\n")
```

输出有：

```
f ' 
l 
a ŀ 
g Ř 
{ M 
m Ű 
0 
s ƈ 
. t 
z _ 
b 
. t 
f ' 
z _ 
l 
a ŀ 
n 
g Ř 
¶ } 
```

根据/[0-9a-z_{}]+/，并根据实际含义，可以写出flag{m0st_btf_lang}

解释一下实际含义，比如第10个可以写z，也可以写_，都是满足取值的，但根据flag的常用格式，可以猜测应选下划线

## 第六道▼ 真真假假

没有提示，但我算是认识到运气好是一种什么体验了，第一次拿首答

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/e3d18f8b0556435784a972907dc7987d/clipboard.png)

下载压缩包，发现加密了，首先尝试伪加密。

用winhex打开压缩包

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/ebf1d9ca560b4302b304bf7b0a6e3eb9/clipboard.png)

发现在全局加密位并没有置成加密，所以一定是伪加密。

在winhex工具栏上找到HEX按钮（用于搜索十六进制）

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/2163dd15bf924f2b84db638869815c56/clipboard.png)

输入504B0102，查找到其所在位置

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/bd91c3aebe5f4ee2bfee7549f3a44a0b/clipboard.png)

将9改为0，保存



关于伪加密

压缩源文件数据区： 

50 4B 03 04：这是头文件标记（0x04034b50） 

14 00：解压文件所需 pkware 版本 

00 00：全局方式位标记（有无加密） 

08 00：压缩方式 

这个地方的标志位叫 frFlags



压缩源文件目录区： 

50 4B 01 02：目录中文件文件头标记(0x02014b50) 

3F 00：压缩使用的 pkware 版本 

14 00：解压文件所需 pkware 版本 

00 00：全局方式位标记（有无加密，这个更改这里进行伪加密，改为09 00打开就会提示有密码了） 

08 00：压缩方式 

还有就是，是否加密看的是第二个数位是奇数还是偶数，奇数表示加密，偶数表示未加密（如：09 00为加密，00 00未加密）

再者，50 4B 03 04部分标记为加密，则一定不是伪加密。只有50 4B 03 04部分标记为未加密，而50 4B 01 02部分标记为加密，这样才是伪加密。



解压后，得到img.html

打开一看，一行很长的文本，直接后缀改为txt，打开（因为太长了，100+KB，我就不全粘贴了，复制一部分，仅供看看文本风格）

开头

> /9j/4AAQSkZJRgABAQEASABIAAD/4REoRXhpZgAATU0AKgAAAAgABgESAAMAAAABAAEAAAExAAIAAAAUAAAIYgEyAAIAAAAUAAAIdodpAAQAAAABAAAIipycAAEAAABCAAAQzuocAAcAAAfqAAAAVgAAAAAc6gAAAAgAAAAAAAAc6gAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

中间

> +LrGzdUuktXK3Nmz/cE0LhZIj7OgNfgb/wcaeItI13/gql4qTTLq4u59L0XTLLUd5/d29ykPmbE/7Zun/A5Hrmf+CG/wAc9b/Z5/bqh8TWt5Ja+EtL8NatqHjXd/qBpNravPvf/b89Idn+2+z+Ovrv9WYTy6GKhP3+xnzn9GPxJ/aU+HfwW1O3sPGHj7wb4Vv7pN8FvrOtW1jJcJ/eVZHTP1FcN8cf2NfgR+394Phv/FXhHwZ48s7yPNrrdoI5LjZ/ehvIf3n/AHw9fy8ftH/HzxB+1d8c/E/xE8WXMl9rXii9e6ff+8+zp/ywgT+4iR7ERP8ApnX3n/wbAfGTx9o/7a194I8Ptfal8OtV0m5vfENt872mlzon7i6/uJI8n7n/AG9//TOjE8N1MJhvrMa3vxD2h7d+15/wasI32rVPgf44kt9p3p4f8VfvIz/sJeRp5n/fxH/36/Ln9p/9i/4p/saeI/7N+JXgnWPDLeZ5cF5MnmWF5/1xuU+R/wDvuv65VGKxPGPgrSPH/h280fXtJ0/XNL1CPy7myvrRLi3uU/uOj5RvxrHA8WYqj7lb30P2aP4//h58RfEPwh8X2fiDwrr2seGde0//AFGpaVdPazx/8DSv1C/YV/4OevGXw7e00H46aK3jfR12J/wkOjokGrW6f35oPkjm/wCAbH/36+lf23f+DZL4Z/GMXWtfB/Um+F/iKX5/7NbfdaDcSf8AXP78H/bM7P8AYr8dv2v/APgn58XP2FfEf2D4keD77SrOR9lrrFt/pWk6h/uXKfJ/wCTZJ/sV9LTxWV5vDkqaTI1if07/ALMn7Yvw4/bM8Bp4h+Gvi3S/EtjjEyQvsurN/wC5NC/7yF/Z0FeqsNtfx4/CD4yeLP2fvHdn4q8E+JNY8K

结尾

> j/APkSvqT4Lf8ABJ79nP8AZ/mjuPDPwf8ABcF5GPku76y/tG5T/ttc+ZJ+tZVOMMFS/gUy/Zn8yHwY/Zb+Jf7Q14lt4D+HvjHxa39/TdInnt/+BzbNif8AbR6+0v2fP+DZ79oj4vRxXHiqTwr8M9Nf5/8AiZXv26/2f9cYd8f/AH3Ilf0N2FhDpdnFb28McMMabURE2ogq5srxcVxnip/wY8gezPzJ/Zr/AODYD4H/AAse2vPH2r+JvibqCfO0M7/2Xpv/AH4g+f8A77kNffXwZ/Zy8C/s7eHE0fwL4P8ADvhLTY12CDSdPjtRJ/v7B8//AAOu92CjFfO4rMcTXd60yuVC0UUVylBRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRiiigBvlCnYoooAMUYoooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/2Q==

毫无头绪，最后两个==让我有点怀疑是base64，然而解码是乱码。又想了一会，脑子一抽居然把100+KB的文本整体用base64解码了，大部分都是乱码，但居然有两个部分是正常的

分别是

> ZmxhZ3toMzExb190SDFzXzFTX2YxNGd9Adobe Photoshop 7.02009:11:25 21:24:19

以及

> http://ns.adobe.com/xap/1.0/<?xpacket begin='﻿' id='W5M0MpCehiHzreSzNTczkc9d'?>

> <x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:Description rdf:about="uuid:faf5bdd5-ba3d-11da-ad31-d33d75182f1b" xmlns:xmp="http://ns.adobe.com/xap/1.0/"><xmp:CreatorTool>Adobe Photoshop 7.0</xmp:CreatorTool></rdf:Description><rdf:Description xmlns:dc="http://purl.org/dc/elements/1.1/"/><rdf:Description xmlns:dc="http://purl.org/dc/elements/1.1/"/></rdf:RDF></x:xmpmeta>



首先想的是进入第二个的那个网站，但没进去。然后观察第一个的前半部分有点像base64呀，解码，居然拿到flag了，你敢信？

ZmxhZ3toMzExb190SDFzXzFTX2YxNGd9

flag{h311o_tH1s_1S_f14g}

## **第七道▼  现代密码签到**

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/281c14f60e2d46dc8e49c211eb7fcf41/clipboard.png)

这种题就是碰运气吧（我还能怎样，能怎样~？）

把key两次base64解码，得到cumtflag，作为密钥（一开始直接把key拿来用，自然解不出来啦）

尝试把密文base64解码，但出来乱码，所以放弃。

尝试各种现代密码，最终通过RC4解密，拿到flag

<http://tool.chacuo.net/cryptrc4>

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/3eb64bfc26f94d72afb34ec32fd3b338/clipboard.png)

flag{CumT_D0uB13_MooN_cTf}



## **第八道▼ web签到**



给出网址[http://202.119.201.199:30100](http://202.119.201.199:30100/)（估计等我再回头看WP时，这个页面早没了，毕竟内网）

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/b93688fde93249ae9a88475b01800ca6/clipboard.png)

定义了变量$page，其值为GET到的内容

若不为空，则操作，若为空，输出page!!!!



在浏览器的地址栏输入

<http://202.119.201.199:30100/?page=php://filter/read=convert.base64-encode/resource=cxk.php>

输出PD9waHAgDQpwaHBpbmZvKCk7IA0KLypmbGFne0N1bXRDVEZfdGhpc19pU19hX1JFbEx5X2ZMYUchISF9Ki8NCj8+DQo=

base64解码得到cxk.php的源代码

<?php  phpinfo();  /*flag{CumtCTF_this_iS_a_RElLy_fLaG!!!}*/ ?> 

拿到flag{CumtCTF_this_iS_a_RElLy_fLaG!!!}

几个文件包含的博客

<https://www.cnblogs.com/whitehawk/p/9940184.html>

<https://www.cnblogs.com/zcz1995/articles/10264030.html>

<https://www.cnblogs.com/bmjoker/p/9035259.html>

**不打算继续做了，要准备高数考试了，截图留念**

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/89c5a03fb5fa46a5adb3450874610772/clipboard.png)

**最终排名**

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/d38d8be4a25a44f388e43f6762814734/clipboard.png)