#!/usr/bin/env python2
# vim: set fileencoding=utf-8:
# @Name: repl.py

import os


def repl(local, histfile=None):
  import readline
  import rlcompleter
  readline.parse_and_bind('tab: complete')
  if histfile is not None and os.path.exists(histfile):
    readline.read_history_file(histfile)
  import code
  code.interact(local=local)
  if histfile is not None:
    readline.write_history_file(histfile)

if __name__ == '__main__':
  repl(locals())
