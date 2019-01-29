# vim: set fileencoding=utf-8:

'''
  vinergy.util.util
  ~~~~~~~~~~~~~~~~~

  Handy tools for Vinergy.
'''

import mimetypes

import pygments.lexers
from pygments import formatters
from pygments import highlight
from pygments.lexers import guess_lexer

from .formatter import MyHTMLFormatter
from .filter import TabFilter

term_ua = ('wget', 'curl')

def guess_ext(code):
  '''Guess file ext with code'''
  lexer = guess_lexer(code)
  mime = lexer.mimetypes[0]
  ext = mimetypes.guess_extension(mime)[1:]
  return ext


def is_terminal(ua):
  '''Determine the given UA is of terminal or not'''
  ua = ua.lower()
  for tua in term_ua:
    if ua.find(tua) != -1:
      return True
  return False

def norm_filetype(syntax):
  """Normalize filetype"""
  try:
    lexer = pygments.lexers.get_lexer_by_name(syntax)
    return lexer.name.lower()
  except:
    return 'text only'

def render(code, formatter, syntax):
  '''Render code with pygments'''
  if not syntax:
    lexer = guess_lexer(code)
  else:
    syntax = syntax.lower()
  try:
    lexer = pygments.lexers.get_lexer_by_name(syntax)
  except:
    lexer = pygments.lexers.TextLexer()
  lexer.add_filter(TabFilter(tabsize=8))
  f = getattr(formatters, formatter)
  if f.__name__ == 'HtmlFormatter':
    f = MyHTMLFormatter
    newcode = highlight(code, lexer, f(style='manni', lineanchors='n',
                                       anchorlinenos=True,
                                       linenos='table', encoding='utf-8'))
  else:
    newcode = highlight(code, lexer, f())
  return newcode
