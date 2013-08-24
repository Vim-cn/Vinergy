#!/usr/bin/env python2
# vim: set fileencoding=utf-8:
# @Author: lilydjwg <lilydjwg@gmail.com>
# @Name: formatter.py
# @Date: 2011年 06月 16日 星期四 00:19:31 CST

'''
  vinergy.util.formatter
  ~~~~~~~~~~~~~~~~~~~~~~

  Custom HTMLFormatter
'''
import io
from pygments import formatters
from pygments.formatters import html


try:
  html._escape_html_table[ord(' ')] = u'&nbsp;'
except AttributeError: # pygments 1.3
  def escape_html(text):
    """Escape &, <, > as well as single and double quotes for HTML."""
    return text.replace('&', '&amp;').  \
                replace('<', '&lt;').   \
                replace('>', '&gt;').   \
                replace('"', '&quot;'). \
                replace("'", '&#39;').  \
                replace(" ", '&nbsp;')
  html.escape_html = escape_html
  del escape_html

class MyHTMLFormatter(formatters.HtmlFormatter):
  def wrap(self, source, outfile):
    return self._wrap_code(source)

  def _wrap_code(self, source):
    for i, t in source:
      yield i, t

  def _wrap_lineanchors(self, inner):
    i = 0
    counter = 0
    for i, t in inner:
      if i == 1:
        counter += 1
        yield 0, '<div id="n-%d" class="line">' % (counter)
        yield i, t[:-1] # strip line feed
        yield 0, '</div>\n'
      else:
        yield i, t

  def _wrap_tablelinenos(self, inner):
    dummyoutfile = io.StringIO()
    lncount = 0
    for t, line in inner:
      if t:
        lncount += 1
      # in Python 2.7, some are unicodes, some are strs. what a mess!
      if isinstance(line, bytes):
        line = line.decode('utf-8')
      dummyoutfile.write(line)

    fl = self.linenostart
    sp = self.linenospecial
    st = self.linenostep
    la = self.lineanchors
    aln = self.anchorlinenos
    nocls = self.noclasses
    if sp:
      lines = []

      for i in range(fl, fl+lncount):
        if i % st == 0:
          if i % sp == 0:
            if aln:
              lines.append('<a href="#%s-%d" class="special">%d</a>' %
                     (la, i, i))
            else:
              lines.append('<span class="special">%d</span>' % (i))
          else:
            if aln:
              lines.append('<a href="#%s-%d">%d</a>' % (la, i, i))
            else:
              lines.append('%d' % (i))
        else:
          lines.append('')
      ls = '\n'.join(lines)
    else:
      lines = []
      for i in range(fl, fl+lncount):
        if i % st == 0:
          if aln:
            lines.append('<a href="#%s-%d">%d</a>' % (la, i, i))
          else:
            lines.append('%d' % (i))
        else:
          lines.append('')
      ls = '\n'.join(lines)

    # in case you wonder about the seemingly redundant <div> here: since the
    # content in the other cell also is wrapped in a div, some browsers in
    # some configurations seem to mess up the formatting...
    if nocls:
      yield 0, ('<table class="%stable">' % self.cssclass +
            '<tr><td><div class="linenodiv" '
            'style="background-color: #f0f0f0; padding-right: 10px">'
            '<pre style="line-height: 125%">' +
            ls + '</pre></div></td><td class="code">')
    else:
      yield 0, ('<table class="%stable">' % self.cssclass +
            '<tr><td class="linenos"><div class="linenodiv">' +
            ls + '</div></td><td class="code">')
    yield 0, dummyoutfile.getvalue()
    yield 0, '</td></tr></table>'
