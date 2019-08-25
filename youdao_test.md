帝国の绝凶虎（mengxin）的CTF初体验，大佬退避(o゜▽゜)o☆

## 第一道▼逆向签到

下载文件，打开IDA64，把文件脱进来，F5将汇编翻译成c语言

主函数：

```汇编转C
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  size_t v4; // rbx
  int v5; // [rsp+0h] [rbp-C0h]
  int v6; // [rsp+4h] [rbp-BCh]
  int v7; // [rsp+8h] [rbp-B8h]
  int v8; // [rsp+Ch] [rbp-B4h]
  int v9; // [rsp+10h] [rbp-B0h]
  int v10; // [rsp+14h] [rbp-ACh]
  int v11; // [rsp+18h] [rbp-A8h]
  int v12; // [rsp+1Ch] [rbp-A4h]
  int v13; // [rsp+20h] [rbp-A0h]
  int v14; // [rsp+24h] [rbp-9Ch]
  int v15; // [rsp+28h] [rbp-98h]
  int v16; // [rsp+2Ch] [rbp-94h]
  int v17; // [rsp+30h] [rbp-90h]
  int v18; // [rsp+34h] [rbp-8Ch]
  int v19; // [rsp+38h] [rbp-88h]
  int v20; // [rsp+3Ch] [rbp-84h]
  int v21; // [rsp+40h] [rbp-80h]
  int v22; // [rsp+44h] [rbp-7Ch]
  int v23; // [rsp+48h] [rbp-78h]
  int v24; // [rsp+4Ch] [rbp-74h]
  int v25; // [rsp+50h] [rbp-70h]
  int v26; // [rsp+54h] [rbp-6Ch]
  int v27; // [rsp+58h] [rbp-68h]
  int v28; // [rsp+5Ch] [rbp-64h]
  int v29; // [rsp+60h] [rbp-60h]
  int v30; // [rsp+64h] [rbp-5Ch]
  int v31; // [rsp+68h] [rbp-58h]
  int v32; // [rsp+6Ch] [rbp-54h]
  int v33; // [rsp+70h] [rbp-50h]
  char s[40]; // [rsp+80h] [rbp-40h]
  int v35; // [rsp+A8h] [rbp-18h]
  int i; // [rsp+ACh] [rbp-14h]

  puts("* please input flag: ");
  __isoc99_scanf("%s", s);
  if ( strlen(s) == 29 )
  {
    v35 = rand() % 100;
    for ( i = 0; ; ++i )
    {
      v4 = i;
      if ( v4 >= strlen(s) )
        break;
      s[i] ^= v35;
    }
    v5 = 53;
    v6 = 63;
    v7 = 50;
    v8 = 52;
    v9 = 40;
    v10 = 1;
    v11 = 50;
    v12 = 61;
    v13 = 55;
    v14 = 99;
    v15 = 62;
    v16 = 118;
    v17 = 98;
    v18 = 60;
    v19 = 60;
    v20 = 12;
    v21 = 106;
    v22 = 58;
    v23 = 37;
    v24 = 54;
    v25 = 12;
    v26 = 38;
    v27 = 12;
    v28 = 102;
    v29 = 48;
    v30 = 60;
    v31 = 33;
    v32 = 54;
    v33 = 46;
    if ( (unsigned int)Check((__int64)s, (__int64)&v5) == 1 )
      puts("* CCCCCCCCCCCongratulation!!!!");
    else
      puts("* try it again");
    result = 0;
  }
  else
  {
    puts("* try it again");
    result = 0;
  }
  return result;
}
```

check函数：

```汇编转C
signed __int64 __fastcall Check(__int64 a1, __int64 a2)
{
  signed int i; // [rsp+1Ch] [rbp-4h]

  for ( i = 0; i <= 28; ++i )
  {
    if ( *(char *)(i + a1) != *(_DWORD *)(4LL * i + a2) )
      return 0LL;
  }
  return 1LL;
}
```



