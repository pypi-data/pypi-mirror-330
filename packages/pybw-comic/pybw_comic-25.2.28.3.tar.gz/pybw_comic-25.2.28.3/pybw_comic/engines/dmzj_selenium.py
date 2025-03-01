# -*- coding: utf-8 -*-
"""
author: Bowei Pu
version: 2023.06.20

Comic spider for dmzj
"""

from pybw.core import *
import warnings
import zhconv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

warnings.filterwarnings("ignore")

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}


class DicDoc():
    def __init__(self, dic={}):
        self._dic = dic
        
        for k, v in self._dic.items():
            # self.k = v
            setattr(self, k, v)


def init_driver(headless=False, if_return=False):
    global driver
    
    opt = webdriver.FirefoxOptions()
    
    opt.add_argument('--ignore-certificate-errors')
    opt.add_argument('--disable-notifications')
    opt.add_argument("--disable-images")
    
    opt.set_preference('permissions.default.image', 2)
    
    if headless:
        opt.add_argument('-headless')
    
    driver = webdriver.Firefox(options=opt)
    if if_return:
        return driver
    else:
        return

def init_driver_old(headless=False):
    global driver
    opts = webdriver.ChromeOptions()
    
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    opts.add_argument('--ignore-certificate-errors')
    opts.add_argument('--disable-notifications')
    
    opts.headless = headless
    driver = webdriver.Chrome(options=opts)
    return


def get_dic_xpath():
    dic_xpath = {
                 'catelogue-booktopic': '/html/body/div[5]/div[3]/div/div[1]/div[2]/div/div[4]/table/tbody/tr[7]/td/a', 
                 'catelogue-bookstate': '/html/body/div[5]/div[3]/div/div[1]/div[2]/div/div[4]/table/tbody/tr[5]/td/a', 
                 'catelogue-bookname': '/html/body/div[5]/div[3]/div/div[1]/div[2]/div/div[4]/table/tbody/tr[1]/td',
                 'catelogue-chapters': '/html/body/div[5]/div[2]/div[1]/div[4]/ul/li[*]/a',
                 'catelogue-chapter-Property_text': 'text',
                 'catelogue-chapter-Property_title': 'title', 
                 'catelogue-chapter-Property_url_short': '', 
                 'catelogue-chapter-Property_url_full': 'href',
                 'onechapter-pages': '//*[@id="page_select"]/option', 
                 'onechapter-pages-Property_text': 'text', 
                 'onechapter-pages-Property_url_part': 'value', 
                 }
    return dic_xpath


def init_dic_xpath(dic=get_dic_xpath()):
    global dic_xpath
    dic_xpath = dic
    return


class DicXpath():
    '''
    '''
    def __init__(self, dic_xpath):
        self.dic_xpath = dic_xpath
        
        for k, v in dic_xpath.items():
            self.k = v


