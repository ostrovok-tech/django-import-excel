#!/usr/bin/env python
#coding:utf-8
from distutils.core import setup
import sys

reload(sys).setdefaultencoding("UTF-8")


setup(
    name='django-import-excel',
    version='0.0.0',
    author='Ostrovok.ru',
    author_email='satels@gmail.com',
    packages=['import_excel',],
    url='http://satels.blogspot.com/',
    download_url = 'https://github.com/ostrovok-team/django-import-excel/zipball/master',
    license = 'MIT license',
    description = u'App for import excel files'.encode('utf8'),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: Russian',
    ),
    install_requires=['xlrd==0.7.1']
)

