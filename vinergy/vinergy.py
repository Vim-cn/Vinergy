#!/usr/bin/env python
# vim:fileencoding=utf-8

'''
vinergy.vinergy
~~~~~~~~~~~~~~~

Vinergy - CLI Pastebin within VimEnergy
'''

import os

import tornado.web
import tornado.ioloop
from tornado.options import define, options
from tornado.httpserver import HTTPServer

from . import handlers

### Templates
topdir = os.path.dirname(os.path.abspath(__file__))
tmpldir = os.path.join(topdir, 'templates')
staticdir = os.path.join(topdir, 'static')

### URL mappings
routers = (
  (r'/', handlers.Index),
  (r'/(.*)', handlers.ShowCode),
)

def main():
  define("port", default=8000, help="run on the given port", type=int)
  define("debug", default=False, help="debug mode", type=bool)

  tornado.options.parse_command_line()
  application = tornado.web.Application(
    routers,
    gzip = True,
    debug = options.debug,
    template_path = tmpldir,
    static_path = staticdir,
  )
  http_server = HTTPServer(application, xheaders=True)
  http_server.listen(options.port)
  try:
    tornado.ioloop.IOLoop.instance().start()
  except KeyboardInterrupt:
    pass

if __name__ == "__main__":
  main()