def time_parser(sec):
    total_sec = sec
    sec = int(total_sec % 60)
    total_min = total_sec // 60
    mins = int(total_min % 60)
    hour = int(total_min // 60)
    return hour, mins, sec


def find_empty_subdir(dire):
    if not os.path.isdir(dire):
        raise Exception('{} is not dir'.format(dire))
    subs = os.listdir(dire)
    subs = [Path(dire).joinpath(i) for i in subs]
    subs = [i for i in subs if os.path.isdir(i)]
    empty_sub = [i for i in subs if not os.path.getsize(i)]
    empty_sub = [i.as_posix() for i in empty_sub]
    return empty_sub



class Catelogue():
    def __init__(self, url='https://manhua.dmzj.com/engagekiss/'):
        self.url = url
        
        self.url_prefix = re.findall('.+com', self.url)[0]
        
        self.req = self.get_req()
        self.bs = BeautifulSoup(self.req.text, 'lxml')
        

        self.book_info = self.parse_comic_info()
        self.bookname = self.book_info.bookname
        self.author = self.book_info.author
        self.bookstate = self.book_info.bookstate
        self.booktopic = self.book_info.booktopic
        
        
        self.chapters = self.get_chapters()
        self.chapter_amount = len(self.chapters)
    
    def get_req(self):
        req = requests.get(self.url, headers=HEADERS)
        if not req.status_code == 200:
            raise Exception('requests status_code != 200, correct webpage '
                'is not obtained')
        return req
        
    def parse_comic_info(self):
        finds = self.bs.find_all('div', {'class': 'anim-main_list'})[0]
        l = finds.text.split()
        l = [i.replace('：', '') for i in l]
        text = ' '.join(l)
        
        info = DicDoc()
        
        # book_name = re.findall('别名 (\w*) ', text)
        author = re.findall('作者 (.*) 地域', text)
        book_state = re.findall('状态 (\w*) ', text)
        book_topic = re.findall('题材 (.*) 分类', text)
        
        # info.bookname = book_name[0] if book_name else ''
        info.author = author[0] if author else ''
        info.bookstate = book_state[0] if book_state else ''
        info.booktopic = book_topic[0] if book_topic else ''
        
        bookname = self.bs.find_all('h1')[0].text
        info.bookname = bookname
        
        return info
    
    def get_chapters(self):
        finds = self.bs.find_all('div', {'class': 'cartoon_online_border'})
        if not finds:
            raise Exception('Cannot find chapter div elements')
        finds = finds[0]
        
        list_chap = finds.find_all('a')
        chapters = {}
        chapters['text'] = [i.text for i in list_chap]
        chapters['title'] = [i.attrs['title'] for i in list_chap]
        chapters['url_short'] = [i.attrs['href'] for i in list_chap]
        chapters['url'] = [self.url_prefix + i.attrs['href']
                           for i in list_chap]
        zip_chapters = []
        for i in zip(chapters['text'], chapters['url'], 
                     chapters['title'], chapters['url_short']):
            zip_chapters.append(list(i))
        return zip_chapters
        

class Catelogue_selenium():
    '''
    '''
    def __init__(self, url='https://manhua.dmzj.com/engagekiss/'):
        self.url = url
        
        self.url_prefix = re.findall('.+com', self.url)[0]
        
        try:
            driver.get(self.url)
        except:
            time.sleep(1)
        time.sleep(1)
        self._click_to_enter_webpage()
        time.sleep(1)

        self.booktopic = self.get_booktopic()
        self.bookstate = self.get_bookstate()
        self.bookname = self.get_comic_bookname()
        
        self.chapters = self.get_chapters()
        self.chapter_amount = len(self.chapters)
    
    def _click_to_enter_webpage(self):
        try:
            time.sleep(1)
            _find = driver.find_element(By.XPATH, '/html/body/div[10]')
            _find.click()
            time.sleep(0.5)
        except:
            pass
        return
    
    def get_booktopic(self):
        # finds = driver.find_elements_by_xpath(dic_xpath['catelogue-booktopic'])
        finds = driver.find_elements(By.XPATH, dic_xpath['catelogue-booktopic'])
        if finds:
            find = finds[0]
            name = find.text
            name = zhconv.convert(name, 'zh-cn')
            name = name.strip().split(' ')[:3]
            name = ' '.join(name)
            return name
        else:
            return ''
            print('\nCannot find booktopic in webpage, please check xpath')
            print('Program exit ...\n')
            # sys.exit()
    
    def get_bookstate(self):
        finds = driver.find_elements(By.XPATH, dic_xpath['catelogue-bookstate'])
        if finds:
            find = finds[0]
            name = find.text
            name = zhconv.convert(name, 'zh-cn')
            if '完结' in name:
                return '完结'
            else:
                return '连载中'
        else:
            print('\nCannot find bookstate in webpage, please check xpath')
            print('Program exit ...\n')
            # sys.exit()
    
    def get_comic_bookname(self):
        finds = driver.find_elements(By.XPATH, dic_xpath['catelogue-bookname'])
        if finds:
            find = finds[0]
            name = find.text
            name = zhconv.convert(name, 'zh-cn')
            return name
        else:
            print('\nCannot find bookname in webpage, please check xpath')
            print('Program exit ...\n')
            # sys.exit()
    
    def get_chapters(self):
        # finds = driver.find_elements_by_xpath(dic_xpath['catelogue-chapters'])
        finds = driver.find_elements(By.XPATH, dic_xpath['catelogue-chapters'])
         
        chapters = {}
        chapters['text'] = [i.get_property(dic_xpath['catelogue-chapter-Property_text']).strip() for i in finds]
        chapters['title'] = [i.get_property(dic_xpath['catelogue-chapter-Property_title']).strip() for i in finds]
        chapters['url_short'] = [i.get_property(dic_xpath['catelogue-chapter-Property_url_short']) for i in finds]
        if dic_xpath['catelogue-chapter-Property_url_full']:
            chapters['url'] = [i.get_property(dic_xpath['catelogue-chapter-Property_url_full']) for i in finds]
        else:
            chapters['url'] = [self.url_prefix + i for i in chapters['url_short']]
        
        length = len(chapters['url'])
        zip_chapters = []
        for i in zip(chapters['text'], chapters['url'], chapters['title'], chapters['url_short']):
            zip_chapters.append(list(i))
        
        return zip_chapters
        

def driver_load_url(url):
    success = {'state': False, 
               'stop': 30, 
               'count': 0, 
               'sleep': 1, 
               'if_break': True, 
               'break': 1
               }
    while not success['state']:
        if success['break']:
            if success['count'] > success['break']:
                break
        if success['count'] > success['stop']:
            raise Exception('Cannot find pages')
        try:
            try:
                driver.get(url)
            except:
                time.sleep(1)
            success['state'] = True
        except:
            success['count'] += 1
            time.sleep(success['sleep'])
            if success['sleep'] < 5:
                success['sleep'] += 0.5
    return


class OneChapter():
    '''
    '''
    def __init__(self, url):
        self.url = url
        
        self.images = self.get_pages()

    def get_pages(self):
        self._driver_load_url(self.url)
        
        success = {'state': False, 'stop': 30, 'count': 0, 'sleep': 1}
        while not success['state']:
            if success['count'] > success['stop']:
                raise Exception('Cannot find pages')
            try:
                finds = driver.find_elements(By.XPATH, dic_xpath['onechapter-pages'])
                success['state'] = True
            except:
                success['count'] += 1
                time.sleep(success['sleep'])
        
        pages = {}
        pages['text'] = [i.get_property(dic_xpath['onechapter-pages-Property_text']).strip() for i in finds]
        pages['index_text'] = ['page_{}-{}'.format(str(i+1).zfill(6), text) for i, text in enumerate(pages['text'])]
        pages['url_part'] = [i.get_property(dic_xpath['onechapter-pages-Property_url_part']).strip() for i in finds]
        pages['url'] = ['https:' + i for i in pages['url_part']]

        zip_pages = []
        for i in zip(pages['index_text'], pages['url'], pages['text'], pages['url_part']):
            zip_pages.append(list(i))
        
        return zip_pages

    @classmethod
    def _driver_load_url(cls, url):
        success = {'state': False, 
                   'stop': 30, 
                   'count': 0, 
                   'sleep': 1, 
                   'if_break': True, 
                   'break': 1
                   }
        while not success['state']:
            if success['break']:
                if success['count'] > success['break']:
                    break
            if success['count'] > success['stop']:
                raise Exception('Cannot find pages')
            try:
                try:
                    driver.get(url)
                except:
                    time.sleep(1)
                success['state'] = True
            except:
                success['count'] += 1
                time.sleep(success['sleep'])
                if success['sleep'] < 5:
                    success['sleep'] += 0.5
        return


    ## Not used for DongManZhiJia, because this website directly gives every 
    ## image url in one page, no need to enter every page to get its image url
    @classmethod
    def get_image_url(cls, url, driver):
        '''
        Get image download url from page url
        '''
        # global driver
        try:
            driver.get(url)
        except:
            time.sleep(1)
        time.sleep(0.5)
        success = {'state': False, 'try': 1}
        while not success['state']:
            try:
                if success['try'] % 10 == 0:
                    try:
                        driver.get(url)
                    except:
                        time.sleep(1)
                    time.sleep(0.5)
                image = driver.find_elements(By.ID, 'cp_image')[0]
                success['state'] = True
            except:
                success['try'] += 1
                time.sleep(0.5)
        link = image.get_attribute('src')
        # driver.get(link)
        # image = driver.find_element_by_css_selector('img')
        return link


class ImageDownloader():
    '''
    '''
    def __init__(self, url, url_from, filetype='auto'):
        self.url = url
        self.url_from = url_from
        self.filetype = self._detect_filetype(self.url, filetype)

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
        req = requests.get(self.url, headers=headers)
        content = req.content
        with open(filename, 'wb') as f:
            f.write(content)
        return


class Book():
    '''
    '''
    def __init__(self, 
                 url='https://manhua.dmzj.com/engagekiss/', 
                 dire='', 
                 headless=False):
        self.url = url
        self._headless = headless
        
        self.website_label = 'dmzj'

        init_driver(headless=self._headless)
        init_dic_xpath()
        
        self.catelogue = Catelogue(self.url)
        self.booktopic = self.catelogue.booktopic
        self.bookstate = self.catelogue.bookstate
        self.bookname = self.catelogue.bookname
        
        self.continue_state = {'continue': False, 'delete_last_dir': False}
        self._parse_input_continue(dire)
        self.dire = self._get_save_dire(dire)

        self.chapters = self.catelogue.chapters
        self.chapter_amount = self.catelogue.chapter_amount

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
            dirs = glob('*{}*'.format(self.bookname))
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
            dire = '{} {} [{}] [{}] [{}]'.format(time_label, self.catelogue.bookname, self.booktopic, self.bookstate, self.website_label)
        return dire
    
    def download(self, start_label=''):
        print('\n{0}\nBookname | 《 {1} 》\n{0}\n'.format('='*50, self.bookname))
        time_book0 = time.time()
        date_book0 = time.strftime('%Y-%m-%d %T')
        
        if os.path.exists(self.dire):
            print('\nExist  dir: 【 {} 】\n'.format(self.dire))
        else:
            print('\nCreate dir: 【 {} 】\n'.format(self.dire))
            os.makedirs(self.dire, exist_ok=True)
        
        with open('{}/book_url.txt'.format(self.dire), 'w') as f:
            f.write('{}\n'.format(self.url))

        ## ------ For start control [2022.09.21]
        if start_label:
            start_ok = False
            start_label = zhconv.convert(start_label, 'zh-cn')
        else:
            start_ok = True

        # for chap_index, chapter in enumerate(tqdm(self.chapters)):
        for chap_index, chapter in enumerate(self.chapters):
            chap_index += 1
            time0 = time.time()
            
            chap_title = chapter[0]
            chap_title = zhconv.convert(chap_title, 'zh-cn')
            chap_title0 = chap_title
            chap_title = '{} {}'.format(str(chap_index).zfill(3), chap_title)
            path_chap = Path(self.dire).joinpath(chap_title).as_posix()

            ## ------ For start control [2022.09.21]
            if not start_ok:
                if start_label not in chap_title:
                    continue
                else:
                    start_ok = True

            chap_title_old = []
            chap_title_old.append(chap_title0)
            chap_title_old.append('chap_{} {}'.format(str(chap_index).zfill(3), chap_title0))
            path_chap_old = [Path(self.dire).joinpath(i).as_posix() for i in chap_title_old]
            
            if not os.path.exists(path_chap):
                _old_dir = False
                for i in path_chap_old:
                    if os.path.exists(i):
                        print('\n------ Skip info ------')
                        print('    For 【{}】'.format(path_chap))
                        print('    Find old version save dir 【{}】 '.format(i))
                        print('    Skip this chapter, please check if this is right\n')
                        _old_dir = True
                        break
                if _old_dir:
                    continue
                else:
                    os.makedirs(path_chap)
            else:
                continue
            
            chap_url = chapter[1]
            onechap = OneChapter(chap_url)
            images = onechap.images
            
            print('\nDownloading [{0}/{1}]: {2}'.format(chap_index, self.chapter_amount, chap_title))
            for i, image in enumerate(tqdm(images)):
            # for i, image in enumerate(images):
                i += 1
                
                filename = image[0]
                filename = 'page_{}'.format(str(i).zfill(6))
                file_path = Path(path_chap).joinpath(filename).as_posix()
                if os.path.exists(file_path):
                    continue
                
                url_d = image[1]
                
                imgd = ImageDownloader(url_d, chap_url)
                imgd.download(file_path)
                time.sleep(0.5)
        
            _, time_m, time_s = time_parser(time.time() - time0)
            
            print('      [ {} | {} | {:0>2}:{:0>2} ]'.format(chap_title, time.strftime('%Y-%m-%d %T'), time_m, time_s))
        
        time_book_h, time_book_m, time_book_s = time_parser(time.time() - time_book0)
        date_book2 = time.strftime('%Y-%m-%d %T')
        print('\n      {0} Done | {1} {0}'.format('='*5, self.bookname))
        print(  '        start | {} '.format(date_book0))
        print(  '        done  | {} '.format(date_book2))
        print(  '        time  | {:0>2}:{:0>2}:{:0>2} \n'.format(time_book_h, time_book_m, time_book_s))
        
        empty_sub = find_empty_subdir(self.dire)
        if empty_sub:
            print('\n    ====== Caution !!! ======')
            print(  '      These subdir is empty:')
            for i in empty_sub:
                print('        {}'.format(i))
            print('\n      Please check and download it again!')
            print(  '      Book url: {}\n'.format(self.url))


if __name__ == '__main__':
    ## ------ user settings ------
    read_inputs = True
    read_dire = True
    
    urls = [
            'https://manhua.dmzj.com/engagekiss/', 
           ]
    
    
    ## ------ Prepare ------
    if read_inputs:
        urls = []
        while True:
            inputs = input('url of catelogue: ')
            if inputs:
                urls.append(inputs.strip())
            else:
                break
    
    if read_dire:
        dire = input('\ndir to save the comic: ')

    # print('\n    (if start label, download will not start ')
    # print(  '     until a chapter title contain start label)')
    start_label = input('\nstart label (where to start): ')


    ## ------ Program Begin ------
    for url in urls:
        book = Book(url, dire=dire, headless=True)
        book.download(start_label)
        driver.close()

    