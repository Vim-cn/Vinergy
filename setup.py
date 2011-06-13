#!/usr/bin/env python
# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: setup.py
# @Date: 2011年06月06日 星期一 23时17分46秒

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup


with open('README.rst') as file:
  long_description = file.read()

config = {
  'name': 'Vinergy',
  'description': 'Vinergy - CLI Pastebin within VimEnergy',
  'long_description': long_description,
  'author': 'Vayn',
  'author_email': 'vayn@vayn.de',
  'url': 'http://p.vim-cn.com',
  'download_url': 'https://github.com/vayn/vinergy',
  'version': '0.2',
  'license': 'GPL3',
  'install_requires': ['nose', 'paste', 'web.py', 'pymongo', 'pygments'],
  'packages': ['vinergy'],
  'classifiers': [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL) ',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Topic :: Internet',
  ],
}

setup(**config)


