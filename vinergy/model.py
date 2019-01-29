import hashlib

import asyncpg

from .config import DBINFO
from .util.b52 import b52_encode

DB_CONN = None

async def setup():
  global DB_CONN
  DB_CONN = await asyncpg.connect(DBINFO)

async def get_code_by_name(name, syntax):
  row = await DB_CONN.fetchrow(
    'select content from rendered_code where name = $1 and syntax = $2',
    name, syntax,
  )
  if row is None:
    raise FileNotFoundError
  return row['content']

async def get_raw_code_by_name(name):
  row = await DB_CONN.fetchrow(
    'select content from raw_code where name = $1', name)
  if row is None:
    raise FileNotFoundError
  return row['content']

async def get_codename_by_content(content):
  h = hashlib.sha1(content.encode('utf-8'))
  sha1sum = h.digest()
  row = await DB_CONN.fetchrow(
    '''select name from raw_code
       where sha1sum = $1''', sha1sum)
  if row is None:
    raise FileNotFoundError
  return row['name']

async def insert_code(content):
  h = hashlib.sha1(content.encode('utf-8'))
  sha1sum = h.digest()
  row = await DB_CONN.fetchrow(
    '''insert into raw_code
       (content, sha1sum) values
       ($1, $2) returning id
    ''', content, sha1sum)

  name = b52_encode(row['id'])
  await DB_CONN.execute(
    '''update raw_code
       set name = $1 where id = $2''',
    name, row['id'])

  return name

async def update_code(name, content, syntax):
  await DB_CONN.execute(
    '''insert into rendered_code
       (name, content, syntax) values
       ($1, $2, $3)''',
    name, content, syntax)
