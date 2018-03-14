#!/usr/bin/env python

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/utils/jinja2', '', _path)
sys.path.append(_root)
from utils.jinja2.jinja2_util import env  # noqa


class JsonUtilTest(unittest.TestCase):
    def test_env(self):
        environment = env()
        templates = os.path.join(_root, 'templates')
        self.assertEqual(environment.loader.searchpath, [templates])
        self.assertEquals(environment.trim_blocks, True)
        self.assertEquals(environment.lstrip_blocks, True)


if __name__ == '__main__':
    unittest.main()