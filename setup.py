#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='floweaver-path',
    version='0.0.3',
    description='floweaver extension to handle the path visualization',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fullflu/floweaver-path',
    author='fullflu',
    author_email='k.takayama0902@gmail.com',
    license='MIT',
    install_requires=['floweaver', 'ipysankeywidget'],
    keywords='floweaver-path',
    include_package_data=True,
    package_dir={"": "src"},
    packages=["floweaver_path"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=['pytest'],
)