主函数中下图所示的代码块将输入的字符串逐个字符地与随机数（0~99）进行异或

（若a^b=c，则a=b^c,按此原理可写脚本）

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/1366a9d20da5475cbd23da5bac1fa3fa/clipboard.png)

check函数将经过异或处理后的数据和主函数中存储的v5~v33作比较，相同则返回真

第一次接触逆向的题，我没想明白随机数每次都变，怎么保证输入的字符串是正确答案？

后来无意中暴力了一下，得到了100个不同的字符串，这才想明白，有100个字符串是正确答案，一个随机数对应一个，也就是说，当flag的字符串对应的随机数并没有随机到的时候，这是输入flag后也会显示* try it again

我写的暴力脚本：

（python还在学，不熟练，先用c++）

（c++是世界上最好的语言，233）

```c++
#include<iostream>
#include<cstdlib>
#include<ctime> 
using namespace std;
int main()
{
	srand(time(0));//不写这个的话，随机数并不随机
	int v[29]={53,63,50,52,40,1,50,61,55,99,62,118,98,60,60,12,106,58,37,54,12,38,12,102,48,60,33,54,46};
    int v35=rand()%100;
    for (int i=0;i<=99;i++)
    {
    	v35=i;
    	cout<<v35<<endl;
    	for (int i=0;i<=28;i++)
    		cout<<(char(v35^v[i]));
		cout<<endl;
	}
    return 0;
}
```

结果

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/09e108ecffcf4dbe97a6447c6de3d32b/clipboard.png)

## **第二道▼base全家桶了解一下??**

base64解码为base32再解码到base16再解码到明文

密文：R1kzRE1RWldHRTNET04yQ0dVM1RNTkpXSU0zREdNWlFHWkNETU5KVklZM1RJTVpRR01ZREtSUldHTTNUS05TRUc0MkRNTVpYR1EzRE1OMkU=

64转32：

GY3DMQZWGE3DON2CGU3TMNJWIM3DGMZQGZCDMNJVIY3TIMZQGMYDKRRWGM3TKNSEG42DMMZXGQ3DMN2E

32转16

666C61677B57656C63306D655F7430305F63756D746374667D

16解码：   

flag{Welc0me_t00_cumtctf}



Base64编码是使用64个可打印ASCII字符（A-Z、a-z、0-9、+、/）将任意字节序列数据编码成ASCII字符串，另有“=”符号用作后缀用途。



Base32编码是使用32个可打印字符（字母A-Z和数字2-7）对任意字节数据进行编码的方案



Base16编码使用16个ASCII可打印字符（数字0-9和字母A-F）对任意字节数据进行编码



## **第三道▼现代密码签到**

两次DES解码

密文：

U2FsdGVkX1+p43JX7+KrdUBXg/UTw+ejas2dbmiVanvVSxOuhSdp3JLc+7G4zK5p hHvL/5MHRKFV/L2THW1XCylB3U+pxCxbmnpQ2RB2ZTU=U2FsdGVkX1+p43JX7+KrdUBXg/UTw+ejas2dbmiVanvVSxOuhSdp3JLc+7G4zK5p hHvL/5MHRKFV/L2THW1XCylB3U+pxCxbmnpQ2RB2ZTU=

第一次解码：

U2FsdGVkX18968C+7acWUzWtYyuQd2MFLMh0HnGGnMlmYlemknPnfg==

第二次解码：

cumtctf{double_D3s_HHH}

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/650eaaeb76ee42cd84b96cb4e01fa74e/clipboard.png)



![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/4296108ba4fc4b1289d3360be5fb7b13/clipboard.png)



## **第四道▼Misc签到**

对照盲文翻译即可，翻译为BAIND，根据提示，改为B1IND，正好和BLIND（盲的）相似

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/edc361fb748d43f19c4eb079f516f37c/clipboard.png)



![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/346cb5a3f9064a17adbd11997bbadb04/timg.jpg)

## **第五道▼Easy_Math**

