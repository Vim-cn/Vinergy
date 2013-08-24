#!/usr/bin/env python
# vim:fileencoding=utf-8

import os
from hashlib import md5
import time
import datetime

import bson
from tornado.web import RequestHandler, HTTPError, MissingArgumentError
import tornado.template

from . import model
from .util import util

def _create_template(self, name):
  '''don't compress_whitespace in <pre> incorrectly'''
  path = os.path.join(self.root, name)
  f = open(path, "rb")
  template = tornado.template.Template(
    f.read(), name=name, loader=self,
    compress_whitespace=False,
  )
  f.close()
  return template

tornado.template.Loader._create_template = _create_template

class BaseHandler(RequestHandler):
  def get_template_namespace(self):
    ns = super(BaseHandler, self).get_template_namespace()
    ns['url'] = self.request.full_url()
    ns['path'] = self.request.path
    return ns

class ShowCode(BaseHandler):
  def get(self, codeid):
    '''Browse code'''
    if codeid.rfind('/') != -1:
      # URL looks like wuitE/vim
      codeid, syntax = codeid.rsplit('/', 1)
      syntax = syntax.lower()
    else:
      syntax = None
    doc = model.get_code_by_name(codeid)
    if not doc:
      raise HTTPError(404, codeid + ' not found')
    codes = dict(doc['content'])

    if syntax is None:
      syntax = self.request.query.lower()

    if not syntax:
      self.set_header('Content-Type', 'text/plain')
      self.finish(codes['text'])
      return

    # NOTE: syntax may fall back to text
    syntax = util.norm_filetype(syntax)

    is_terminal = util.is_terminal(self.request.headers.get('User-Agent'))
    if is_terminal and syntax != 'text':
      syntax_ = 't_' + syntax
    else:
      syntax_ = syntax
    code = codes.get(syntax_, None)

    # If there is rendered code in database already, just return it
    if code is not None:
      if is_terminal:
        self.finish(code)
      else:
        self.render('code.html', code=code)
      return

    # Otherwise we should render text first
    code = codes['text']
    if is_terminal:
      # term
      r = util.render(code, 'TerminalFormatter', syntax)
      model.update_code(codeid, r, syntax_)
      self.finish(r)
    else:
      # web
      r = util.render(code, 'HtmlFormatter', syntax)
      model.update_code(codeid, r, syntax_)
      self.render('code.html', code=r)

class Index(BaseHandler):
  def get(self):
    self.render('index.html')
    return

  def post(self):
    '''Insert new code'''
    try:
      code = self.get_argument('vimcn')
      # Content must be longer than "print 'Hello, world!'"
      # or smaller than 64 KiB
      if len(code) < 23 or len(code) > 64 * 1024:
        raise ValueError
      oid = bson.Binary(md5(code.encode('utf-8')).digest(),
                        bson.binary.MD5_SUBTYPE)
      r = model.get_codename_by_oid(oid)
      if r is not None:
        name = r
      else:
        name, count = util.name_count()
        # Python 3.3: datetime.datetime.utcnow().timestamp()
        epoch = time.mktime(datetime.datetime.utctimetuple(
          datetime.datetime.utcnow()))
        model.insert_code(oid, name, code, count, epoch)
      self.finish('http://%s/%s\n' % (self.request.host, name))
    except MissingArgumentError:
      self.set_status(400)
      self.finish('Oops. Please Check your command.\n')
    except ValueError:
      self.set_status(400)
      tip = '''Hi, the code snippet must be longer than 'print("Hello, world!")' or shorter than 64 KiB.\n'''
      tip = util.render(tip, 'TerminalFormatter', 'py')
      self.finish(tip)

