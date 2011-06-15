#!/usr/bin/env python2
# vim: set fileencoding=utf-8:
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: mylog.py
# @Date: 2011年 06月 11日 星期六 11:06:33 CST

import sys
import logging
from wsgilog import WsgiLog, LogStdout

import config


class Log(WsgiLog):
  def __init__(self, application):
    WsgiLog.__init__(
      self,
      application,
      logformat='%(message)s',
      tofile=True,
      file=config.LOG_FILE,
      interval=config.LOG_INTERVAL,
      backups=config.LOG_BACKUPS
    )
    sys.stdout = LogStdout(self.logger, logging.INFO)
    sys.stderr = LogStdout(self.logger, logging.ERROR)
