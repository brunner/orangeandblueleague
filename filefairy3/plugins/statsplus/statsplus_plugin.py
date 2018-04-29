#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import datetime
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugins/statsplus', '', _path)
sys.path.append(_root)
from apis.plugin.plugin_api import PluginApi  # noqa
from apis.renderable.renderable_api import RenderableApi  # noqa
from enums.activity.activity_enum import ActivityEnum  # noqa
from utils.box.box_util import clarify  # noqa
from utils.component.component_util import table  # noqa
from utils.datetime.datetime_util import decode_datetime  # noqa
from utils.datetime.datetime_util import encode_datetime  # noqa
from utils.datetime.datetime_util import suffix  # noqa
from utils.standings.standings_util import sort  # noqa
from utils.team.team_util import chlany  # noqa
from utils.team.team_util import divisions  # noqa
from utils.team.team_util import encoding_to_decoding_sub  # noqa
from utils.team.team_util import encodings  # noqa
from utils.team.team_util import logo_inline  # noqa
from utils.team.team_util import precoding_to_encoding_sub  # noqa
from utils.team.team_util import precodings  # noqa
from utils.team.team_util import teamid_to_encoding  # noqa

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box_'
_player = 'players/player_'
_shorten = '{}(?:{}|{})'.format(_html, _game_box, _player)
_encodings = '|'.join(encodings())
_precodings = '|'.join(precodings())
_chlany = chlany()
_lhclazz = 'table-fixed border border-bottom-0 mt-3'
_lhcols = [' class="text-center"']
_lbclazz = 'table-fixed border'
_lbcols = [' class="td-sm position-relative text-center w-20"'] * 5


class StatsplusPlugin(PluginApi, RenderableApi):
    def __init__(self, **kwargs):
        super(StatsplusPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return False

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/statsplus/'

    @staticmethod
    def _info():
        return 'Collects live sim results.'

    @staticmethod
    def _title():
        return 'statsplus'

    def _notify_internal(self, **kwargs):
        activity = kwargs['activity']
        if activity == ActivityEnum.DOWNLOAD:
            self.data['finished'] = True
            self.write()
        return False

    def _on_message_internal(self, **kwargs):
        obj = kwargs['obj']
        bot_id = obj.get('bot_id')
        channel = obj.get('channel')
        if bot_id != 'B7KJ3362Y' or channel != 'C7JSGHW8G':
            return ActivityEnum.NONE

        data = self.data
        original = copy.deepcopy(data)

        if self.data['finished']:
            self.data['finished'] = False
            self._clear()

        text = obj.get('text', '')
        highlights = '<[^|]+\|[^<]+> (?:sets|ties) [^)]+\)'
        pattern = '\d{2}\/\d{2}\/\d{4} <([^|]+)\|([^<]+)> (?:sets|ties)'
        if re.findall(pattern, text):
            self._handle('highlights', text, highlights, True)

        injuries = '\w+ <[^|]+\|[^<]+> was injured [^)]+\)'
        pattern = '\d{2}\/\d{2}\/\d{4} Rain delay'
        if re.findall(pattern, text):
            self._handle('injuries', text, injuries, True)

        pattern = '\d{2}\/\d{2}\/\d{4} \w+ <([^|]+)\|([^<]+)> was injured'
        if re.findall(pattern, text):
            self._handle('injuries', text, injuries, True)

        pattern = '\d{2}\/\d{2}\/\d{4} MAJOR LEAGUE BASEBALL Final Scores\n'
        if re.findall(pattern, text):
            self._handle('scores', text, '<[^|]+\|[^<]+>', False)

        if data != original:
            self.write()

        return ActivityEnum.BASE

    def _run_internal(self, **kwargs):
        if self.data['updated']:
            self.data['updated'] = False
            self._render(**kwargs)
            self.write()
            return ActivityEnum.BASE

        return ActivityEnum.NONE

    def _render_internal(self, **kwargs):
        html = 'html/fairylab/statsplus/index.html'
        _home = self._home(**kwargs)
        return [(html, '', 'statsplus.html', _home)]

    def _setup_internal(self, **kwargs):
        self._render(**kwargs)

    def _clear(self):
        self.data['scores'] = {}
        self.data['injuries'] = {}
        self.data['highlights'] = {}

    def _handle(self, key, text, pattern, append):
        date = re.findall('\d{2}\/\d{2}\/\d{4}', text)
        if date:
            date = datetime.datetime.strptime(date[0], '%m/%d/%Y')
            encoded_date = encode_datetime(date)
            if not append or encoded_date not in self.data[key]:
                self.data[key][encoded_date] = []

            match = re.findall(pattern, text)
            for m in match:
                e = re.sub(_shorten, '{0}{1}', precoding_to_encoding_sub(m))
                self.data[key][encoded_date].append(e)
                self.data['updated'] = True

    def _home(self, **kwargs):
        data = self.data
        ret = {
            'breadcrumbs': [{
                'href': '/fairylab/',
                'name': 'Home'
            }, {
                'href': '',
                'name': 'Statsplus'
            }],
            'scores': [],
            'injuries': [],
            'highlights': []
        }

        if not data['postseason']:
            ret['live'] = self._live_regular()

        for date in sorted(data['highlights'].keys(), reverse=True):
            ret['highlights'].append(self._table('highlights', date, _player))

        for date in sorted(data['injuries'].keys(), reverse=True):
            ret['injuries'].append(self._table('injuries', date, _player))

        for date in sorted(data['scores'].keys(), reverse=True):
            ret['scores'].append(self._table('scores', date, _game_box))

        return ret

    def _live_regular(self):
        div = divisions()
        size = len(div) / 2
        al, nl = div[:size], div[size:]

        lrba = self._live_regular_body(al)
        lrbn = self._live_regular_body(nl)

        lhal = table(clazz=_lhclazz, hcols=_lhcols, head=['American League'])
        lbal = table(clazz=_lbclazz, bcols=_lbcols, body=lrba)
        lhnl = table(clazz=_lhclazz, hcols=_lhcols, head=['National League'])
        lbnl = table(clazz=_lbclazz, bcols=_lbcols, body=lrbn)

        return [lhal, lbal, lhnl, lbnl]

    def _live_regular_body(self, league):
        body = []
        for division in league:
            group = [(teamid, self._record(teamid)) for teamid in division[1]]
            inner = [logo_inline(*team_tuple) for team_tuple in sort(group)]
            body.append(inner)
        return body

    def _record(self, teamid):
        encoding = teamid_to_encoding(teamid)
        hw, hl = 0, 0
        for date in self.data['scores']:
            scores = '\n'.join(self.data['scores'][date])
            hw += len(re.findall(r'\|' + re.escape(encoding), scores))
            hl += len(re.findall(r', ' + re.escape(encoding), scores))
        return '{0}-{1}'.format(hw, hl)

    def _table(self, key, date, path):
        lines = self.data[key][date]
        body = self._table_body(date, lines, path)
        head = self._table_head(date)
        return table(hcols=[''], bcols=[''], head=head, body=body)

    def _table_body(self, date, lines, path):
        body = []
        for line in lines:
            line = re.sub('<([^|]+)\|([^<]+)>', r'<a href="\1">\2</a>', line)
            body.append([encoding_to_decoding_sub(line).format(_html, path)])
        return body

    def _table_head(self, date):
        ddate = decode_datetime(date)
        fdate = ddate.strftime('%A, %B %-d{S}, %Y')
        return [fdate.replace('{S}', suffix(ddate.day))]
