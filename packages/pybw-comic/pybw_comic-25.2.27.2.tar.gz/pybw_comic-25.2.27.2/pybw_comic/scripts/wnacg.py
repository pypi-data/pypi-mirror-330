# -*- coding: utf-8 -*-
"""
author: Bowei Pu at 2025.02.26
version: 2025.02.27

Download comic for wnacg.com website.
"""

import os, time, warnings
from pathlib import Path
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from pybw_comic.engines.copymanga import ImageDownloader


warnings.filterwarnings("ignore")


def parse_url(url):
    """
    """
    if 'index' in url:
        url_index = url
        url_slide = url.replace('index', 'slide')
    elif 'slide' in url:
        url_index = url.replace('slide', 'index')
        url_slide = url
    return url_index, url_slide


def init_driver_chrome(headless=False, image=False, if_return=True):
    """
    Copy from pybw_comic.engines.copymanga
    """
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


def download_one_mange(url):
    """
    """
    ## ------ Prepare ------
    url_index, url_slide = parse_url(url)
    
    opt = webdriver.EdgeOptions()
    opt.add_argument('--headless')
    
    d = webdriver.Edge(option=opt)

    d.get(url_index)

    # dire = d.title
    # dire = dire.replace(' - 紳士漫畫-專註分享漢化本子|邪惡漫畫', '')
    
    x_title = '/html/body/div[4]/h2'
    find = d.find_element(By.XPATH, x_title)
    
    dire = '{} {}'.format(time.strftime('%y%m%d_%H%M'), find.text)

    print('\nTitle: {}\n'.format(dire))
    os.makedirs(dire)
    
    
    d.get(url_slide)
    time.sleep(1)

    x_links = '/html/body/div[7]/div/img'
    finds = d.find_elements(By.XPATH, x_links)
    links = [i.get_property('src') for i in finds]

    d.close()
    
    ## ------ Program Begin ------
    for link in tqdm(links):
        name = Path(link).name
        ImageDownloader(link).download(r'{}/{}'.format(dire, name))
    return


def main():
    while True:
        print('\n{}'.format('-' * 50))
        url = input('\nInput url:\n>> ')
        download_one_mange(url)


if __name__ == '__main__':
    ## ------ user settings ------
    
    
    ## ------ Program Begin ------
    main()



