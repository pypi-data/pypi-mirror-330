# -*- coding: utf-8 -*-
"""
author: Bowei Pu at 2023.06.26
version: 2023.11.01

Comic spider for copymanga.

site url:
    https://www.copymanga.site/  (when vpn, may not able to download)
    https://www.copymanga.tv/  (for China mainland)
    
test url:
    https://www.copymanga.tv/comic/hydxjxrwgb
    https://www.copymanga.tv/comic/yisansancmdefengjing

"""

from pybw.core import *
import warnings
import zhconv
import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


warnings.filterwarnings("ignore")


Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}


_xpath_catelogue = {
    'book_name': '/html/body/main/div[1]/div/div[2]/ul/li[1]/h6',
    'author': '/html/body/main/div[1]/div/div[2]/ul/li[3]/span[2]/a',
    'state': '/html/body/main/div[1]/div/div[2]/ul/li[6]/span[2]',
    'topic': '/html/body/main/div[1]/div/div[2]/ul/li[7]/span[2]/a',
    'last_update': '/html/body/main/div[1]/div/div[2]/ul/li[5]/span[2]',

    'columns_Name': ['/html/body/main/div[2]/div[3]/span',
                     '/html/body/main/div[2]/div[3]/span[1]',
                     '/html/body/main/div[2]/div[3]/span[2]',
                    ],
    'columns': '/html/body/main/div[2]/div[3]/div/div[1]/ul/li/a',
    'chapters': {-1: '/html/body/main/div[2]/div[3]/div/div[2]/div/div/ul[1]/a',
                  0: '/html/body/main/div[2]/div[3]/div[1]/div[2]/div/div[1]/ul[1]/a',
                  1: '/html/body/main/div[2]/div[3]/div[1]/div[2]/div/div[2]/ul[1]/a',
                  2: '/html/body/main/div[2]/div[3]/div[1]/div[2]/div/div[3]/ul[1]/a',
                  3: '/html/body/main/div[2]/div[3]/div[1]/div[2]/div/div[4]/ul[1]/a',
                  4: '/html/body/main/div[2]/div[3]/div[2]/div[2]/div/div[1]/ul[1]/a',
                  5: '/html/body/main/div[2]/div[3]/div[2]/div[2]/div/div[2]/ul[1]/a',
                  6: '/html/body/main/div[2]/div[3]/div[2]/div[2]/div/div[3]/ul[1]/a',
                  7: '/html/body/main/div[2]/div[3]/div[2]/div[2]/div/div[4]/ul[1]/a',
                },  
}
_xpath_chapter = {
    'images': '/html/body/div[2]/div/ul/li/img',
    'comic_index': '/html/body/div[1]/span[1]',
    'comic_count': '/html/body/div[1]/span[2]',
}
dic_xpath = DictDoc()
dic_xpath.catelogue = DictDoc(_xpath_catelogue)
dic_xpath.chapter = DictDoc(_xpath_chapter)


def get_proxies(proxy_num=7890):
    if proxy_num:
        proxies = {'http': '127.0.0.1:{}'.format(proxy_num),
                   'https': '127.0.0.1:{}'.format(proxy_num)
                  }
    else:
        proxies = None
    return proxies


def init_driver_firefox(headless=False, image=True, if_return=True):
    opt = webdriver.FirefoxOptions()
    
    opt.add_argument('--ignore-certificate-errors')
    opt.add_argument('--disable-notifications')
    opt.add_argument("--disable-images")
    opt.add_argument('--log-level=3')
    
    if headless:
        opt.add_argument('-headless')
    if not image:
        opt.set_preference('permissions.default.image', 2)
    
    driver = webdriver.Firefox(options=opt)
    driver.set_page_load_timeout(60)
    
    if if_return:
        return driver
    else:
        # global driver
        return


