# -*- coding: utf-8 -*-
"""
author: Bowei Pu at 2022.07.10
version: 2023.06.28
function: Script for execute comic spider
"""

import os
import warnings
from glob import glob
from pathlib import Path

warnings.filterwarnings("ignore")


def read_url_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = [i.strip() for i in f.readlines()]
    content = [i for i in content if i]
    content = [[j.strip() for j in i.split(',')] for i in content]
    urls = [i[0] for i in content]
    return urls


def find_package_file(text, dire=''):
    """
    Not used
    """
    files = glob('{}/*{}*'.format(dire, text))
    file = files[-1]
    filename = Path(file).name
    return filename


def detect_repeat(dire):
    """
    (Not used in this scripts)
    (May useful elsewhere)
    
    Detect repeat files
    """
    if not os.path.isdir(dire):
        return
    files = os.listdir(dire)
    files = [Path(dire).joinpath(i).as_posix() for i in files]
    sizes = []
    for file in files:
        s = os.path.getsize(file)
        if s in sizes and s == sizes[-1]:
            return file
        sizes.append(s)
    return


def print_repeat(dire):
    """
    (Not used in this scripts)
    (May useful elsewhere)
    
    Detect repeat files
    """
    if not os.path.isdir(dire):
        return
    for d in os.listdir(dire):
        path_d = Path(dire).joinpath(d).as_posix()
        repeat = detect_repeat(path_d)
        if repeat:
            print(repeat)


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
            inputs = inputs.strip()
            if inputs:
                if os.path.exists(inputs):
                    urls = read_url_file(inputs)
                    print('\nRead urls from file 【{}】:'.format(inputs))
                    for i in urls:
                        print('    - {}'.format(i))
                    break
                urls.append(inputs)
            else:
                break
    urls = [i.strip() for i in urls]
    
    if read_dire:
        dire = input('\ndir to save the comic: ')
    
    # print('\n    (if start label, download will not start ')
    # print(  '     until a chapter title contain start label)')
    start_label = input('\nstart label (which chapter to start): ')
    
    headless = input('\ndriver headless (default Ture, any input False): ')
    headless = True if not headless.strip() else False
    
    proxy_num = input('\nproxy num (default None): ')
    proxy_num = int(proxy_num) if proxy_num else None
    
    print('\n{}\n'.format('-' * 50))
    
    ## ------ Program Begin ------
    for url in urls:
        
        if 'dmzj' in url:
            from pybw_comic.engines.dmzj_selenium import Book
        elif 'xmanhua' in url:
            from pybw_comic.engines.xmanhua import Book
        elif '1kkk' in url:
            from pybw_comic.engines.www_1kkk import Book
        elif 'manhuadb' in url:
            from pybw_comic.engines.manhuaDB import Book
        elif 'mhkan' in url:
            from pybw_comic.engines.mhkan import Book
        elif 'cnanjie' in url:
            from pybw_comic.engines.cnanjie import Book
        elif 'maofly' in url:
            from pybw_comic.engines.maofly import Book
        elif 'copymanga' in url or 'mangacopy' in url:
            from pybw_comic.engines.copymanga import Book
        else:
            raise Exception('\nPlease check url\n')

        
        book = Book(url, dire=dire, headless=headless, proxy_num=proxy_num)
        book.download(start_label)