用IDA64打开

主函数：

```汇编转C
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  char v4; // [rsp+0h] [rbp-160h]
  int v5; // [rsp+100h] [rbp-60h]
  int v6; // [rsp+104h] [rbp-5Ch]
  int v7; // [rsp+108h] [rbp-58h]
  int v8; // [rsp+10Ch] [rbp-54h]
  int v9; // [rsp+110h] [rbp-50h]
  int v10; // [rsp+114h] [rbp-4Ch]
  int v11; // [rsp+118h] [rbp-48h]
  int v12; // [rsp+11Ch] [rbp-44h]
  int v13; // [rsp+120h] [rbp-40h]
  __int64 v14; // [rsp+130h] [rbp-30h]
  __int64 v15; // [rsp+138h] [rbp-28h]
  __int64 v16; // [rsp+140h] [rbp-20h]
  __int64 v17; // [rsp+148h] [rbp-18h]
  int v18; // [rsp+150h] [rbp-10h]
  char s[8]; // [rsp+157h] [rbp-9h]
  char v20; // [rsp+15Fh] [rbp-1h]

  *(_QWORD *)s = 0LL;
  v20 = 0;
  v14 = 0LL;
  v15 = 0LL;
  v16 = 0LL;
  v17 = 0LL;
  v18 = 0;
  v5 = 1;
  v6 = 2;
  v7 = 1;
  v8 = 2;
  v9 = 1;
  v10 = 1;
  v11 = 1;
  v12 = 1;
  v13 = 2;
  memset(&v4, 0, 0x100uLL);
  puts("* please input flag: ");
  __isoc99_scanf("%s", s);
  if ( strlen(s) == 9 )
  {
    String2Int(s, (__int64)&v14);
    Change((__int64)&v14, (__int64)&v5, (__int64)&v4);
    if ( (unsigned int)Check((__int64)&v4) == 1 )
      puts("CCCCCCCCCCCongratulation!!!!");
    else
      puts("try it again");
    result = 0;
  }
  else
  {
    puts("* try it again");
    result = 0;
  }
  return result;
}
```

String2Int函数：

作用很简单，把输入的字符串的每一个字符都分别赋值给从v14开始的9个变量

```汇编转C
size_t __fastcall String2Int(const char *a1, __int64 a2)
{
  size_t result; // rax
  int i; // [rsp+1Ch] [rbp-14h]

  for ( i = 0; ; ++i )
  {
    result = strlen(a1);
    if ( i >= result )
      break;
    *(_DWORD *)(4LL * i + a2) = a1[i];
  }
  return result;
}
```

change函数：（就你这破函数事儿多，变啥变啊，看了我好几个小时）

这个太难看了，萌新不会写算法，所以就手动模拟了（模拟图见本题最后）

```汇编转C
_DWORD *__fastcall Change(__int64 a1, __int64 a2, __int64 a3)
{
  _DWORD *result; // rax
  signed int m; // [rsp+24h] [rbp-14h]
  signed int l; // [rsp+28h] [rbp-10h]
  signed int k; // [rsp+2Ch] [rbp-Ch]
  signed int j; // [rsp+30h] [rbp-8h]
  signed int i; // [rsp+34h] [rbp-4h]

  for ( i = 0; i <= 2; ++i )
  {
    for ( j = 0; j <= 2; ++j )
    {
      result = (_DWORD *)(4 * (3 * i + (signed __int64)j) + a3);
      *result = 0;
    }
  }
  for ( k = 0; k <= 2; ++k )
  {
    for ( l = 0; l <= 2; ++l )
    {
      for ( m = 0; m <= 2; ++m )
      {
        result = (_DWORD *)(4 * (3 * k + (signed __int64)l) + a3);
        *result += *(_DWORD *)(4 * (3 * m + (signed __int64)l) + a2) * *(_DWORD *)(4 * (3 * k + (signed __int64)m) + a1);
      }
    }
  }
  return result;
}
```