def init_driver_chrome(headless=False, image=False, if_return=True):
    opt = webdriver.ChromeOptions()

    opt.add_argument('--ignore-certificate-errors')
    opt.add_argument('--disable-notifications')
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    opt.add_argument('--log-level=3')
    
    if headless:
        opt.add_argument('--headless')
    if not image:
        prefs = {'profile.managed_default_content_settings.images': 2}
        opt.add_experimental_option('prefs',prefs)

    driver = webdriver.Chrome(options=opt)
    driver.set_page_load_timeout(60)
    
    if if_return:
        return driver
    else:
        # global driver
        return


class CleanText():
    """
    """
    def __init__(self, text):
        self.text = text
        self.clean_text = self.get_clean_text(self.text)
        
    @classmethod
    def get_clean_text(cls, text):
        text = cls.strip_space(text)
        text = cls.to_CN(text)
        text = cls.merge_space(text)
        return text
    
    @classmethod
    def strip_space(cls, text):
        text = text.strip()
        return text
    
    @classmethod
    def to_CN(cls, text):
        text = zhconv.convert(text, 'zh-cn')
        return text
    
    @classmethod
    def merge_space(cls, text):
        text = re.sub(' +', ' ', text)
        return text


def find_empty_subdir(dire):
    if not os.path.isdir(dire):
        raise Exception('{} is not dir'.format(dire))
    subs = os.listdir(dire)
    subs = [Path(dire).joinpath(i) for i in subs]
    subs = [i for i in subs if os.path.isdir(i)]
    # empty_sub = [i for i in subs if not os.path.getsize(i)]
    empty_sub = [i for i in subs if not os.listdir(i)]
    empty_sub = [i.as_posix() for i in empty_sub]
    return empty_sub


class ImgDownloader():
    """
    """
    def __init__(self, url, url_referer='', proxy_num=None):
        self.url = url
        self.url_referer = url_referer if url_referer else ''
        
        self.proxies = get_proxies(proxy_num)
        
        self.file_origin = Path(self.url).name

    @classmethod
    def _generate_headers(cls, referer=''):
        if not referer:
            referer = ''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Referer': referer
        }
        return headers
        
    def download(self, file=''):
        file = file if file else self.file_origin
        headers = self._generate_headers(referer=self.url_referer)
        if self.proxies:
            req = requests.get(self.url, headers=headers, proxies=self.proxies)
        else:
            req = requests.get(self.url, headers=headers)
        with open(file, 'wb') as f:
            f.write(req.content)


class ImageDownloader():
    '''
    '''
    def __init__(self, url, url_from='', filetype='auto', proxy_num=7890):
        self.url = url
        self.url_from = url_from
        self.filetype = self._detect_filetype(self.url, filetype)
        
        self.proxies = get_proxies(proxy_num)

    @classmethod
    def _detect_filetype(cls, url, filetype='auto'):
        if filetype not in ['auto', 'detect']:
            return filetype
        if 'png' in url:
            return 'png'
        elif 'jpg' in url:
            return 'jpg'
        elif 'jpeg' in url:
            return 'jpeg'
        else:
            return 'jpg'

    @classmethod
    def _headers(cls, referer):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Referer': referer}
        return headers
    
    def download(self, filename):
        if not Path(filename).suffix:
            filename = filename + '.' + self._detect_filetype(self.url)
        headers = self._headers(self.url_from)
        req = requests.get(self.url, headers=headers, proxies=self.proxies)
        content = req.content
        with open(filename, 'wb') as f:
            f.write(content)
        return


