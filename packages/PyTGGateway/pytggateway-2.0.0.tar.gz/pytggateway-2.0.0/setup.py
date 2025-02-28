#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Sasivarnasarma
@contact: sasivarnasarma@protonmail.com
@license MIT License, see LICENSE file

Copyright (C) 2024
"""
from setuptools import setup, find_packages


VERSION = '2.0.0'

setup(
    name='PyTGGateway',
    version=VERSION,
    author='Sasivarnasarma',
    author_email='sasivarnasarma@protonmail.com',
    url='https://github.com/Sasivarnasarma/TGGateway',
    description='Telegram Gateway API Wrapper',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    download_url=f'https://github.com/Sasivarnasarma/TGGateway/archive/v{VERSION}.zip',
    license='MIT',
    packages=find_packages(),
    install_requires=['httpx'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
     python_requires='>=3.7',
)