Check函数：

经过change变换后的字符与check内的局部变量v2~v10相比较

```汇编转C
signed __int64 __fastcall Check(__int64 a1)
{
  int v2; // [rsp+8h] [rbp-30h]
  int v3; // [rsp+Ch] [rbp-2Ch]
  int v4; // [rsp+10h] [rbp-28h]
  int v5; // [rsp+14h] [rbp-24h]
  int v6; // [rsp+18h] [rbp-20h]
  int v7; // [rsp+1Ch] [rbp-1Ch]
  int v8; // [rsp+20h] [rbp-18h]
  int v9; // [rsp+24h] [rbp-14h]
  int v10; // [rsp+28h] [rbp-10h]
  int i; // [rsp+34h] [rbp-4h]

  v2 = 274;
  v3 = 294;
  v4 = 316;
  v5 = 262;
  v6 = 274;
  v7 = 252;
  v8 = 380;
  v9 = 421;
  v10 = 427;
  for ( i = 0; i <= 8; ++i )
  {
    if ( *(_DWORD *)(4LL * i + a1) != *(&v2 + i) )
      return 0LL;
  }
  return 1LL;
}
```



手动模拟，解出方程，转换成char类型的，得到flag

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/a94662fefe5641bda58af8c8823ae0f3/f399e0f88576ad8c9e6e50940847bfd8.jpg)



![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/bcdffd6b21524eb699fcd2583f983400/clipboard.png)



## **第六道▼BXS图标真好看**

（这是我们队（c家家）的第七道，我队第六道是张龙做的web）

后缀改为png，得到密文fgookwnl{_un_gaDy_0p}，刚开始以为fgookwnl对应flag，两个字母对应一个字母，后来无意中发现flag中的f到l和l到a都相隔7位，就以为所有的都是往后找7个数，但到了flag中的g时，发现从a到g相隔7位（不算已经取出的f），但从g到{才隔着6位（除非算上取出的l才相隔7位），然后就以为前3此移位是7位，后面的移位都是6位，但这样取，}居然提前取出来了。然后他突然灵机一动，共21个字符，7移动了3次，然后移动6，3*7=21，即7三次，6三次，一直到1三次（虽然最后发现1只有两次，因为21个字符有20个间隔）

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/c0c9bfe90ba44d19978350286f1294f7/2b8e70929ed9b5b984b0858b91455a59.jpg)



## **第七道▼古典密码签到**

