#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/util/jinja2', '', _path)
sys.path.append(_root)
from util.jinja2.jinja2_util import env  # noqa


class Jinja2UtilTest(unittest.TestCase):
    def test_env(self):
        environment = env()
        templates = os.path.join(_root, 'templates')
        self.assertEqual(environment.loader.searchpath, [templates])
        self.assertEqual(environment.trim_blocks, True)
        self.assertEqual(environment.lstrip_blocks, True)


if __name__ == '__main__':
    unittest.main()