class Catelogue():
    """
    Note:
        动态页面，需要加载，无法使用requests
    """
    def __init__(self, url='', headless=False, driver_img=False, sleep=1,
                 proxy_num=7890):
        if not url:
            url = 'https://www.copymanga.tv/comic/hydxjxrwgb'
        
        self.url = url
        self.headless = headless
        self.driver_img = driver_img
        self.sleep = sleep
        
        self.proxies = get_proxies(proxy_num)
        
        # self.url_prefix = '//'.join(Path(url).parts[:2])
        self.url_prefix = re.findall('(.+copymanga.+?)\/', self.url) \
                          + re.findall('(.+mangacopy.+?)\/', self.url)
        self.url_prefix = self.url_prefix[0]
        
        self.book_info = self.get_comic_info()
        for i in self.book_info.__dict__.keys():
            if i != 'dic':
                setattr(self, i, self.book_info.__dict__[i])
        
        self.driver = init_driver_chrome(self.headless, self.driver_img)
        
        self.chapters = self.get_chapters()
        self.chapter_amount = len(self.chapters)

    def __repr__(self):
        return '< Catelogue | {} >'.format(self.book_name)
    
    def close(self):
        self.driver.close()
    
    def close_driver(self):
        self.driver.close()
    
    def get_comic_info(self):
        if self.proxies:
            req = requests.get(self.url, headers=Headers, proxies=get_proxies())
        else:
            req = requests.get(self.url, headers=Headers)
        bs = BeautifulSoup(req.text, 'lxml')
        tree = etree.HTML(req.text)
        
        info = DictDoc()
        
        name = tree.xpath(dic_xpath.catelogue.book_name)
        info.book_name = CleanText(name[0].text).clean_text if name else ''
        
        author = tree.xpath(dic_xpath.catelogue.author)
        if not author:
            author = ''
        else:
            author = [CleanText(i.text).clean_text for i in author]
            author = ' '.join(author)
        info.author = author
        
        state = tree.xpath(dic_xpath.catelogue.state)
        if not state:
            state = '连载'
        else:
            state = CleanText(state[0].text).clean_text
        info.book_state = '完结' if '完结' in state else '连载'
        
        topic = tree.xpath(dic_xpath.catelogue.topic)
        if not topic:
            topic = ''
        else:
            topic = [CleanText(i.text).clean_text for i in topic]
            topic = [i.strip('#') for i in topic]
            topic = ' '.join(topic)
        info.book_topic = topic
        
        last_update = tree.xpath(dic_xpath.catelogue.last_update)
        if not last_update:
            last_update = ''
        else:
            last_update = last_update[0].text
        info.last_update = last_update
        
        return info

    def get_chapters(self, sleep=None):
        if not sleep:
            sleep = self.sleep
        self.driver.get(self.url)
        time.sleep(1)
        
        c_Names = self.driver.find_elements(By.XPATH, dic_xpath.catelogue.columns_Name[0])
        c_Names = [i.text for i in c_Names]
        
        # finds = self.driver.find_elements(By.CLASS_NAME, 'nav-item')
        finds = self.driver.find_elements(By.XPATH, dic_xpath.catelogue.columns)
        
        ## [Todo] 2023.06.28 parse the second column, currently only parser finds[:4]
        # finds = finds[:4]
        
        columns_index = {i: CleanText(find.text).clean_text 
                         for i, find in enumerate(finds)}
        
        '''
        ## Clean finds: [1] ignore column "全部"
        ##              [2] ignore column that cannot click
        finds = [find for find in finds[1:] 
                 if find.get_attribute('class') != 'nav-link disabled']
        columns_index = {i: CleanText(find.text).clean_text 
                         for i, find in enumerate(finds)}
        '''
        
        finds = [i for i in finds 
                 if i.get_attribute('class') != 'nav-link disabled']
        
        chapters = {}
        for i, column in enumerate(finds):
            if i == 0:
                pass
                # continue
            if column.get_attribute('class') == 'nav-link disabled':
                continue
            
            # c_Name = 'c1' + c_Names[0] if i <=3 else 'c2' + c_Names[1]
            # c_Name = CleanText(c_Name).clean_text
            c_Name = 'c1' if i <=3 else 'c2'
            
            column_name = CleanText(column.text).clean_text
            # column_name = '{}_{}'.format(c_Name, column_name)
            column_name = c_Name + column_name
            
            column.click()
            time.sleep(sleep)
            
            engine = 'lxml'
            if engine == 'selenium':
                chap_eles = self.driver.find_elements(By.XPATH, 
                    dic_xpath.catelogue.chapters[i])
                chapters[column_name] = [
                    {'text': CleanText(ele.text).clean_text,
                     'title': CleanText(ele.get_attribute('title')).clean_text,
                     'url': ele.get_attribute('href')
                    }
                    for ele in chap_eles
                ]
            elif engine in ['lxml', 'etree']:
                tree = etree.HTML(self.driver.page_source)
                chap_eles = tree.xpath(dic_xpath.catelogue.chapters[i])
                chapters[column_name] = [
                    {'text': CleanText(ele.find('li').text).clean_text,
                     'title': CleanText(ele.get('title')).clean_text,
                     'url': self.url_prefix + ele.get('href')
                    }
                    for ele in chap_eles
                ]
        return chapters