先base32，根据提示得到^pho^oav\`\ntZnj\`\ntZZZcccx

一点基础也没有，根本无从下手，中间想试试移位，但死活和flag对不上（忘了还有cumtctf这个格式）。最后想试试凯撒，但凯撒只能搞纯字母，过了一会，突然想到，可能是凯撒的思想，不一定在26个字符中移位，也可能在Z（ascll最小，为90）和x（ascll最大，为120）间移位。编了个程序，虽然最后发现有点小错误，但还是发现出现了cumtctf的字样，于是肯定思路没错，找错误吧。错误还没找到的，先发现了其实就是向后移动5位。。。重新编了个往后移5位的程序，答案就跑出来了

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/98646fde4ff148c08c8a9deb5cfbb8d5/clipboard.png)



进前十啦

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/8ee73bf3dc62415f9d0c4dc18378501b/clipboard.png)



![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/23868ee315134ca3960d7217d2e516b1/clipboard.png)

web的签到题是张龙做的哦



## **第八道▼起床改error啦！**

解压，得到一张图片

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/2593c63e7f26410c97403f3f65fb2344/2333.png)

按照提示，图文无关，拖进C32Asm

文件末尾出现了flag.doc的字样，怀疑是两个文件结合而来

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/ebe2b2bdca264c85995de2ed6e4aa32e/clipboard.png)

打开kali，将图片拖进虚拟机ctf文件夹

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/b5fdfd8f107b4ed5839d5f2e5080987a/clipboard.png)

将新生成的flag.doc拖回win10，居然打不开

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/60996828c2e74f129f551c127a4e4502/clipboard.png)

这时发现之前用binwalk时出现的Zip archive data这句话，百度一下，原来是种压缩方式

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/7006eaf721744450868c3a7988737f39/clipboard.png)

unzip解压这个doc

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/32dc5825ffcc499d89242b1023452bad/clipboard.png)

拖回win10，打开

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/b73deb10a9044ebcb93fdcd5a9f5cbe5/clipboard.png)

那就接着找吧。点击文件再点击选项

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/e99fd3ee1a90468c9417ad10b66802f2/clipboard.png)

然后点击显示，勾上隐藏文字

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/8724fe61a5594c46be5bd980c4514dc0/clipboard.png)

答案就出来了

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/1197ac55046f4e98812866eb6b81558e/clipboard.png)



## **第九道▼矿大校歌认真听听吧？**

一个带密码的压缩包，尝试1~6位数字暴力破解密码，没出来，拖进winhex（或C32Asm），最后一行写着cumtctf2019，猜测就是密码，果然。

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/94944fb5c5674bf2bb2050d84ba15971/clipboard.png)

里面只有一个cumt.mp3，是矿大校歌。打开听了，正常的校歌。

拖进audacity（在这个软件上耗费了我三个小时以上的时间，没想到这道题用不到这个软件）

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/772e30e98d154e83ad1e9a72ebbdf95d/clipboard.png)



![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/43303806b40f47bfab62f51bec235a74/clipboard.png)

频谱图也看不出来flag（最初怀疑过紫线和白线，放大后一点一点找，耗费了好几个小时，也听了好几个小时的校歌）

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/d5386ad7b73244f4ab4e044d41e94d12/clipboard.png)

关闭，打开kali，用binwalk分析

结果并不是多个文件的结合

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/633472e48cf84c0997e6b5b94cf1740e/clipboard.png)

回到win10，用MP3Stego试一下

双击MP3Stego目录下的mp3.bat（该文件作用是在cmd中进入MP3Stego目录），键入

decode -X -P cumtctf cumt.mp3 

-X是文件名

-P是密码

（至于为啥后面的参数的顺序是反着的我也不清楚）

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/2d513c1356384141b3df0c4ef380d706/clipboard.png)

生成了两个文件

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/6b78c0b791304d1485b532adbe34d2aa/clipboard.png)

打开cumt.mp3.txt，得到flag{cumtctf_1s_v3ry_g00d!}

（最初不知道密码，猜了个题目名，即cmut，结果提示错误，没想到cumtctf2019既是压缩包密码，又是MP3隐写的密码）

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/af545e0c86e64f2691e9ff2fab2cc3ff/clipboard.png)



## **第十题▼SimpleUpload签到**

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/f1a27dac42b44d0596fcf71777e287fa/clipboard.png)

只能上传图片，但要求是上传.php

使用burpsuite抓包再修改数据上传<https://www.sohu.com/a/236194259_658302>

安装了jdk后，我仍然无法打开burpsuite.jar，所以我将burpsuite.jar放入

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/daa25c8508f94d5ba3e78f26a1e3692f/clipboard.png)

打开cmd，键入java -jar burpsuite.jar，通过这样打开burpsuite，但弊端是每次都要输入一次，而且使用burpsuite过程中不能关闭输入命令的那个cmd窗口，否则burpsuite也会关闭。

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/b2146a250b454a7cb6ac22f5b15d3f02/clipboard.png)



![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/a2b76be559b447e9824240bf221f7117/clipboard.png)

依次点close（不更新），next，然后点start burp

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/c92632d0350a4f0fbc24c39a2bd4e454/clipboard.png)

打开360极速浏览器（chrome我还不会设置代理服务器），搜索“代理”

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/6bb35cdbea0d4c18a5a5edf7bc117156/clipboard.png)

点击代理服务器设置

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/e59b230fb05a41a58f7263a58d99ff49/clipboard.png)

在代理服务器列表中添加127.0.0.1:8080

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/0293dfaafd6c4c1da83744772805ab04/clipboard.png)

点击代理服务器，勾选127.0.0.1:8080

浏览器地址栏键入题目网址，发现打不开，那就先把上图的不使用代理服务器勾选，打开网页后再勾选127.0.0.1:8080

再桌面新建一个空白文件，文件名为1.php .png

注意php和.png之间有一个空格。

打开burpsuite，开启抓包（Intercept is on）

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/99481853a4da4f6bb6167ca507e37330/clipboard.png)

这时上传1.php .png

抓到包

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/d8c0fc9219f9408cb522f2e30bd90f91/clipboard.png)

点击Proxy中的Intercept中的Hex

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/c495c4d30af74b85a18c10d4dfdf60b0/clipboard.png)

找到1.php .png所在的一行

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/c9020bfe5ce34c0aa32523f00ec0b7a3/clipboard.png)

将20改为00（空格的hex是20）

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/18bece9bbd2848a88bb3fd296c645f79/clipboard.png)

原理是：提交的是.png，但服务器端读到00后就截断了，所以服务器端认为是.php

点击Forward，上传修改后的包

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/d30c3813fd9845da85b26fb863f93a82/clipboard.png)

得到flag

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/15f7d0612e04494384949beabeda02fe/clipboard.png)

（做出来后没几分钟，张龙告诉我他也做出来了，好像他是直接F12查看的代码，假期结束后再问问他）

（之前他说这道题有头绪了，我以为这100分到手了，没想到两天了他还不提交flag，我以为他懒得不做了，气的我现学了好几个小时，才搞到flag。不靠谱的男人(。・∀・)ノ）



## **第十一题▼**

参考了这个的第一题<https://www.cnblogs.com/baifan2618/p/7762666.html>

题目网址<http://bxs.cumt.edu.cn:30007/test/index.php>

（sqlmap的各种参数详见另一篇笔记）

打开kali的终端，键入

sqlmap -u http://bxs.cumt.edu.cn:30007/test/index.php?id=1 --dbs

结果如下图

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/6e69cf2ecc22450da83750835b7e6edc/2019-01-28%2016-32-34%20%E7%9A%84%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE.png)

得到可访问数据库

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/5423d7cc024847f19a32b9f54bf288c5/clipboard.png)

猜测flag在security中

sqlmap -u http://bxs.cumt.edu.cn:30007/test/index.php?id=1 --tables -D security

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/4c69d8d7088a45928a58a93b07a73e54/2019-01-28%2016-35-41%20%E7%9A%84%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE.png)

上下两图无缝衔接（太长了，截不到一起）

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/715968f8252e4028b489844be0c9dffc/2019-01-28%2016-37-51%20%E7%9A%84%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE.png)

看到flagishere就知道稳了

sqlmap -u http://bxs.cumt.edu.cn:30007/test/index.php?id=1 --columns -T flagishere -D security

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/db48dc74de6249d1aa27eb823c793ecf/2019-01-28%2016-40-36%20%E7%9A%84%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE.png)



![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/804975b8568940a2919072394bf6fbe3/2019-01-28%2016-40-52%20%E7%9A%84%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE.png)

我这个萌新还以为flag就是non-numeric呢，还以为要在网址后面加?id=numeric

都错了。接着键入

sqlmap -u http://bxs.cumt.edu.cn:30007/test/index.php?id=1 --dump -C flag -T flagishere -D security

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/de75a2ab15564061ae23f98774104209/2019-01-28%2016-44-07%20%E7%9A%84%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE.png)



![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/ce84194cedc84c1dab19b5dfa2bd3eb5/2019-01-28%2016-44-36%20%E7%9A%84%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE.png)

得到flag



最终成绩

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/65613fd8990c4e5990e619f4d8b01b61/clipboard.png)

![img](C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/95489666d9dc4625aba29b2952ff7daf/clipboard.png)

