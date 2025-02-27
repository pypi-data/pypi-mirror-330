# Copyright (c) PyBW
# Distributed under the terms of the MIT License.

import sys
import platform
from setuptools import setup, find_packages

is_win_64 = sys.platform.startswith('win') and platform.machine().endswith('64')
extra_link_args = ['-Wl,--allow-multiple-definition'] if is_win_64 else []

with open('README.md', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='pybw_comic',
    version='25.2.27.2',
    python_requires='>=3.6',
    
    author='Bowei Pu',
    author_email='pubowei@foxmail.com',
    
    description='comic spider',
    long_description=readme, 
    long_description_content_type='text/markdown',
    url='https://gitee.com/pubowei/comic',
    keywords=['comic', 'spider'],
    license='MIT',
    
    packages=find_packages(), 
    include_package_data=True, 
    
    scripts = [
        'pybw_comic/scripts/comic.py', 
        'pybw_comic/scripts/wnacg.py', 
    ], 
    
    entry_points = {
        'console_scripts': [
            'comic2pdf = pybw_comic.convert.image_to_pdf:main_concat',
            'comic2pdf2 = pybw_comic.convert.image_to_pdf:main',
            'wn = pybw_comic.scripts.wnacg:main',
        ]
    },

    project_urls={
        'Docs': 'https://gitee.com/pubowei/comic',
        'Package': 'https://pypi.org/project/pybw',
        'Repo': 'https://gitee.com/pubowei/comic',
    },


    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
)
