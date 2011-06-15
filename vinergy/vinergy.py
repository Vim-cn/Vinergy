#!/usr/bin/env python2
# vim: set fileencoding=utf-8:
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: vinergy.py
# @Date: 2011年06月11日 星期六 02时49分07秒

'''
  vinergy.vinergy
  ~~~~~~~~~~~~~~~

  Vinergy - CLI Pastebin within VimEnergy
'''
import os
import web
import time
import datetime
from hashlib import md5

import model
import config
from util import util


### Url mappings
urls = (
  '/(.*)', 'Index',
)


### Templates
rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
render = web.template.render(rootdir+'templates/', base='base')


### Controllers
class Index:

  def GET(self, got):
    '''Browse code'''
    if not got: # Show frontpage
      return render.index(config.URL)
    else: # Show code
      if got.rfind('/') != -1:
        # Url looks like wuitE/vim
        syntax = got.rsplit('/', 1)[1].lower()
        got = got.rsplit('/', 1)[0]
      else:
        syntax = None
      doc = model.get_code_by_name(got)
      # "got" nothing
      if not doc:
        raise web.notfound(got + ' not found\n')
      codes = dict(doc['content'])

      if syntax is None:
        syntax = web.ctx.query[1:].lower()
      if not syntax:
        return codes['raw']
      syntax = util.norm_filetype(syntax)

      is_t = util.is_termua(web.ctx.env['HTTP_USER_AGENT'])
      s = lambda s: 't_'+s if is_t else s
      # If there is rendered code in database already, just return it
      code = codes.get(s(syntax), None)
      if code is not None: return code if is_t else render.code(code)
      # Otherwise we should render raw first
      code = codes['raw']
      if is_t:
        # term
        r = util.render(code, 'TerminalFormatter', syntax)
        model.update_code(got, r, s(syntax))
        return r
      else:
        # web
        r = util.render(code, 'HtmlFormatter', syntax)
        model.update_code(got, r, s(syntax))
        return render.code(r)


  def POST(self, got):
    '''Insert new code'''
    try:
      code = web.input().vimcn
      # Content must be longer than "print 'Hello, world!'"
      if len(code) < 21: raise ValueError
      oid = md5(unicode(code).encode('utf8')).hexdigest()
      r = model.get_code_by_oid(oid)
      if r is not None:
        name = r['name']
      else:
        name, count = util.name_count()
        epoch = time.mktime(datetime.datetime.utctimetuple(datetime.\
                                                           datetime.utcnow()))
        model.insert_code(oid, name, code, count, epoch)
      raise util.response(' ' + config.URL + '/' + name + '\n')
    except AttributeError:
      status = '400 Bad Request'
      raise util.response('Oops. Please Check your command.\n', status)
    except ValueError:
      status = '400 Bad Request'
      tip = 'Hi, content must be longer than \'print "Hello, world!"\'\n'
      tip = util.render(tip, 'TerminalFormatter', 'py')
      raise util.response(tip, status)


### Application
app = web.application(urls, globals())


if __name__ == '__main__':
  ### Run app on localhost
  app.run()
else:
  ### Run app on wsgi mode
  web.config.debug = False
  application = app.wsgifunc()
