from post import Post
from chapter import Chapter
import re, os, time

def novel(file_path):
    post = Post()
    post.login()
    category_name = '女友'
    category_slug = 'gi'
    category_mid = post.category(category_name, category_slug)
    if category_mid:
        with open(file_path, 'r', encoding='utf-8') as f:
            txt = f.read()
        c = Chapter(file_path)
        c.change_format()
        chapters = c.find_chapters()
        for num, chapter in enumerate(chapters):
            post.send_text(chapter.title, chapter.content, category_mid)
            time.sleep(1)
            #间隔太短会导致后台文章的顺序出现问题
            print("%d/%d"%(num+1,len(chapters)))
        
if __name__ == '__main__':
    novel(r'D:\桌面\东哥\我的网恋女友.txt')