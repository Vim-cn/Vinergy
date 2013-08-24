#!/usr/bin/env python2
# vim: set fileencoding=utf-8:
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: b52.py
# @Date: 2011年06月15日 星期三 10时26分25秒

'''
  vinergy.util.b52
  ~~~~~~~~~~~~~~~~

  Base 52 translator
'''

ALPHABET = 'bcdfghjklmnpqrstvwxyz0123456789BCDFGHJKLMNPQRSTVWXYZ'
PAD = 4

def b52_encode(num, alphabet=ALPHABET):
  '''Encode a nubmer in Base X'''
  if (num == 0):
    return alphabet[0]
  base = len(alphabet)
  # Let encoded string longer than PAD
  num = int(num + pow(base, PAD))

  s = []
  while num:
    rem = num % base
    num = num // base
    s.append(alphabet[rem])
  return ''.join(reversed(s))

def b52_decode(s, alphabet=ALPHABET):
  '''Decode the encoded string into number'''
  base = len(alphabet)
  l = len(s)
  num = 0
  idx = 0
  for c in s:
    p = (l - (idx + 1))
    num += alphabet.index(c) * (base ** p)
    idx += 1
  num = int(num - pow(base, PAD))
  return num
