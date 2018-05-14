#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/json', '', _path))
from util.json.json_ import dumps  # noqa


class FakeObject(object):
    def __init__(self):
        self.a = 1


class JsonTest(unittest.TestCase):
    def test_dumps(self):
        data = {'c': 1, 'b': FakeObject(), 'a': 'foo'}
        actual = dumps(data)
        expected = '{\n  "a": "foo", \n  "b": "", \n  "c": 1\n}'
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()