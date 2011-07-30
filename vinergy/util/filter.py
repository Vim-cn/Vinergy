#!/usr/bin/env python2
# vim: set fileencoding=utf-8:
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: filter.py
# @Date: 2011年07月21日 星期四 18时06分21秒

'''
  vinergy.util.filter
  ~~~~~~~~~~~~~~~~~~~~~~

  Custom Pygments Filter
'''
import re

from pygments.util import get_int_opt
from pygments.filter import Filter

class TabFilter(Filter):
  def __init__(self, **options):
    Filter.__init__(self, **options)
    self.tabsize = get_int_opt(options, 'tabsize', 4)
    self.repl = re.compile(r'^\t+')

  def sub(self, tabs):
    def substitution(match):
      return match.group(0).replace('\t', tabs)
    return substitution

  def filter(self, lexer, stream):
    tabs = ' ' * self.tabsize
    for ttype, value in stream:
      value = self.repl.sub(self.sub(tabs), value).expandtabs(1)
      yield ttype, value
