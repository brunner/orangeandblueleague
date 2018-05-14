#!/usr/bin/env pythonutils
# -*- coding: utf-8 -*-

import abc
import datetime
import json
import importlib
import mock
import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/util/test', '', _path)
sys.path.append(_root)
from api.renderable.renderable import Renderable  # noqa
from util.jinja2.jinja2_ import env  # noqa
from util.json.json_ import dumps  # noqa


class Test(unittest.TestCase):
    @abc.abstractmethod
    def init_mocks(self):
        pass

    @staticmethod
    def write(fname, data):
        with open(fname, 'r+') as f:
            original = json.loads(f.read())
            f.seek(0)
            f.write(dumps(data) + '\n')
            f.truncate()
            return original


def _gen_golden(case, _cls, _pkg, _pth, _read):
    @mock.patch.object(_cls, '_render_internal')
    @mock.patch('api.renderable.renderable.check_output')
    def test_golden(self, mock_check, mock_render):
        self.init_mocks(_read)
        date = datetime.datetime(1985, 10, 26, 6, 2, 30)
        golden = os.path.join(_pth, 'goldens/{}_golden.html'.format(case))
        sample = '{}.samples.{}_sample'.format(_pkg, case)
        module = importlib.import_module(sample)
        subtitle, tmpl, context = [
            getattr(module, attr) for attr in ['subtitle', 'tmpl', 'context']
        ]
        mock_render.return_value = [(golden, subtitle, tmpl, context)]
        plugin = _cls(e=env())
        plugin._render(date=date)

    return test_golden


def main(_tst, _cls, _pkg, _pth, _read, _main):
    if issubclass(_cls, Renderable):
        d = os.path.join(_root, _pth, 'samples')
        cs = filter(lambda x: x.endswith('_sample.py'), os.listdir(d))
        for c in cs:
            case = re.sub('_sample.py', '', c)
            test_golden = _gen_golden(case, _cls, _pkg, _pth, _read)
            setattr(_tst, 'test_golden__{}'.format(case), test_golden)

    if _main:
        unittest.main()