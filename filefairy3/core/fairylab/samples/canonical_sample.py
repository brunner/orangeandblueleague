#!/usr/bin/env python
# -*- coding: utf-8 -*-

subtitle = ''

tmpl = 'home.html'

context = {
    'title':
    'home',
    'breadcrumbs': [{
        'href': '',
        'name': 'Home'
    }],
    'browsable': [{
        'href': '/fairylab/bar/',
        'title': 'bar',
        'info': 'Description of bar.',
        'table': None,
        'ts': '10m ago',
        'success': '',
        'danger': ''
    }, {
        'href': '/fairylab/baz/',
        'title': 'baz',
        'info': 'Description of baz.',
        'table': None,
        'ts': '1h ago',
        'success': '',
        'danger': 'failed'
    }, {
        'href': '/fairylab/foo/',
        'title': 'foo',
        'info': 'Description of foo.',
        'table': None,
        'ts': '2m ago',
        'success': '',
        'danger': ''
    }],
    'internal': [{
        'href': '',
        'title': 'quux',
        'info': 'Description of quux.',
        'table': None,
        'ts': '15m ago',
        'success': '',
        'danger': 'failed'
    }, {
        'href': '',
        'title': 'quuz',
        'info': 'Description of quuz.',
        'table': None,
        'ts': '30s ago',
        'success': 'just now',
        'danger': ''
    }, {
        'href': '',
        'title': 'qux',
        'info': 'Description of qux.',
        'table': None,
        'ts': '2d ago',
        'success': '',
        'danger': ''
    }],
}