class Chapter():
    """
    """
    def __init__(self, url='', headless=False, driver_img=False):
        if not url:
            url = 'https://www.copymanga.tv/comic/hydxjxrwgb/chapter/f8c2a2a3-c608-11e8-879b-024352452ce0'
        
        self.url = url
        self.headless = headless
        self.driver_img = driver_img
        
        # self.url_prefix = '//'.join(Path(url).parts[:2])
        # self.url_prefix = re.findall('(.+copymanga.+?)\/', self.url)[0]
        self.url_prefix = re.findall('(.+copymanga.+?)\/', self.url) \
                          + re.findall('(.+mangacopy.+?)\/', self.url)
        self.url_prefix = self.url_prefix[0]
        
        '''
        self.chapter_info = self.get_chapter_info()
        for i in self.book_info.__dict__.keys():
            if i != 'dic':
                setattr(self, i, self.book_info.__dict__[i])
        '''
        
        self.driver = init_driver_chrome(self.headless, self.driver_img)
        
        self.images = self.get_images()
        loading = any(['loading.jpg' in i for i in self.images])
        while loading:
            self.images = self.get_images(refresh=False)
            loading = any(['loading.jpg' in i for i in self.images])
            time.sleep(1)
    
    def __repr__(self):
        return '< Chapter | {} >'.format(self.url)
    
    def close(self):
        self.driver.close()
    
    def close_driver(self):
        self.driver.close() 
    
    def get_chapter_info(self):
        pass
    
    def get_images(self, refresh=True):
        if refresh:
            self.driver.get(self.url)
        time.sleep(1)
        
        action = ActionChains(self.driver)
        idx, count = 1, 100
        action.send_keys(Keys.HOME).perform()
        while idx < count:
            # action.send_keys(Keys.PAGE_UP).perform()
            # action.send_keys(Keys.PAGE_DOWN).perform()
            # action.send_keys(Keys.END).perform()
            # action.send_keys(Keys.HOME).perform()
            action.send_keys(Keys.PAGE_DOWN).perform()
            
            idx = self.driver.find_element(By.XPATH, 
                dic_xpath.chapter.comic_index)
            count = self.driver.find_element(By.XPATH, 
                dic_xpath.chapter.comic_count)
            idx, count = int(idx.text), int(count.text)
            # ran_num = random.random() * 0.5
            # time.sleep(ran_num if ran_num >= 0.1 else 0.1)
            time.sleep(0.1)
        time.sleep(1)
        
        image_eles = self.driver.find_elements(By.XPATH, 
            dic_xpath.chapter.images)
        images = [i.get_attribute('src') for i in image_eles]
        return images


