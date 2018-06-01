#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/leaguefile/samples', '', _path)
sys.path.append(_root)
from util.component.component import card  # noqa
from util.component.component import table  # noqa

_breadcrumbs = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Leaguefile'
}]

_cols = [' class="w-55p"', '']
_table = table(
    clazz='table-sm',
    hcols=_cols,
    bcols=_cols,
    body=[['Time: ', '56m'], ['Size: ', '59,969,530']])
_fp = card(title='Mar 10', table=_table, ts='30s ago', success='ongoing')
_up = table(
    clazz='border mt-3',
    head=['Date', 'Time', 'Size'],
    body=[['Mar 8', '10h 11m', '358,347,534'],
          ['Mar 6', '9h 34m', '356,922,996']])

subtitle = ''

tmpl = 'leaguefile.html'

context = {
    'title': 'leaguefile',
    'breadcrumbs': _breadcrumbs,
    'fp': _fp,
    'up': _up
}
