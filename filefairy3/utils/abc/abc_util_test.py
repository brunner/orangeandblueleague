#!/usr/bin/env python

import abc
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/utils/abc', '', _path))
from utils.abc.abc_util import abstractstatic  # noqa


class Foo(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(Foo, self).__init__()

    @abstractstatic
    def _data():
        pass


class Bar(Foo):
    def __init__(self):
        super(Bar, self).__init__()

    @staticmethod
    def _data():
        return 'Bar'


class AbcUtilTest(unittest.TestCase):
    def test_abstractstatic(self):
        self.assertEquals(Bar._data(), 'Bar')


if __name__ == '__main__':
    unittest.main()