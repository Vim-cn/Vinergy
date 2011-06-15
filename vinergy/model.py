#!/usr/bin/env python2
# vim: set fileencoding=utf-8:
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: model.py
# @Date: 2011年06月11日 星期六 03时00分35秒

'''
  vinergy.model
  ~~~~~~~~~~~~~

  Models of Vinergy
'''

__all__ = ['get_code_by_name',
           'get_code_by_oid',
           'get_count',
           'insert_code',
           'update_code',
          ]

from pymongo import Connection, DESCENDING

from config import DBURL


conn = Connection(**DBURL)
db = conn.vinergy
codebase = db.codebase

def get_code_by_name(name):
  '''Get code by name'''
  code = codebase.find_one({'name': name})
  return code or None

def get_code_by_oid(oid):
  '''Get code by oid (_id)'''
  code = codebase.find_one({'_id': oid})
  return code or None

def get_count():
  '''Get count of latest snippet'''
  doc = codebase.find(None, {'content': 0}).sort('count', DESCENDING).limit(1)
  count = doc[0]['count']
  return int(count)

def insert_code(oid, name, content, count, date):
  '''Insert new code to database'''
  code = {'_id': oid,
          'name': name,
          'content': [('raw', content)],
          'syntax': ['raw'],
          'count': count,
          'date': date,
         }
  codebase.insert(code)

def update_code(name, content, syntax):
  '''
    update doc with new rendered code.
  '''
  code = {'content': [syntax, content],
          'syntax': syntax,
         }
  codebase.update({'name': name}, {'$push': code})


