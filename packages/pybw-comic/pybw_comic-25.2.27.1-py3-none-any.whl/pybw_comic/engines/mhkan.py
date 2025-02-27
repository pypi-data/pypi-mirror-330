# -*- coding: utf-8 -*-
'''
'''
import os
import sys
import warnings
import time
import shutil
from glob import glob
from pathlib import Path
from tqdm import tqdm
import re
import random
import zhconv
from collections import OrderedDict
import requests
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

warnings.filterwarnings("ignore")

def init_driver(headless=False):
    # global driver
    opts = webdriver.ChromeOptions()
    
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    opts.add_argument('--ignore-certificate-errors')
    opts.add_argument('--disable-notifications')
    
    opts.headless = headless
    driver = webdriver.Chrome(options=opts)
    time.sleep(1)
    return driver


def get_dic_xpath():
    dic_xpath = {
                 'catelogue-chapters': '//*[@id="chapter-list-1"]/li/a', 
                 'catelogue-chapters_P_text': 'text', 
                 'catelogue-chapters_P_url_full': 'href', 
                 'catelogue-booktopic': '/html/body/div[4]/div[1]/div/div[2]/ol/li[5]/a', 
                 'catelogue-bookstate': '/html/body/div[4]/div[1]/div/div[3]/div[1]/div[1]/div[2]/ul/li[1]/span[1]/a', 
                 'catelogue-bookname': '/html/body/div[4]/div[1]/div/div[3]/div[1]/div[1]/div[2]/div[1]/h1/span', 
                 
                 'onechapter-pages': '/html/body/div[1]/div[4]/div/select/option', 
                 'onechapter-pages-Property_text': 'text', 
                 'onechapter-pages-Property_url_part': 'value', 
                 'onechapter-pages-Property_url_full': 'href', 

                 'onechapter-image': '//*[@id="images"]/img', 
                 'onechapter-image-Property_url': 'src'
                }
    return dic_xpath


def init_dic_xpath(dic=get_dic_xpath()):
    global dic_xpath
    dic_xpath = dic
    return

class CleanText():
    '''
    '''
    def __init__(self, text):
        self.text = text
        self.clean_text = self.get_clean_text(self.text)
        
    @classmethod
    def get_clean_text(cls, text):
        text = cls.to_CN(text)
        text = cls.clean_space(text)
        return text
        
    @classmethod
    def to_CN(cls, text):
        text = zhconv.convert(text, 'zh-cn')
        return text
    
    @classmethod
    def clean_space(cls, text):
        text = re.sub(' +', ' ', text)
        return text


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
    '''
    '''
    def __init__(self, url='https://www.mhkan.com/manhua/cheyezhige/', headless=False):
        '''
        彻夜之歌: https://www.mhkan.com/manhua/cheyezhige/
        '''
        self.url = url
        self._headless = headless
        
        self.driver = init_driver(self._headless)
        
        book_info = self.get_book_info()
        self.booktopic = book_info['booktopic']
        self.bookstate = book_info['bookstate']
        self.bookname = book_info['bookname']
        
        self.chapters = self.get_chapters()
        self.chapter_amount = len(self.chapters)
        
        self.driver.close()
        
    def get_book_info(self):
        self.driver.get(self.url)
        time.sleep(1)
        
        book_info = {}
        
        try:
            finds_topic = self.driver.find_elements(By.XPATH, dic_xpath['catelogue-booktopic'])
            topics = [i.text.strip() for i in finds_topic]
            topic = ' '.join(topics)
        except:
            topic = ''
        book_info['booktopic'] = topic
        
        finds_state = self.driver.find_elements(By.XPATH, dic_xpath['catelogue-bookstate'])
        state = finds_state[0].text.strip()
        if '完结' in state:
            state = '完结'
        else:
            state = '连载中'
        book_info['bookstate'] = state
        
        finds_title = self.driver.find_elements(By.XPATH, dic_xpath['catelogue-bookname'])
        title = finds_title[0].text.strip()
        book_info['bookname'] = title
        
        return book_info
    
    def get_chapters(self):
        self.driver.get(self.url)
        time.sleep(1)
        
        state = {'success': False, 'limit': 30, 'count': 0, 'sleep': 1}
        while not state['success'] and state['count'] <= state['limit']:
            try:
                finds = self.driver.find_elements(By.XPATH, dic_xpath['catelogue-chapters'])
                if finds:
                    state['success'] = True
            except:
                state['count'] += 1
                time.sleep(state['sleep'])
        
        chapters = []
        for i, find in enumerate(finds):
            i = str(i+1).zfill(3)
            text_i = find.text
            text_i = '{} {}'.format(i, text_i)
            url_i = find.get_property(dic_xpath['catelogue-chapters_P_url_full'])
            info_i = [text_i, url_i]
            chapters.append(info_i)
        
        return chapters


