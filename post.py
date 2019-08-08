import re, copy, requests

class Post():

    session = requests.Session()
    session_login = requests.Session()
    base_url = 'http://yjd.fatiger.cn'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    proxies = {'http':'127.0.0.1:8080','https': '127.0.0.1:8080'}    #burpsuite抓包

    def login(self):
        url = self.base_url + '/index.php/action/login?_=be45360f1a19e7e1defca0f4d836b7cf'
        data = {
            'name': 'user',
            'password': 'password',
            'referer': 'http%3A%2F%2Fyjd.fatiger.cn%2Fadmin%2F'
            }
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'http://yjd.fatiger.cn/admin/login.php?referer=http%3A%2F%2Fyjd.fatiger.cn%2Fadmin%2F',
            }
        r = self.session.post(url, data, headers=headers)
        self.session_login = copy.deepcopy(self.session)
        #print(self.session.cookies.get_dict())


    def search_category_mid(self, name):
        url = 'http://yjd.fatiger.cn/admin/manage-categories.php'
        headers = {'User-Agent': self.user_agent}
        r = self.session.get(url, headers=headers)
        self.session = copy.deepcopy(self.session_login)
        html = r.content.decode('utf-8')
        #with open('22222.html','w',encoding='utf-8') as f:
        #    f.write(html)
        tag_list = re.findall(r'\<a href="http://yjd\.fatiger\.cn/admin/category\.php\?mid\=(\d+?)">(.+?)\</a>', html)
        for tag in tag_list:
            if tag[1] == name:
                #print(self.session.cookies.get_dict())
                return tag[0]    #mid


    def make_category(self, name, slug, description):  
        url = self.base_url + '/index.php/action/metas-category-edit?_=caa33ebc320681da55d5f75f0fdce813'
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
            'Referer': 'http://yjd.fatiger.cn/admin/category.php',
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
        url = self.base_url + '/index.php/action/contents-post-edit?_=b4af7d3e443a7a19067a1479dedf0a70'
        data = {
            'title': title,
            'text': text,
            'fields%5Bthumbnail%5D': '',
            'fields%5BpreviewContent%5D': '',
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
            'Referer': 'http://yjd.fatiger.cn/admin/write-post.php',
            }
        r = self.session.post(url, data, headers=headers)
        #print(self.session.cookies.get_dict())    #cookies



if __name__ == '__main__':
    category_name = '我的网恋女友'
    category_slug = 'my_girlfriend'
    title = 'PYTHON'
    text = 'hello'

    post = Post()
    post.login()
    category_mid = post.category(category_name, category_slug)
    if category_mid:
        post.send_text(title, text, category_mid)