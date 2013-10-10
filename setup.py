#!/usr/bin/env python
# vim:fileencoding=utf-8

from setuptools import setup, find_packages
import vinergy

with open('README.rst') as file:
  long_description = file.read()

setup(
  name = 'Vinergy',
  version = vinergy.__version__,
  entry_points = {
    'console_scripts': [
      'vinergy = vinergy.vinergy:main',
    ],
  },
  description = 'Vinergy - CLI Pastebin within VimEnergy',
  long_description = long_description,
  author = 'Vayn & lilydjwg',
  author_email = 'vayn@vayn.de & lilydjwg@gmail.com',
  url = 'http://p.vim-cn.com',
  download_url = 'https://github.com/Vim-cn/vinergy',
  license = 'GPL3',
  install_requires = ['tornado>=3.1', 'pymongo', 'pygments'],
  packages = find_packages(),
  classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL) ',
    'Programming Language :: Python',
    'Programming Language :: Python 2.7',
    'Programming Language :: Python 3',
    'Programming Language :: Python 3.3',
    'Topic :: Internet',
  ],
)
