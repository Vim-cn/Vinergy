#!/usr/bin/env python

from setuptools import setup, find_packages
import vinergy

with open('README.rst') as file:
  long_description = file.read()

setup(
  name = 'Vinergy',
  version = vinergy.__version__,
  entry_points = {
    'console_scripts': [
      'vinergy = vinergy.__main__:main',
    ],
  },
  description = 'Vinergy - CLI Pastebin within VimEnergy',
  long_description = long_description,
  author = 'Vayn & lilydjwg',
  author_email = 'vayn@vayn.de & lilydjwg@gmail.com',
  url = 'https://cfp.vim-cn.com/',
  download_url = 'https://github.com/Vim-cn/vinergy',
  license = 'GPL3',
  install_requires = ['tornado>=5', 'asyncpg', 'pygments'],
  packages = find_packages(),
  package_data = {'vinergy': ['static/*', 'templates/*']},
  exclude_package_data = {'vinergy': ['*~']},
  zip_safe = True,
  classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL) ',
    'Programming Language :: Python',
    'Programming Language :: Python 3',
    'Programming Language :: Python 3.7',
    'Topic :: Internet',
  ],
)
