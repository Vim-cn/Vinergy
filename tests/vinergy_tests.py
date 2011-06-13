#!/usr/bin/env python
# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: vinergy_tests.py
# @Date: 2011年06月06日 星期一 23时22分07秒

from paste.fixture import TestApp
from nose.tools import *
from vinergy.vinergy import app, model


class TestCode(object):
  def test_index(self):
    middleware = []
    testapp = TestApp(app.wsgifunc(*middleware))
    r = testapp.get('/')
    assert_equal(r.status, 200)
    r.mustcontain('vinergy')

  def test_model(self):
    assert_false(model.get_code_by_name(None))