class OneChapter():
    '''
    '''
    def __init__(self, url='https://www.mhkan.com/manhua/cheyezhige/280036.html', headless=False):
        self.url = url
        self._headless = headless
        
        self.driver = init_driver(headless=self._headless)
        
        self._driver_load_url(self.driver, self.url)
        # self._click_webpage()
        
        self.image_url = self.get_image_url(self.driver)
        
        self.driver.close()
    
    def _click_webpage(self):
        to_click = {
                    'id': ['', 0],
                    }
        for k, v in to_click.items():
            try:
                if v and v[0]:
                    self._click_by_xpath(v[0], v[1])
            except:
                pass
        return
    
    def _click_by_xpath(self, pat_xpath, order=0):
        try:
            time.sleep(3)
            _finds = self.driver.find_elements(By.XPATH, pat_xpath)
            _find = _finds[order]
            _find.click()
            time.sleep(3)
        except:
            pass
        return

    def get_image_url(self, driver):
        success = {'state': False, 'stop': 30, 'count': 0, 'sleep': 0.5}
        while not success['state']:
            if success['count'] > success['stop']:
                raise Exception('Cannot find element')
            try:
                finds = driver.find_elements(By.XPATH, dic_xpath['onechapter-image'])
                find = finds[0]
                success['state'] = True
            except:
                success['count'] += 1
                time.sleep(success['sleep'])
        find = finds[0]
        img_url = find.get_property(dic_xpath['onechapter-image-Property_url'])
        return img_url
    
    def _get_index_end(self):
        finds = self.driver.find_elements(By.XPATH, '//*[@id="chapterpager"]/a')
        end = finds[-1].text
        end = int(end)
        return end
    
    def _next_page(self):
        ## Not used for manhuaDB, because some errors occur
        time.sleep(0.5)
        dic = {
               'next_page': '/html/body/div[2]/div[2]/nav/div/a'
              }
        success = {'state': False, 'stop': 10, 'count': 0, 'sleep': 0.5}
        while not success['state']:
            if success['count'] > success['stop']:
                raise Exception('Reach try limit, cannot find element')
            try:
                finds = self.driver.find_elements(By.XPATH, dic['next_page'])
                find = [i for i in finds if i.text.strip() == '下页'][0]
                find.click()
                success['state'] = True
            except:
                print('try: {}'.format(success['count']))
                success['count'] += 1
                time.sleep(success['sleep'])
        return
    
    def cal_images(self):
        driver = init_driver(headless=self._headless)
        
        self._driver_load_url(driver, self.url)
        # self._click_webpage()
        
        images_url = []
        
        pages = driver.find_elements(By.XPATH, dic_xpath['onechapter-pages'])
        pages_text = [i.text.strip() for i in pages]
        # print(pages_text)
        len_pages = int(len(pages))
        
        
        for i in range(len_pages):
            control = {'success': False, 'limit': 5, 'count': 0, 'sleep': 1}
            while not control['success'] and control['count'] <= control['limit']:
                try:
                    finds = driver.find_elements(By.XPATH, dic_xpath['onechapter-pages'])
                    find = finds[i]
                    if pages_text[i] != find.text.strip():
                        continue
                        # raise Exception('The element finded is not right')
                    find.click()
                    control['success'] = True
                except:
                    control['count'] += 1
                    time.sleep(control['sleep'])
            
            '''
            This sleep time is very important
            After test, 3.5 is good for manhuaDB
            3.5s reduce a little more than 50% errors than 3s and 2.5s
            3s and 2.5s have almost the same amount of errors
            '''
            time.sleep(1.5)
            count = 0
            while count <= 30:
                if i == 0:
                    time.sleep(3)
                    image_url_i = self.get_image_url(driver)
                    ## for code debug
                    # image_url_i = onechap.get_image_url()
                    break
                
                image_url_i = self.get_image_url(driver)
                ## for code debug
                # image_url_i = onechap.get_image_url(driver)
                
                temp_urls = images_url + [image_url_i]
                if image_url_i == images_url[-1] or len(temp_urls) != len(set(temp_urls)):
                    print('{} {} | count {}'.format(i+1, pages_text[i], count+1))
                    count += 1
                    time.sleep(1)
                    continue
                else:
                    break
            
            if not image_url_i:
                    break
            images_url.append(image_url_i)

        
        driver.close()
        
        if images_url[0] == images_url[1]:
            images_url = images_url[1:]
        if images_url[-1] == images_url[-2]:
            images_url = images_url[:-1]
        if len(images_url) != len(set(images_url)):
            raise Exception('images urls are repeate')
        
        zip_images = []
        for i, url_i in enumerate(images_url):
            i = str(i+1).zfill(6)
            zip_images.append(['page_{}'.format(i), url_i])
        self.images = zip_images
        return
    
    @classmethod
    def _driver_load_url(cls, driver, url):
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
                driver.get(url)
                success['state'] = True
                time.sleep(1)
            except:
                success['count'] += 1
                time.sleep(success['sleep'])
                if success['sleep'] < 5:
                    success['sleep'] += 0.5
        return


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
        elif 'webp' in url:
            return 'webp'
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
                 url='https://www.mhkan.com/manhua/cheyezhige/', 
                 dire='', 
                 headless=False):
        self.url = url
        self._headless = headless
        
        self.website_label = 'mhkan'

        # init_driver(headless=self._headless)
        init_dic_xpath()
        
        self.catelogue = Catelogue(self.url, self._headless)
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
                    last_subdir_name = Path(last_subdir).name
                    print('--- Delete last subdir: \" {} \"\n'.format(last_subdir_name))
                    shutil.rmtree(last_subdir)
                    
        if not dire:
            dire = dire = '{} {} [{}] [{}] [{}]'.format(time_label, self.catelogue.bookname, self.booktopic, self.bookstate, self.website_label)
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
            # chap_title = '{} {}'.format(str(chap_index).zfill(3), chap_title)
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
            onechap = OneChapter(chap_url, headless=self._headless)
            onechap.cal_images()
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
                time.sleep(1)
        
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
            'https://www.1kkk.com/manhua6123/', 
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
        dire = dire.strip()
    
    
    ## ------ Program Begin ------
    for url in urls:
        book = Book(url, dire=dire, headless=True)
        book.download()






