#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import datetime
import logging
import os
import re
import string
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/core/dashboard', '', _path))
from api.messageable.messageable import Messageable  # noqa
from api.registrable.registrable import Registrable  # noqa
from api.renderable.renderable import Renderable  # noqa
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from util.ago.ago import delta  # noqa
from util.component.component import anchor  # noqa
from util.component.component import card  # noqa
from util.component.component import table  # noqa
from util.datetime_.datetime_ import decode_datetime  # noqa
from util.datetime_.datetime_ import encode_datetime  # noqa
from util.datetime_.datetime_ import suffix  # noqa
from util.secrets.secrets import secrets_sub  # noqa
from util.slack.slack import chat_post_message  # noqa
from util.slack.slack import files_upload  # noqa

_cols = ['', ' class="text-right w-75p"']
_link = 'https://github.com/brunner/orangeandblueleague/blob/master/filefairy/'


class StringFormatter(string.Formatter):
    def get_value(self, key, args, kwargs):
        return kwargs.get(key, '{{{0}}}'.format(key))


class Dashboard(Messageable, Registrable, Renderable):
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)
        self.formatter = StringFormatter()

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/dashboard/'

    @staticmethod
    def _info():
        return 'Tails exceptions and log messages.'

    @staticmethod
    def _title():
        return 'dashboard'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == Notify.FAIRYLAB_DAY:
            self._retire(**kwargs)
        return Response()

    def _on_message_internal(self, **kwargs):
        return Response()

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/dashboard/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'dashboard.html', _home)]

    def _setup_internal(self, **kwargs):
        self._render(**kwargs)
        return Response()

    def _shadow_internal(self, **kwargs):
        return []

    def resolve(self, *args, **kwargs):
        if len(args) != 1:
            return Response()

        module = args[0]

        data = self.data
        original = copy.deepcopy(data)

        for day in self.data['records']:
            for r in self.data['records'][day]:
                if module + '.py' in r['pathname']:
                    r['levelname'] = 'INFO'
                if 'Disabled ' + module + '.' in r['msg']:
                    r['levelname'] = 'INFO'

        if data != original:
            self.write()
            self._render(**kwargs)

        return Response()

    @staticmethod
    def _line(record):
        lineno = record['lineno']
        return '#L' + str(lineno)

    @staticmethod
    def _url(record):
        pathname = record['pathname']
        if pathname.count('filefairy/') == 1:
            start, end = pathname.split('filefairy/')
        else:
            end = pathname
        return _link + end + Dashboard._line(record)

    @staticmethod
    def _content(record):
        pathname = record['pathname']
        if '/' in pathname:
            start, end = pathname.rsplit('/', 1)
        else:
            end = pathname
        return end + Dashboard._line(record)

    @staticmethod
    def _msg(record):
        count = record['count']
        x = ' (x' + str(count) + ')' if count > 1 else ''
        return record['msg'].strip('.') + x + '.'

    @staticmethod
    def _card(date, record):
        href = Dashboard._url(record)
        title = Dashboard._content(record)
        info = Dashboard._msg(record)
        code = record['exc']
        ts = delta(decode_datetime(record['date']), date)
        return card(href=href, title=title, info=info, code=code, ts=ts)

    @staticmethod
    def _row(record):
        a = anchor(Dashboard._url(record), Dashboard._content(record))
        msg = Dashboard._msg(record)
        left = '<div class="d-inline-block pr-1">' + a + '</div>'
        right = '<div class="d-inline-block">' + msg + '</div>'
        date = record['date']
        ddate = decode_datetime(date)
        fdate = ddate.strftime('%H:%M')
        return [left + right, fdate]

    @staticmethod
    def _sort(record):
        return (record['date'], record['pathname'], record['lineno'])

    def _home(self, **kwargs):
        ret = {
            'breadcrumbs': [{
                'href': '/fairylab/',
                'name': 'Home'
            }, {
                'href': '',
                'name': 'Dashboard'
            }]
        }

        date = kwargs['date']

        ret['exceptions'] = []
        ret['warnings'] = []
        ret['logs'] = []
        for day in sorted(self.data['records']):
            dday = decode_datetime(day)
            fday = dday.strftime('%A, %B %-d{S}, %Y').replace(
                '{S}', suffix(dday.day))

            body = []
            records = sorted(self.data['records'][day], key=self._sort)
            for r in records:
                levelname = r['levelname']
                if levelname == 'WARNING' and r['count'] < 5:
                    continue
                if levelname == 'ERROR':
                    ret['exceptions'].insert(0, self._card(date, r))
                if levelname == 'WARNING':
                    ret['warnings'].insert(0, self._card(date, r))
                body.insert(0, self._row(r))

            t = table(
                clazz='border mt-3 table-fixed',
                hcols=_cols,
                bcols=_cols,
                head=[fday, ''],
                body=body)
            ret['logs'].insert(0, t)

        return ret

    def _log(self, **kwargs):
        record = {k: kwargs[k] for k in ['levelname', 'lineno', 'msg']}

        cwd = os.getcwd()
        record['pathname'] = os.path.join(cwd, kwargs['pathname'])

        levelname = kwargs['levelname']
        if levelname == 'DEBUG':
            content = self._content(record)
            chat_post_message('testing', content + ': ' + record['msg'])
            if kwargs.get('output'):
                output = secrets_sub(kwargs['output'])
                flog = kwargs.get('module', 'unknown') + '.log.txt'
                files_upload(output, flog, 'testing')
        else:
            e = kwargs['exc_info']
            exc = logging.Formatter.formatException(self, e) if e else ''
            record['exc'] = secrets_sub(exc)
            count = self._record(record)
            if levelname == 'ERROR' or (levelname == 'WARNING' and count == 5):
                content = self._content(record)
                chat_post_message('testing', content + ': ' + record['msg'])
                flog = kwargs.get('module', 'unknown') + '.log.txt'
                files_upload(record['exc'], flog, 'testing')

    def _record(self, record):
        date = datetime.datetime.now()
        encoded_date = encode_datetime(date)

        day = datetime.datetime(date.year, date.month, date.day)
        encoded_day = encode_datetime(day)
        if encoded_day not in self.data['records']:
            self.data['records'][encoded_day] = []

        count = 1
        for r in self.data['records'][encoded_day]:
            if record.items() <= r.items():
                rdate = decode_datetime(r['date'])
                diff = date - rdate
                s, d = diff.seconds, diff.days
                if d == 0 and s < 1000:
                    count = r['count'] + 1
                    r['count'] = count
                    r['date'] = encoded_date

        if count == 1:
            record.update({'count': 1, 'date': encoded_date})
            self.data['records'][encoded_day].append(record)

        self.date = date
        self.write()
        self._render(date=date)

        return count

    def _retire(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        date = kwargs['date']
        cut = date - datetime.timedelta(days=7)
        cut = datetime.datetime(cut.year, cut.month, cut.day)

        days = list(original['records'].keys())
        for day in days:
            if decode_datetime(day) <= cut:
                del data['records'][day]

        if data != original:
            self.write()
            self._render(**kwargs)


class LoggingHandler(logging.Handler):
    def __init__(self, dashboard):
        super().__init__()
        self.dashboard = dashboard

    def emit(self, record):
        self.dashboard._log(**vars(record))
