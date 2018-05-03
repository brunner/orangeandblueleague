#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import copy
import datetime
import os
import re
import sys
import threading

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/download', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.serializable.serializable_api import SerializableApi  # noqa
from utils.datetime.datetime_util import decode_datetime  # noqa
from utils.datetime.datetime_util import encode_datetime  # noqa
from utils.file.file_util import ping  # noqa
from utils.file.file_util import recreate  # noqa
from utils.file.file_util import wget_file  # noqa
from utils.logger.logger_util import log  # noqa
from utils.unicode.unicode_util import deunicode  # noqa
from values.notify.notify_value import NotifyValue  # noqa
from values.response.response_value import ResponseValue  # noqa


class DownloadPlugin(PluginApi, SerializableApi):
    def __init__(self, **kwargs):
        super(DownloadPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _info():
        return 'Manages file download and data extraction.'

    def _notify_internal(self, **kwargs):
        notify = kwargs['notify']
        if notify == NotifyValue.LEAGUEFILE_FINISH:
            self.download(**kwargs)
            return True
        return False

    def _on_message_internal(self, **kwargs):
        return ResponseValue()

    def _run_internal(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        response = ResponseValue()

        if self.data['year']:
            self.data['year'] = False
            response.append_notify(NotifyValue.DOWNLOAD_YEAR)

        if self.data['downloaded']:
            self.data['downloaded'] = False
            response.append_notify(NotifyValue.DOWNLOAD_FINISH)

        if self.data['unreachable']:
            output = ping()
            if output.get('ok'):
                log(self._name(), **dict(
                    kwargs, s='Download resumed.', v=True))
                self.data['unreachable'] = False
                t = threading.Thread(
                    target=self._download_internal, kwargs=kwargs)
                t.daemon = True
                t.start()
                response.append_notify(NotifyValue.BASE)

        if data != original:
            self.write()

        return response

    def _setup_internal(self, **kwargs):
        pass

    def _shadow_internal(self, **kwargs):
        return {'statsplus': {'download.now': self.data['now']}}

    def download(self, **kwargs):
        data = self.data
        original = copy.deepcopy(data)

        log(self._name(), **dict(kwargs, s='Download started.'))
        output = ping()
        if output.get('ok'):
            data['unreachable'] = False
            t = threading.Thread(target=self._download_internal, kwargs=kwargs)
            t.daemon = True
            t.start()
        else:
            data['unreachable'] = True
            log(self._name(), **dict(kwargs, c=output, s='Download failed.'))

        if data != original:
            self.write()

    def _download_internal(self, **kwargs):
        self.data['then'] = self.data['now']

        wget_file()
        self._games()
        self._leagues()

        self.data['downloaded'] = True
        log(self._name(), **dict(kwargs, s='Download finished.'))

        dthen = decode_datetime(self.data['then'])
        dnow = decode_datetime(self.data['now'])
        if dthen.year != dnow.year:
            self.data['year'] = True

        self.write()

    def _games(self):
        box_scores = os.path.join(_root, 'extract/box_scores')
        game_logs = os.path.join(_root, 'extract/game_logs')
        recreate(box_scores)
        recreate(game_logs)

        boxes = 'download/news/html/box_scores'
        leagues = 'download/news/txt/leagues'
        for box in os.listdir(os.path.join(_root, boxes)):
            bdname = os.path.join(box_scores, box)
            bfname = os.path.join(_root, boxes, box)
            log_ = box.replace('game_box', 'log').replace('html', 'txt')
            ldname = os.path.join(game_logs, log_)
            lfname = os.path.join(_root, leagues, log_)
            if not os.path.isfile(bfname) or not os.path.isfile(lfname):
                continue
            self._games_internal(bdname, bfname, ldname, lfname)

    def _games_internal(self, bdname, bfname, ldname, lfname):
        then = decode_datetime(self.data['then'])
        now = decode_datetime(self.data['now'])

        with open(bfname, 'r') as bff:
            bcontent = bff.read()
        with open(lfname, 'r') as lff:
            lcontent = lff.read()

        pattern = 'MLB Box Scores[^\d]+(\d{2}\/\d{2}\/\d{4})'
        match = re.findall(pattern, bcontent)
        if match:
            date = datetime.datetime.strptime(match[0], '%m/%d/%Y')
            if date >= then:
                with open(bdname, 'w') as bdf:
                    bdf.write(bcontent)
                with open(ldname, 'w') as ldf:
                    ldf.write(lcontent)
            if date >= now:
                now = date + datetime.timedelta(days=1)

        self.data['now'] = encode_datetime(now)

    def _leagues(self):
        leagues = 'download/news/txt/leagues'
        dpath = os.path.join(_root, 'extract/leagues/{}.txt')
        fpath = os.path.join(_root, leagues, 'league_100_{}.txt')
        for key in ['injuries', 'news', 'transactions']:
            dname = dpath.format(key)
            fname = fpath.format(key)
            if not os.path.isfile(dname) or not os.path.isfile(fname):
                continue
            self._leagues_internal(key, dname, fname)

    def _leagues_internal(self, key, dname, fname):
        then = decode_datetime(self.data['then'])
        now = decode_datetime(self.data['now'])

        with codecs.open(fname, 'r', encoding='utf-8', errors='replace') as ff:
            content = deunicode(ff.read())

        with open(dname, 'w') as df:
            match = re.findall('\d{8}\t[^\n]+\n', content.strip() + '\n')
            for m in match:
                date = datetime.datetime.strptime(m[:8], '%Y%m%d')
                if date >= then:
                    df.write(m)
                if date > now:
                    now = date

        self.data['now'] = encode_datetime(now)
