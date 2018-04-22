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
from utils.component.component_util import table  # noqa
from utils.datetime.datetime_util import decode_datetime, encode_datetime, suffix  # noqa
from utils.team.team_util import divisions, hometown, ilogo  # noqa

_html = 'https://orangeandblueleaguebaseball.com/StatsLab/reports/news/html/'
_game_box = 'box_scores/game_box'


class StatsplusPlugin(PluginApi, RenderableApi):
    def __init__(self, **kwargs):
        super(StatsplusPlugin, self).__init__(**kwargs)

    @property
    def enabled(self):
        return True

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

        if 'MAJOR LEAGUE BASEBALL Final Scores\n' in text:
            self._final_scores(text)

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

    @staticmethod
    def _live_tables_header(title):
        return table(
            clazz='table-fixed border border-bottom-0 mt-3',
            hcols=[' class="text-center"'],
            bcols=[],
            head=[title],
            body=[])

    @staticmethod
    def _link(text):
        match = re.findall('^<([^|]+)\|([^<]+)>$', text)
        if match:
            link, content = match[0]
            return '<a href="{0}">{1}</a>'.format(link, content)
        return ''

    def _clear(self):
        self.data['scores'] = {}

    def _final_scores(self, text):
        match = re.findall('\d{2}\/\d{2}\/\d{4}', text)
        if match:
            date = datetime.datetime.strptime(match[0], '%m/%d/%Y')
            score = text.split('\n', 1)[1].replace(_html + _game_box, '{0}{1}')
            self.data['scores'][encode_datetime(date)] = score
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
            'scores': []
        }

        status = data['status']
        if status == 'season':
            ret['live'] = self._live_tables_season()

        for date in sorted(data['scores'].keys(), reverse=True):
            ret['scores'].append(self._scores_table(date))

        return ret

    def _live_tables_season(self):
        div = divisions()
        size = len(div) / 2
        al, nl = div[:size], div[size:]
        return [
            self._live_tables_header('American League'),
            self._live_tables_season_internal(al),
            self._live_tables_header('National League'),
            self._live_tables_season_internal(nl)
        ]

    def _live_tables_season_internal(self, league):
        body = []
        for division in league:
            inner = []
            for teamid in division[1]:
                inner.append(self._scores_season(teamid))
            body.append(inner)
        return table(
            clazz='table-fixed border',
            hcols=[],
            bcols=[' class="td-sm position-relative text-center w-20"'] * 5,
            head=[],
            body=body)

    def _scores_season(self, teamid):
        ht = hometown(teamid)
        w, l = 0, 0
        for date in self.data['scores']:
            score = self.data['scores'][date]
            w += len(re.findall(r'\|' + re.escape(ht), score))
            l += len(re.findall(r', ' + re.escape(ht), score))
        return ilogo(teamid, '{0}-{1}'.format(w, l))

    def _scores_table(self, date):
        pdate = decode_datetime(date)
        fdate = pdate.strftime('%A, %B %-d{S}, %Y').replace(
            '{S}', suffix(pdate.day))
        body = []
        for line in self.data['scores'][date].splitlines():
            text = line.format(_html, _game_box).replace('*', '')
            body.append([self._link(text)])
        return table(hcols=[''], bcols=[''], head=[fdate], body=body)
