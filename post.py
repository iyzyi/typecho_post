'''
需要对typecho的/var/Widget/Security.php改动一处地方(修改token)：
public function execute()
{
    $this->_options = $this->widget('Widget_Options');
    $user = $this->widget('Widget_User');

    $this->_token = $this->_options->secret;
    if ($user->hasLogin()) {
        $this->_token .= '&' . $user->authCode . '&' . $user->uid;
    }
->> $this->_token = "I need to change part of token for up files easy by python.";
}s
添加->>处所在的那一行

对token的说明：
token由两部分组成，以&连接，再取MD5，前半段不是固定的，我读源代码没读懂，所以改成了
'I need to change part of token for up files easy by python.'
后半段是固定的网址，就是referer。
登录admin的token
MD5前：I need to change part of token for up files easy by python.&http://yjd.fatiger.cn/admin/login.php?referer=http%3A%2F%2Fyjd.fatiger.cn%2Fadmin%2F
MD5后：be45360f1a19e7e1defca0f4d836b7cf
发布文章的token
MD5前：I need to change part of token for up files easy by python.&http://yjd.fatiger.cn/admin/write-post.php
MD5后：b4af7d3e443a7a19067a1479dedf0a70
'''

import re, copy, requests

def md5(string):
    import hashlib
    m = hashlib.md5()
    m.update(bytes(string, 'utf-8'))
    return str(m.hexdigest()).lower()

def url_encode(string):
    from urllib.parse import quote
    return quote(string, 'utf-8')

class Post():

    base_url = 'http://iyzy.xyz'
    #base_url = 'http://yjd.fatiger.cn'
    first_half_token = 'I need to change part of token for up files easy by python.&'
    session = requests.Session()
    session_login = requests.Session()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    proxies = {'http':'127.0.0.1:8080','https': '127.0.0.1:8080'}    #burpsuite抓包

    def login(self):
        second_half_token = '{}/admin/login.php?referer={}%2Fadmin%2F'.format(self.base_url, url_encode(self.base_url))
        token = md5(self.first_half_token + second_half_token)
        url = self.base_url + '/index.php/action/login?_=%s' % token
        data = {
            'name': 'admin',
            'password': 'DdhjX520',
            'referer': '{}%2Fadmin%2F'.format(url_encode(self.base_url))
            }
        headers = {
            'User-Agent': self.user_agent,
            'Referer': second_half_token,
            }
        r = self.session.post(url, data, headers=headers)
        self.session_login = copy.deepcopy(self.session)
        #print(self.session.cookies.get_dict())


    def search_category_mid(self, name):
        url = '%s/admin/manage-categories.php'%self.base_url
        headers = {'User-Agent': self.user_agent}
        r = self.session.get(url, headers=headers)
        self.session = copy.deepcopy(self.session_login)
        html = r.content.decode('utf-8')
        #with open('22222.html','w',encoding='utf-8') as f:
        #    f.write(html)
        tag_list = re.findall(r'\<a href="%s/admin/category\.php\?mid\=(\d+?)">(.+?)\</a>' % (self.base_url.replace('.','\.')), html)
        #tag_list = re.findall(r'\<a href="http://yjd\.fatiger\.cn/admin/category\.php\?mid\=(\d+?)">(.+?)\</a>', html)
        for tag in tag_list:
            if tag[1] == name:
                #print(self.session.cookies.get_dict())
                return tag[0]    #mid


    def make_category(self, name, slug, description): 
        second_half_token = '%s/admin/category.php' % self.base_url
        token = md5(self.first_half_token + second_half_token)
        url = self.base_url + '/index.php/action/metas-category-edit?_=%s' % token
        data = {
            'name': name,
            'slug': slug,
            'parent': '0',
            'description': description,
            'do': 'insert',
            'mid': ''
            }
        headers = {
            'User-Agent': self.user_agent,
            'Referer': second_half_token,
            }
        r = self.session.post(url, data, headers=headers)
        self.session = copy.deepcopy(self.session_login)
        if '缩略名已经存在' in r.content.decode('utf-8'):
            print('缩略名已经存在，请修改')
            return None
        else:
            mid = self.search_category_mid(name)
            if mid:
                return mid
            else:
                print('创建目录失败')


    def category(self, name, slug, description=''):   
        mid = self.search_category_mid(name)
        #print(mid)
        if mid:
            return mid
        else:
            return self.make_category(name, slug, description)
        #print(self.session.cookies.get_dict())


    def send_text(self, title, text, mid):
        second_half_token = '%s/admin/write-post.php' % self.base_url
        token = md5(self.first_half_token + second_half_token)
        url = self.base_url + '/index.php/action/contents-post-edit?_=%s' % token
        data = {
            'title': title,
            'text': text,
            'fields[thumbnail]': '',
            'fields[previewContent]': '',
            'cid': '',
            'do': 'publish',
            'markdown': '1',
            'date': '',
            'category[]': mid,
            'tags': '',
            'visibility': 'publish',
            'password': '',
            'allowComment': '1',
            'allowPing': '1',
            'allowFeed': '1',
            'trackback': '',
            'timezone': '28800'
            }
        headers = {
            'User-Agent': self.user_agent,
            'Referer': second_half_token,
            }
        r = self.session.post(url, data, headers=headers)
        self.session = copy.deepcopy(self.session_login)
        #print(self.session.cookies.get_dict())    #cookies


    def search_pic_url(self, name):
        url = '%s/admin/manage-medias.php'%self.base_url
        headers = {'User-Agent': self.user_agent}
        r = self.session.get(url, headers=headers)
        self.session = copy.deepcopy(self.session_login)
        html = r.content.decode('utf-8')
        tag_list = re.finditer(r'\<a href="(%s/admin/media\.php\?cid\=\d+)">(.+?)\</a>' % (self.base_url.replace('.','\.')), html)
        for tag in tag_list:
            if tag.group(2) == name:
                r = self.session.get(tag.group(1), headers=headers)
                self.session = copy.deepcopy(self.session_login)
                html = r.content.decode('utf-8')
                pic_url = re.search(r'\<img src\="(.+?)".+?/>', html)
                return pic_url.group(1)
                

    def upload_pic(self, pic_path, name):    
        '''
        name要带后缀，否则上传失败
        请保证图片不重名
        '''
        second_half_token = '%s/admin/write-post.php' % self.base_url
        token = md5(self.first_half_token + second_half_token)
        url = self.base_url + '/index.php/action/upload?_=%s' % token
        data = {'name': name}
        files = {'file': (name, open(pic_path, 'rb'))}
        headers = {
            'User-Agent': self.user_agent,
            'Referer': second_half_token,
            }
        r = self.session.post(url, data, files=files, headers=headers)
        self.session = copy.deepcopy(self.session_login)
        #print(r.content)

        if r:
            pic_url = self.search_pic_url(name)
            if pic_url:
                return pic_url
            else:
                print('上传%s失败'%pic_path)
        else:
            print('上传%s失败'%pic_path)


if __name__ == '__main__':
    category_name = '我的网恋女友2'
    category_slug = 'my_girlfriend2'    #若标签已存在，则此项（标签缩略名）忽略即可，只有创建新标签时才会用到
    title = 'PYTHON'
    text = 'hello'

    post = Post()
    post.login()
    category_mid = post.category(category_name, category_slug)
    if category_mid:
        post.send_text(title, text, category_mid)
        pic_url = post.upload_pic(r'C:/Users/kljxn/AppData/Local/YNote/data/kljxn@qq.com/670b0c7dc6434e6bb880818077326171/clipboard.png', 'dd.png')
        print(pic_url)