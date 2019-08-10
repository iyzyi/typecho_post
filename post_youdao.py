from post import Post
import re, time
from urllib.parse import unquote

def youdao(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()
    '''
    pic_iter = re.finditer(r'\!\[.*?\]\((file:///(.*?))\)', txt)
    for tag in pic_iter:
        pic_name = str(time.time()).replace('.','')+ '.png'
        pic_url = post.upload_pic(tag.group(2), pic_name)
        txt = txt.replace(tag.group(1), pic_url)
    '''
    pic_iter = re.finditer(r'\!\[.*?\]\((.*?)\)', txt)
    for tag in pic_iter:
        pic_path = unquote(tag.group(1))    #图片名称含有汉字时，有道云笔记采用url编码的方式来记录，所以解码找到对应的图片位置
        print(pic_path)
        pic_name = str(time.time()).replace('.','')+ '.png'
        pic_url = post.upload_pic(pic_path, pic_name)
        txt = txt.replace(tag.group(1), pic_url)
    return txt


if __name__ == '__main__':
    post = Post()
    post.login()
    category_name = 'CTF'
    category_slug = 'ctf'
    title = '第三次CTF双月赛'
    category_mid = post.category(category_name, category_slug)
    file_path = r'ctf3.md'
    text = youdao(file_path)
    if category_mid:
        post.send_text(title, text, category_mid)
        print('发送成功')