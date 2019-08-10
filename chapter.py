import re
import codecs  
import chardet
import functools

class Object():
    title = ''
    content = ''
    number = -1    #number为chapter的起始位置下标

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
        if a.number < b.number:
            return -1
        if a.number > b.number:
            return 1
        return 0


    def add_chapters(self, title_iter):
        for title in title_iter:
            self.last_content_end = title.start()-1    #-1是为了去掉尾端的\n
            obj = Object()
            obj.title = self.last_title
            obj.content = self.txt[self.last_content_begin:self.last_content_end]
            obj.number = self.last_title_begin
            self.chapter_list.append(obj)

            self.last_title = title.group(1)
            self.last_title_begin = title.start()
            self.last_content_begin = title.end()


    def find_chapters(self):
        first_line = re.search(r'^　　\S*(第.+?[章节回集卷] \S*)\n\n', self.txt)    
        #注意此处的'　　'是两个全角空格，修改时若写成4个半角空格会出现意想不到的后果
        #first_line = re.search(r'^　　(风过暖城卷末感言)', self.txt)
        if first_line:
            self.last_title = first_line.group(1)
            self.last_title_begin = first_line.start()
            self.last_content_begin = first_line.end()
        else:
            self.last_title = '写在前面'
            self.last_title_begin = 0
            self.last_content_begin = 0

        title_iter = re.finditer(r'\n　　\S*(第.+?[章节回集卷] \S*)\n\n', self.txt)
        self.add_chapters(title_iter)        
        title_iter2 = re.finditer(r'((五十万字小结)|(八十万字及二月全勤总结)|(推本书)|(最美的诗篇卷末感言)|(妹妹人设图)|(完结感言)|(大结局))\n', self.txt)
        self.add_chapters(title_iter2)

        obj = Object()
        obj.title = self.last_title
        obj.content = self.txt[self.last_content_begin:]
        obj.number = self.last_title_begin
        self.chapter_list.append(obj)
        return sorted(self.chapter_list, key=functools.cmp_to_key(self.cmp))
 

if __name__ == '__main__':
    c = Chapter('我的网恋女友.txt')
    c.change_format()
    chapters = c.find_chapters()
    for i in chapters:
        '''
        with open('233.txt', 'a+', encoding='utf-8') as f:
            f.write(i.title+'\n2333\n')
            f.write(i.content+'\n2333\n')
            #f.write(str(i.number))
        '''
        #print(i.number)
        print(i.title)