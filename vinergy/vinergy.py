#!/usr/bin/env python
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

import util
import model
import config


### Url mappings
urls = (
  '/(.*)', 'Index',
)


### Templates
t_globals = {
  'datestr': web.datestr,
}
rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
render = web.template.render(rootdir+'templates/', base='base',
                             globals=t_globals)


### Controllers
class Index:

  def GET(self, got):
    '''Browse code'''
    if not got: # Show frontpage
      return render.index(config.URL)
    else: # Show code
      doc = model.get_code_by_name(got)
      # "got" nothing
      if not doc:
        raise web.notfound(got + ' not found\n')
      codes = dict(doc['content'])

      syntax = web.ctx.query[1:].lower()
      if not syntax:
        return codes['raw']

      is_t = util.is_termua(web.ctx.env['HTTP_USER_AGENT'])
      s = lambda s: 't_'+s if is_t else s
      # If there is rendered code in database already, just return it
      code = codes.get(s(syntax), None)
      if code is not None: return code
      # Otherwise we should render raw first
      code = codes['raw']
      if is_t:
        r = util.render(code, 'TerminalFormatter', syntax)
      else:
        r = util.render(code, 'HtmlFormatter', syntax)
      model.update_code(got, r, s(syntax))
      return r


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
        name = util.new_name()
        while model.get_code_by_name(name):
          name = util.new_name()
        epoch = time.mktime(datetime.datetime.utctimetuple(datetime.\
                                                           datetime.utcnow()))
        model.insert_code(oid, name, code, epoch)
      raise util.response(' ' + config.URL + '/' + name + '\n')
    except AttributeError:
      status = '500 Internal Server Error'
      raise util.response('Oops. Please Check your command.\n', status)
    except ValueError:
      status = '500 Internal Server Error'
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
