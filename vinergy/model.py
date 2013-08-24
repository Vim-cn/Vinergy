from pymongo import Connection

from .config import DBINFO

db = Connection(**DBINFO).vinergy
codebase = db.codebase
codebase.ensure_index('count')

def get_code_by_name(name):
  '''Get code by name'''
  return codebase.find_one({'name': name})

def get_codename_by_oid(oid):
  '''Get code by oid (_id)'''
  doc = codebase.find_one({'_id': oid}, ['name'])
  if doc:
    return doc['name']

def get_count():
  '''Get count of latest snippet'''
  try:
    doc = list(codebase.find(None, ['count']).sort('count', direction=-1).limit(1))[0]
  except KeyError:
    return None
  else:
    return int(doc['count'])

def insert_code(oid, name, content, count, date):
  '''Insert new code to database'''
  code = {
    '_id': oid,
    'name': name,
    'content': [('text', content)],
    'syntax': ['text'],
    'count': count,
    'date': date,
  }
  codebase.insert(code)

def update_code(name, content, syntax):
  '''
    update doc with new rendered code.
  '''
  code = {
    'content': [syntax, content],
    'syntax': syntax,
  }
  codebase.update({'name': name}, {'$push': code})
