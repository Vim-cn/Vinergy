import os
import asyncio
from typing import Any
import importlib.resources
import mimetypes
from urllib.parse import urljoin

import tornado.web
import tornado.ioloop
import tornado.template
from tornado.options import define, options
from tornado.httpserver import HTTPServer

from . import handlers

class ResourceFileHandler(tornado.web.RequestHandler):
  def initialize(self, root):
    self.root = root.replace('.', '/')

  def get(self, path):
    p = os.path.join(self.root, path)
    if os.path.commonpath([self.root, p]) != self.root:
      raise tornado.web.HTTPError(404)

    package, name = p.rsplit('/', 1)
    package = package.replace('/', '.')
    with importlib.resources.open_binary(package, name) as f:
      data = f.read()

    content_type = self.get_content_type(p)
    if content_type:
      self.set_header("Content-Type", content_type)
    self.finish(data)

  def get_content_type(self, path):
    mime_type, encoding = mimetypes.guess_type(path)
    # per RFC 6713, use the appropriate type for a gzip compressed file
    if encoding == "gzip":
      return "application/gzip"
    # As of 2015-07-21 there is no bzip2 encoding defined at
    # http://www.iana.org/assignments/media-types/media-types.xhtml
    # So for that (and any other encoding), use octet-stream.
    elif encoding is not None:
      return "application/octet-stream"
    elif mime_type is not None:
      return mime_type
    # if mime_type not detected, use application/octet-stream
    else:
      return "application/octet-stream"

class ResourceTemplateLoader(tornado.template.BaseLoader):
  def __init__(self, root: str, **kwargs: Any) -> None:
    super().__init__(**kwargs)
    self.root = root.replace('.', '/')

  def resolve_path(self, name: str, parent_path: str = None) -> str:
    if parent_path:
      return urljoin(parent_path, name)
    else:
      return name

  def _create_template(self, name: str) -> tornado.template.Template:
    path = os.path.join(self.root, name)
    package, name = path.rsplit('/', 1)
    package = package.replace('/', '.')
    with importlib.resources.open_binary(package, name) as f:
      template = tornado.template.Template(
        f.read(), name=name, loader=self)
      return template

### URL mappings
routers = (
  (r'/static/(.*)', ResourceFileHandler, {'root': 'vinergy.static'}),
  (r'/', handlers.Index),
  (r'/(.*)', handlers.ShowCode),
)

def setup():
  from .config import PAD
  from .util import b52
  from . import model

  b52.PAD = PAD
  loop = asyncio.get_event_loop()
  loop.run_until_complete(model.setup())

def main():
  define("port", default=8000, help="run on the given port", type=int)
  define("address", default='', help="run on the given IP address", type=str)
  define("debug", default=False, help="debug mode", type=bool)

  tornado.options.parse_command_line()
  setup()
  application = tornado.web.Application(
    routers,
    gzip = True,
    debug = options.debug,
    template_loader = ResourceTemplateLoader(
      root='vinergy.templates', whitespace='all'),
  )
  http_server = HTTPServer(application, xheaders=True)
  http_server.listen(options.port, options.address)
  try:
    tornado.ioloop.IOLoop.current().start()
  except KeyboardInterrupt:
    pass

if __name__ == "__main__":
  main()