class Book():
    def __init__(self, url='', dire='', headless=False, driver_img=True,
                 proxy_num=None):
        url_text = 'https://www.copymanga.tv/comic/hydxjxrwgb'
        self.url = url if url else url_test
        # self.dire = dire
        self.headless = headless
        self.driver_img = True
        
        self.proxy_num = proxy_num
        self.proxies = get_proxies(proxy_num)
        
        self.website_label = 'copymanga'
        
        self.catelogue = Catelogue(self.url, headless=self.headless, 
                                   driver_img=False, sleep=1, 
                                   proxy_num=self.proxy_num)
        self.catelogue.driver.close()
        
        self.book_info_dict = self.catelogue.book_info.dict
        for i in self.book_info_dict.keys():
            setattr(self, i, self.book_info_dict[i])
        
        self.continue_state = {'continue': False, 'delete_last_dir': False}
        self._parse_input_continue(dire)
        self.dire = self._get_save_dire(dire)

        self.chapters = self.catelogue.chapters
        # self.chapter_amount = len(self.catelogue.chapters)
        self.chapter_amount = len([j for i in self.catelogue.chapters.keys()
                                     if not '全部' in i
                                     for j in self.catelogue.chapters[i]])

    def _parse_input_continue(self, text):
        text = text.strip()
        reg = '^(continue)[\s\-_]*(del$|delete$)?'
        reg = re.compile(reg)
        match = re.findall(reg, text)
        if match:
            self.continue_state['continue'] = True
            if match[0][1]:
                self.continue_state['delete_last_dir'] = True
        return
    
    def _get_save_dire(self, dire):
        time_label = time.strftime('%y%m%d_%H%M%S')
        dire = dire.strip()
        if self.continue_state['continue']:
            dirs = glob('*{}*'.format(self.book_name))
            dirs = [i for i in dirs if os.path.isdir(i)]
            if not dirs:
                dire = ''
            else:
                dire = dirs[-1]
                print('\nFind dir to continue: 【 {} 】\n'.format(dire))
                if self.continue_state['delete_last_dir']:
                    subdirs = os.listdir(dire)
                    subdirs.sort()
                    subdirs = [Path(dire).joinpath(i).as_posix() for i in subdirs]
                    subdirs = [i for i in subdirs if os.path.isdir(i)]
                    last_subdir = subdirs[-1]
                    print('--- Delete last subdir: {}\n'.format(last_subdir))
                    shutil.rmtree(last_subdir)      
        if not dire:
            dire = '{} {} [{}] [{}] [{}] [{}]'.format(
                time_label, self.catelogue.book_name, 
                self.author, self.book_topic, self.book_state, 
                self.website_label)
        return dire 
        
    def download(self, start_labels=[], mode=0):
        """
        Execute download the comic book.
        
        Args:
            start_labels: [Todo]
            mode: 0, 'not_all': don not download column "全部"
                  1, 'all': only download column "全部"
                  col_name (str): only download the given col_name
        """
        ## [Todo] start label. 2023.06.28 is not used
        
        print('\n{0}\nBookname | 《 {1} 》\n{0}\n'.format(
            '=' * 50, self.book_name))
        time_book0 = time.time()
        date_book0 = time.strftime('%F %T')
        
        if os.path.exists(self.dire):
            print('\nExist  dir: 【 {} 】\n'.format(self.dire))
        else:
            print('\nCreate dir: 【 {} 】\n'.format(self.dire))
            os.makedirs(self.dire, exist_ok=True)
        
        with open('{}/book_url.txt'.format(self.dire), 'w', encoding='utf-8') as f:
            f.write('{}\n'.format(self.url))
            f.write('{}\n'.format(self.catelogue.book_info.dict))

        ## ------ For start control [2022.09.21]
        if start_labels:
            start_ok = False
            start_labels = [CleanText(i).clean_text for i in start_labels]
        else:
            start_ok = True
        
        for col_idx, col_name in enumerate(self.catelogue.chapters.keys()):
            if mode in [0, '0', 'not_all']:
                if '全部' in col_name:
                    continue
            elif mode in [1, '1', 'all']:
                if not '全部' in col_name:
                    continue
            elif mode in self.catelogue.chapters.keys():
                if CleanText(col_name).clean_text != CleanText(mode).clean_text:
                    continue
            else:
                continue
            
            for i in start_labels:
                if col_name in i:
                    start_label = i
            chaps = self.catelogue.chapters[col_name]
            chap_amount = len(chaps)
            for chap_idx, chap in enumerate(chaps):
                chap_idx += 1
                time0 = time.time()
                
                chap_title = CleanText(chap['title']).clean_text
                chap_title = '{}_{} {}'.format(
                    col_name, str(chap_idx).zfill(3), chap_title)
                path_chap = Path(self.dire).joinpath(chap_title).as_posix()

                ## ------ For start control [2022.09.21]
                if not start_ok:
                    if start_label not in chap_title:
                        continue
                    else:
                        start_ok = True
                
                ## --- Judge if path_chap exist, and skip it
                if os.path.exists(path_chap):
                    _chap_imgs = os.listdir(path_chap)
                    if _chap_imgs:
                        continue
                else:
                    os.makedirs(path_chap)
                
                chap_url = chap['url']
                onechap = Chapter(chap_url, headless=self.headless,
                                  driver_img=self.driver_img)
                onechap.driver.close()
                images = onechap.images
                
                # print('\nDownloading [{0}/{1}]: {2}'.format(
                    # chap_idx, self.chapter_amount, chap_title))
                print('\nDownloading [{}] [{}/{}]: {}'.format(
                    col_name, chap_idx, chap_amount, chap_title))
                
                
                for i, img_url in enumerate(tqdm(images)):
                    file_prefix = 'page_{}-'.format(str(i+1).zfill(6))
                    file = Path(img_url).name
                    file = file_prefix + file
                    file_path = Path(path_chap).joinpath(file).as_posix()
                    if os.path.exists(file_path):
                        continue
                    
                    imgd = ImgDownloader(img_url, chap_url, self.proxy_num)
                    imgd.download(file_path)
                    time.sleep(0.5)
                    
                time_p = time_parser(time.time() - time0)
                time_m, time_s = time_p['min'], time_p['sec']
                print('      [ {} | {} | {:0>2}:{:0>2} ]'.format(
                    chap_title, time.strftime('%F %T'), time_m, time_s))
        
        time_book_p = time_parser(time.time() - time_book0)
        time_book_h = time_book_p['hour']
        time_book_m = time_book_p['min']
        time_book_s = time_book_p['sec']
        date_book2 = time.strftime('%F %T')
        print('\n      {0} Done | {1} {0}'.format('=' * 5, self.book_name))
        print(  '        start | {} '.format(date_book0))
        print(  '        done  | {} '.format(date_book2))
        print(  '        time  | {:0>2}:{:0>2}:{:0>2} \n'.format(
            time_book_h, time_book_m, time_book_s))
        
        empty_sub = find_empty_subdir(self.dire)
        if empty_sub:
            print('\n    ====== Caution !!! ======')
            print(  '      These subdir is empty:')
            for i in empty_sub:
                print('        {}'.format(i))
            print('\n      Please check and download it again!')
            print(  '      Book url: {}\n'.format(self.url)) 


class ChapterDownloader():
    """
    """
    def __init__(self, url, headless=True, driver_img=True):
        self.url = url
        self.headless = headless
        self.driver_img = driver_img
        
        self.chap = Chapter(self.url, self.headless, self.driver_img)
        self.chapter_info = self._get_chapter_info()
        self.chap.driver.close()
    
    def _get_chapter_info(self):
        ele = self.chap.driver.find_element(By.TAG_NAME, 'h4')
        title = CleanText(ele.text).clean_text
        title = title.replace('/', ' ')
        info = {'title': title}
        return info
    
    def download(self, dire='', sleep=0.5):
        if not dire:
            dire = self.chapter_info['title']
        if not os.path.exists(dire):
            os.makedirs(dire)
        
        for i, img_url in enumerate(tqdm(self.chap.images)):
            file = Path(img_url).name
            file = 'page_{}-{}'.format(str(i+1).zfill(3), file)
            file_path = Path(dire).joinpath(file).as_posix()
            img_d = ImgDownloader(img_url, self.url)
            img_d.download(file_path)
            time.sleep(sleep)












