# -*- coding: utf-8 -*-
"""
author: Bowei Pu at 2025.02.26
version: 2025.02.27

Download comic for wnacg.com website.
"""

import os, time, warnings, re
from pathlib import Path
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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


def download_one_mange(url, headless=True):
    """
    """
    ## ------ Prepare ------
    url_index, url_slide = parse_url(url)
    
    opt = webdriver.EdgeOptions()
    
    opt.add_argument('--ignore-certificate-errors')
    opt.add_argument('--disable-notifications')
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    opt.add_argument('--log-level=3')
    
    if headless:
        opt.add_argument('--headless')
        
    d = webdriver.Edge(options=opt)

    d.get(url_index)
    
    x_title = '/html/body/div[4]/h2'
    find = d.find_element(By.XPATH, x_title)
    title = find.text
    
    x_page = '/html/body/div[4]/div/div[2]/label[2]'
    find = d.find_element(By.XPATH, x_page)
    total_page = find.text
    total_page = int(re.findall('(\d+)P', total_page)[0])
    
    dire = '{} [{}P] {}'.format(time.strftime('%y%m%d_%H%M'), total_page, title)

    print('\nTitle: {}'.format(dire))
    
    print('\nTotal page: {} P'.format(total_page))
    
    os.makedirs(dire)
    
    ## --- get image links
    d.get(url_slide)
    
    x_progress = '/html/body/div[7]/div/span'
    while True:
        finds = d.find_elements(By.XPATH, x_progress)
        progress = re.findall('(\d+)\/(\d+)', finds[-1].text)
        progress = [int(i) for i in progress[0]]
        
        if progress[0] == progress[1]:
            break
        else:
            action = ActionChains(d)
            action.send_keys(Keys.HOME).perform()
            time.sleep(1)
            action.send_keys(Keys.END).perform()
            time.sleep(10)

    x_links = '/html/body/div[7]/div/img'
    finds = d.find_elements(By.XPATH, x_links)
    links = [i.get_property('src') for i in finds]
    
    print('\nFind image: {} P'.format(len(links)))
    print()
    
    with open('{}/url.txt'.format(dire), 'w', encoding='utf-8') as f:
        f.write('index: {}\n'.format(url_index))
        f.write('slide: {}\n'.format(url_slide))
    
    file = '{}/{}.txt'.format(dire, title)
    with open(file, 'w', encoding='utf-8') as f:
        for i in links:
            f.write(i + '\n')

    d.close()
    
    ## ------ Program Begin ------
    width = len(str(len(links)))
    for i, link in enumerate(tqdm(links)):
        name = '{}-{}'.format(str(i).zfill(width), Path(link).name)
        ImageDownloader(link).download(r'{}/{}'.format(dire, name))
    return


def main():
    while True:
        print('\n\n{}'.format('-' * 50))
        print('(To turn off headless option, add \'noheadless\' in url)')
        print('\nInput url:')
        url = input('>> ')
        
        if 'noheadless' in url:
            headless = False
            url = url.replace('noheadless', '')
        else:
            headless = True
        
        url = url.strip()
        
        if url.lower() in ['exit', 'quit', 'close']:
            os.sys.exit()
        
        if not url or 'wnacg' not in url:
            continue
        
        download_one_mange(url, headless)


if __name__ == '__main__':
    ## ------ user settings ------
    
    
    ## ------ Program Begin ------
    main()



