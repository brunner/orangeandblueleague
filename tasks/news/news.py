#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/news', '', _path))

from api.renderable.renderable import Renderable  # noqa
from api.runnable.runnable import Runnable  # noqa
from api.serializable.serializable import Serializable  # noqa
from common.datetime_.datetime_ import decode_datetime  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import row  # noqa
from common.elements.elements import table  # noqa
from common.datetime_.datetime_ import suffix  # noqa
from common.json_.json_ import loads  # noqa
from common.re_.re_ import match  # noqa
from common.re_.re_ import search  # noqa
from common.reference.reference import player_to_link_sub  # noqa
from common.teams.teams import encoding_to_decoding_sub  # noqa
from common.teams.teams import icon_absolute  # noqa
from types_.notify.notify import Notify  # noqa
from types_.response.response import Response  # noqa

DATA_DIR = re.sub(r'/tasks/news', '', _path) + '/resources/data/news'
EXTRACT_DIR = re.sub(r'/tasks/news', '/resources/extract', _path)
EXTRACT_LEAGUES = os.path.join(EXTRACT_DIR, 'leagues')


class News(Renderable, Runnable, Serializable):
    def __init__(self, **kwargs):
        super(News, self).__init__(**kwargs)

    @staticmethod
    def _href():
        return '/fairylab/news/'

    @staticmethod
    def _title():
        return 'News'

    def _render_data(self, **kwargs):
        _index_html = self.get_news_html(**kwargs)
        return [('news/index.html', '', 'news.html', _index_html)]

    def _notify_internal(self, **kwargs):
        if kwargs['notify'] == Notify.STATSPLUS_FINISH:
            self._render(**kwargs)
        return Response()

    def create_tables(self, name):
        data = loads(os.path.join(EXTRACT_LEAGUES, name + '.json'))

        tables = []
        for date in sorted(data, reverse=True):
            d = decode_datetime(date)
            suf = suffix(d.day)
            head = d.strftime('%A, %B %-d{S}, %Y').replace('{S}', suf)
            body = []
            for t in data[date]:
                body.append(row(cells=[cell(content=self.get_content(t))]))

            tables.append(
                table(clazz='border mb-3',
                      hcols=[col(clazz='font-weight-bold text-dark')],
                      bcols=[col(clazz='position-relative')],
                      head=[row(cells=[cell(content=head)])],
                      body=body))

        return tables

    def get_news_html(self, **kwargs):
        ret = {}
        for name in ['injuries', 'news', 'transactions']:
            ret[name] = self.create_tables(name)

        return ret

    @staticmethod
    def get_content(text):
        encoding = search(r'(T\d+)\D', text)
        if encoding is None or match(r'(The ' + encoding + r' traded)', text):
            encoding = 'T30'

        text = re.sub(r'^' + encoding + r': ', '', text)
        text = re.sub(r'was injured \.', 'was injured.', text)
        text = re.sub(r'of the ' + encoding + r' honored: Wins', 'wins', text)
        text = re.sub(r'original Organization ', '', text)
        text = re.sub(r'The Diagnosis: (\w)', News.get_diagnosis_content, text)
        text = re.sub(r'Rule 5 draft pick(\w)', r'Rule 5 draft pick \1', text)
        text = re.sub(r'NO-HITTER', r'no-hitter', text)

        text = encoding_to_decoding_sub(text)
        text = player_to_link_sub(text)

        return icon_absolute(encoding, text)

    @staticmethod
    def get_diagnosis_content(m):
        return 'Diagnosis: ' + m.group(1).lower()
