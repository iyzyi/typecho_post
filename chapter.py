import re
import codecs  
import chardet
import functools

class Object():
    title = ''
    content = ''
    number = -1

class Chapter():
    def __init__(self, file_path):
        with codecs.open(file_path, 'rb') as f:
            self.txt = f.read()
            encoding = chardet.detect(self.txt)['encoding']
            print(encoding)
            self.txt = self.txt.decode(encoding,'ignore')
        self.chapter_list = []

    def change_format(self):
        '''
        修改txt的文本格式为：
        1、段间距为一个\n
        2、首行缩进4空格
        '''
        self.txt = re.sub(r'\s*\n\s*','\n\n　　', self.txt)
        #段末空格+回车及段首空格(也包括只包含空格的空行)替换为两个回车加两个全角空格
        #全角空格是因为typecho是markdown，四个半角空格会使得形成代码块
        self.txt = re.sub(r'^\s*','　　', self.txt)
        self.txt = re.sub(r'\s*$', '', self.txt)
        #with open('changed.txt', 'w', encoding='utf-8') as f:
        #    f.write(self.txt)

    def cmp(self, a, b):
        return a.number > b.number

    def find_chapters(self):
        first_line = re.search(r'^　　\S*(第.+?[章节回集卷] \S*)\n\n', self.txt)    
        #注意此处的'　　'是两个全角空格，修改时若写成4个半角空格会出现意想不到的后果
        if first_line:
            last_content_begin = first_line.end()
            last_title = first_line.group(1)
        else:
            last_content_begin = 0
            last_title = '写在前面'
        title_iter = re.finditer(r'\n　　\S*(第.+?[章节回集卷] \S*)\n\n', self.txt)
        for count, title in enumerate(title_iter):
            last_content_end = title.start()-1    #-1是为了去掉尾端的\n
            obj = Object()
            obj.title = last_title
            obj.content = self.txt[last_content_begin:last_content_end]
            obj.number = count
            self.chapter_list.append(obj)

            last_content_begin = title.end()
            last_title = title.group(1)
        obj = Object()
        obj.title = last_title
        obj.content = self.txt[last_content_begin:]
        obj.number = 0x3f3f3f3f    #最后一章的count赋‘无穷大’值
        self.chapter_list.append(obj)
        return sorted(self.chapter_list, key=functools.cmp_to_key(self.cmp))
 

if __name__ == '__main__':
    c = Chapter('大说访谈录.txt')
    c.change_format()
    chapters = c.find_chapters()
    for i in chapters:
        with open('233.txt', 'a+', encoding='utf-8') as f:
            f.write(i.title+'\n2333\n')
            f.write(i.content+'\n2333\n')
            #f.write(str(i.number))
        print(i.content)