from tornado.web import RequestHandler, HTTPError, MissingArgumentError

from . import model
from .util import util

class BaseHandler(RequestHandler):
  def get_template_namespace(self):
    ns = super().get_template_namespace()
    ns['url'] = self.request.full_url()
    ns['path'] = self.request.path
    return ns

class ShowCode(BaseHandler):
  async def get(self, codeid):
    '''Browse code'''
    if codeid.rfind('/') != -1:
      # URL looks like wuitE/vim
      codeid, syntax = codeid.rsplit('/', 1)
      syntax = syntax.lower()
    else:
      syntax = None

    if syntax is None:
      syntax = self.request.query.lower()

    if not syntax:
      try:
        content = await model.get_raw_code_by_name(codeid)
      except FileNotFoundError:
        raise HTTPError(404, codeid + ' not found')
      self.set_header('Content-Type', 'text/plain')
      self.finish(content)
      return

    # NOTE: syntax may fall back to text
    syntax = util.norm_filetype(syntax)

    is_terminal = util.is_terminal(self.request.headers.get('User-Agent'))
    if is_terminal and syntax != 'text':
      syntax_ = 't_' + syntax
    else:
      syntax_ = syntax

    try:
      code = await model.get_code_by_name(codeid, syntax_)
      if is_terminal:
        self.finish(code)
      else:
        self.render('code.html', code=code)
    except FileNotFoundError:
      # Otherwise we should render text first
      try:
        code = await model.get_raw_code_by_name(codeid)
      except FileNotFoundError:
        raise HTTPError(404, codeid + ' not found')

      if is_terminal:
        # term
        r = util.render(code, 'TerminalFormatter', syntax)
        self.finish(r)
      else:
        # web
        r = util.render(code, 'HtmlFormatter', syntax)
        self.render('code.html', code=r)
      await model.update_code(codeid, r, syntax_)

  async def put(self, filename):
    try:
      code = self.request.body.decode('utf-8')
      await store_code(self, code)
    except UnicodeDecodeError:
      self.set_status(400)
      self.finish('Oops. Please check your code encoding.\n')

class Index(BaseHandler):
  def get(self):
    self.render('index.html')

  async def post(self):
    '''Insert new code'''
    try:
      code = self.get_argument('vimcn')
      await store_code(self, code)
    except MissingArgumentError:
      self.set_status(400)
      self.finish('Oops. Please check your command.\n')

async def store_code(self, code):
  try:
    # Content must be longer than "print 'Hello, world!'"
    # or smaller than 64 KiB
    if len(code) < 23 or len(code) > 64 * 1024:
      raise ValueError

    try:
      name = await model.get_codename_by_content(code)
    except FileNotFoundError:
      name = await model.insert_code(code)

    self.finish('%s://%s/%s\n' % (
      self.request.protocol, self.request.host, name))
  except ValueError:
    self.set_status(400)
    tip = '''Hi, the code snippet must be longer than 'print("Hello, world!")' or shorter than 64 KiB.\n'''
    tip = util.render(tip, 'TerminalFormatter', 'py')
    self.finish(tip)

