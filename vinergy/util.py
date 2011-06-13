#!/usr/bin/env python
# vim: set fileencoding=utf-8:
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: util.py
# @Date: 2011年06月11日 星期六 06时27分02秒

'''
  vinergy.util
  ~~~~~~~~~~~~

  Handy tools for Vinergy.
'''
__all__ = ['guess_ext',
           'is_termua',
           'new_name',
           'render',
           'response',
          ]

import web
import string
import random
import mimetypes
import pygments.lexers
from pygments import formatters
from pygments import highlight
from pygments.lexers import guess_lexer


def guess_ext(code):
  '''Guess file ext with code'''
  lexer = guess_lexer(code)
  mime = lexer.mimetypes[0]
  ext = mimetypes.guess_extension(mime)[1:]
  return ext

def is_termua(ua):
  '''Determine the given UA is of terminal or not'''
  ua = ua.lower()
  term_ua = ('wget', 'curl')
  for tua in term_ua:
    if ua.find(tua) != -1:
      return True
  return False

def new_name():
  '''Generate new code name'''
  name = ''
  symbols = string.letters + string.digits

  while len(name) < 5:
    n = random.randint(0, len(symbols)-1)
    name = name + symbols[n: n+1]
  return name

def render(code, formatter, syntax):
  '''Render code with pygments'''
  if not syntax:
    lexer = guess_lexer(code)
  syntax = syntax.lower()
  try:
    lexer = pygments.lexers.get_lexer_by_name(syntax)
  except:
    lexer = pygments.lexers.TextLexer()
  f = getattr(formatters, formatter)
  if f.__name__ == 'HtmlFormatter':
    newcode = highlight(code, lexer, f(full=True, style='manni', lineanchors='n',
                                       linenos='table', encoding='utf-8'))
  else:
    newcode = highlight(code, lexer, f())
  return newcode

def response(data, status='200 OK', headers=None):
  '''Return custom response'''
  if not headers:
    headers = {'Content-Type': 'text/plain'}
  response = web.webapi.HTTPError(status, headers, data)
  return response
