#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for standings.py."""

import json
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.extend((_path, re.sub(r'/tasks/standings', '', _path)))

from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import dialog  # noqa
from common.elements.elements import table  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.json_.json_ import filts  # noqa
from common.test.test import RMock  # noqa
from common.test.test import Suite  # noqa
from common.test.test import Test  # noqa
from common.test.test import get_testdata  # noqa
from common.test.test import main  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from tasks.standings.standings import Standings  # noqa
from tasks.standings.standings import GAME_KEYS  # noqa

ENV = env()

DATE_08310000 = datetime_datetime_pst(2024, 8, 31)
DATE_10260602 = datetime_datetime_pst(1985, 10, 26, 6, 2, 30)

GAMES_DIR = re.sub(r'/tasks/standings', '/resource/games', _path)

TESTDATA = get_testdata()


def _data(finished=False, games=None, table_=None):
    if games is None:
        games = {}
    if table_ is None:
        table_ = {}

    return {'games': games, 'finished': finished, 'table': table_}


def _table(keys, table_):
    return {k: table_.get(k, '0-0') for k in keys}


class StandingsTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()

    def create_standings(self, data):
        self.init_mocks(data)
        standings = Standings(date=DATE_10260602, e=ENV)

        self.mock_open.assert_called_once_with(Standings._data(), 'r')
        self.mock_handle.write.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return standings

    def test_reload_data(self):
        standings = self.create_standings(_data())
        actual = standings._reload_data(date=DATE_10260602)
        expected = {
            'division': [
                'condensed_league',
                'expanded_league',
            ],
            'scoreboard': [
                'line_score_body',
                'line_score_foot',
                'line_score_head',
                'unofficial_score_body',
            ],
        }
        self.assertEqual(actual, expected)

    @mock.patch.object(Standings, '_index_html')
    def test_render_data(self, mock_index):
        index_html = {'breadcrumbs': []}
        mock_index.return_value = index_html

        standings = self.create_standings(_data())
        actual = standings._render_data(date=DATE_10260602)
        expected = [('standings/index.html', '', 'standings.html', index_html)]
        self.assertEqual(actual, expected)

        mock_index.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_start')
    @mock.patch.object(Standings, '_parse')
    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__download_year(self, mock_clear, mock_finish, mock_parse,
                                   mock_start):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.DOWNLOAD_YEAR)
        self.assertEqual(response, Response())

        mock_clear.assert_called_once_with(notify=Notify.DOWNLOAD_YEAR)
        self.assertNotCalled(mock_finish, mock_parse, mock_start,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_start')
    @mock.patch.object(Standings, '_parse')
    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__statsplus_finish(self, mock_clear, mock_finish,
                                      mock_parse, mock_start):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.STATSPLUS_FINISH)
        self.assertEqual(response, Response())

        mock_finish.assert_called_once_with(notify=Notify.STATSPLUS_FINISH)
        self.assertNotCalled(mock_clear, mock_parse, mock_start,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_start')
    @mock.patch.object(Standings, '_parse')
    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__statsplus_parse(self, mock_clear, mock_finish, mock_parse,
                                     mock_start):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.STATSPLUS_PARSE)
        self.assertEqual(response, Response())

        mock_parse.assert_called_once_with(notify=Notify.STATSPLUS_PARSE)
        self.assertNotCalled(mock_clear, mock_finish, mock_start,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_start')
    @mock.patch.object(Standings, '_parse')
    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__statsplus_start(self, mock_clear, mock_finish, mock_parse,
                                     mock_start):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.STATSPLUS_START)
        self.assertEqual(response, Response())

        mock_start.assert_called_once_with(notify=Notify.STATSPLUS_START)
        self.assertNotCalled(mock_clear, mock_finish, mock_parse,
                             self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_finish')
    @mock.patch.object(Standings, '_clear')
    def test_notify__other(self, mock_clear, mock_finish):
        standings = self.create_standings(_data())
        response = standings._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.assertNotCalled(mock_clear, mock_finish, self.mock_open,
                             self.mock_handle.write)

    @mock.patch.object(Standings, '_render')
    def test_shadow(self, mock_render):
        standings = self.create_standings(_data())
        response = standings._shadow_internal(date=DATE_10260602)
        self.assertEqual(response, Response())

        mock_render.assert_called_once_with(date=DATE_10260602)
        self.assertNotCalled(self.mock_open, self.mock_handle.write)

    @mock.patch.object(Standings, '_render')
    def test_clear(self, mock_render):
        table_ = {'T40': '87-75', 'T47': '91-71'}
        standings = self.create_standings(_data(table_=table_))
        standings._clear(date=DATE_10260602)

        table_ = {'T40': '0-0', 'T47': '0-0'}
        write = _data(table_=table_)
        mock_render.assert_called_once_with(date=DATE_10260602)
        self.mock_open.assert_called_with(Standings._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Standings, '_render')
    @mock.patch('common.json_.json_.open', create=True)
    @mock.patch('tasks.standings.standings.os.listdir')
    def test_finish(self, mock_listdir, mock_open, mock_render):
        mock_listdir.return_value = ['2449.json', '2469.json', '2476.json']
        suite = Suite(
            RMock(GAMES_DIR, '2449.json', TESTDATA),
            RMock(GAMES_DIR, '2469.json', TESTDATA),
            RMock(GAMES_DIR, '2476.json', TESTDATA),
        )
        mock_open.side_effect = suite.values()

        table_ = {'T40': '66-58', 'T47': '71-53'}
        standings = self.create_standings(_data(table_=table_))
        standings._finish(date=DATE_10260602)

        table_ = {'T40': '66-61', 'T47': '74-53'}
        write = _data(finished=True, table_=table_)
        mock_render.assert_called_once_with(date=DATE_10260602)
        self.mock_open.assert_called_with(Standings._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Standings, '_render')
    @mock.patch('common.json_.json_.open', create=True)
    @mock.patch('tasks.standings.standings.os.listdir')
    def test_parse(self, mock_listdir, mock_open, mock_render):
        mock_listdir.return_value = ['2449.json', '2469.json', '2476.json']
        suite = Suite(
            RMock(GAMES_DIR, '2469.json', TESTDATA),
            RMock(GAMES_DIR, '2476.json', TESTDATA),
        )
        mock_open.side_effect = suite.values()

        game_2449 = filts(json.loads(TESTDATA['2449.json']), GAME_KEYS)
        games = {'2449': game_2449}
        table_ = {'T40': '66-58', 'T47': '71-53'}
        standings = self.create_standings(_data(games=games, table_=table_))
        standings._parse(date=DATE_10260602)

        game_2469 = filts(json.loads(TESTDATA['2469.json']), GAME_KEYS)
        game_2476 = filts(json.loads(TESTDATA['2476.json']), GAME_KEYS)
        games = {'2449': game_2449, '2469': game_2469, '2476': game_2476}
        write = _data(games=games, table_=table_)
        mock_render.assert_called_once_with(date=DATE_10260602)
        self.mock_open.assert_called_with(Standings._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    def test_start(self):
        game_2449 = filts(json.loads(TESTDATA['2449.json']), GAME_KEYS)
        games = {'2449': game_2449}
        standings = self.create_standings(_data(finished=True, games=games))

        date = encode_datetime(DATE_08310000)
        statsplus_scores = {date: {'2998': 'T31 4, TLA 2'}}
        statsplus_table = {'T40': '0-3', 'T47': '3-0'}
        standings.shadow['statsplus.scores'] = statsplus_scores
        standings.shadow['statsplus.table'] = statsplus_table

        standings._start(date=DATE_10260602)

        write = _data()
        self.assertFalse(standings.shadow['statsplus.scores'])
        self.assertFalse(standings.shadow['statsplus.table'])
        self.mock_open.assert_called_with(Standings._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')

    @mock.patch.object(Standings, '_call')
    def test_index_html(self, mock_call):
        con_al = table(head=[[cell(content='American League')]])
        con_nl = table(head=[[cell(content='National League')]])
        exp_ale = table(head=[[cell(content='AL East')]])
        exp_alc = table(head=[[cell(content='AL Central')]])
        exp_alw = table(head=[[cell(content='AL West')]])
        exp_alwc = table(head=[[cell(content='AL Wild Card')]])
        exp_nle = table(head=[[cell(content='NL East')]])
        exp_nlc = table(head=[[cell(content='NL Central')]])
        exp_nlw = table(head=[[cell(content='NL West')]])
        exp_nlwc = table(head=[[cell(content='NL Wild Card')]])
        body_31 = table(head=[[cell(content='Unofficial (T31)')]])
        body_55 = table(head=[[cell(content='Unofficial (T55)')]])
        body_la = table(head=[[cell(content='Unofficial (TLA)')]])
        body_ny = table(head=[[cell(content='Unofficial (TNY)')]])
        body_2449 = table(head=[[cell(content='Final (2449)')]])
        body_2449 = table(head=[[cell(content='Final (2449)')]])
        foot_2449 = table(foot=[[cell(content='W: P123')]])
        body_2469 = table(head=[[cell(content='Final (2469)')]])
        foot_2469 = table(foot=[[cell(content='W: P456')]])
        body_2476 = table(head=[[cell(content='Final (2476)')]])
        foot_2476 = table(foot=[[cell(content='W: P789')]])
        head_2449 = table(head=[[cell(content='Wednesday')]])
        head_2469 = table(head=[[cell(content='Thursday')]])
        head_2476 = table(head=[[cell(content='Friday')]])
        head_2998 = table(head=[[cell(content='Saturday')]])
        mock_call.side_effect = [
            con_al,
            [exp_ale, exp_alc, exp_alw, exp_alwc],
            con_nl,
            [exp_nle, exp_nlc, exp_nlw, exp_nlwc],
            body_31,
            body_55,
            body_la,
            body_ny,
            body_2449,
            foot_2449,
            body_2469,
            foot_2469,
            body_2476,
            foot_2476,
            head_2998,
            head_2449,
            head_2469,
            head_2476,
            head_2998,
            head_2998,
            head_2449,
            head_2469,
            head_2476,
            head_2998,
            head_2998,
            head_2998,
        ]

        table_ = _table(['T' + str(k) for k in range(31, 61)], {})
        game_2449 = filts(json.loads(TESTDATA['2449.json']), GAME_KEYS)
        game_2469 = filts(json.loads(TESTDATA['2469.json']), GAME_KEYS)
        game_2476 = filts(json.loads(TESTDATA['2476.json']), GAME_KEYS)
        games = {'2449': game_2449, '2469': game_2469, '2476': game_2476}
        standings = self.create_standings(_data(games=games, table_=table_))

        date = encode_datetime(DATE_08310000)
        statsplus_scores = {
            date: {
                '2998': 'T31 4, TLA 2',
                '3000': 'TNY 5, TLA 3',
                '3001': 'TNY 1, T55 0',
            },
        }
        statsplus_table = {'T40': '0-3', 'T47': '3-0'}
        standings.shadow['statsplus.scores'] = statsplus_scores
        standings.shadow['statsplus.table'] = statsplus_table
        standings._reload()

        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Standings'
        }]
        tables = [
            head_2449, body_2449, foot_2449, head_2469, body_2469, foot_2469,
            head_2476, body_2476, foot_2476,
        ]  # yapf: disable
        actual = standings._index_html(date=DATE_10260602)
        expected = {
            'breadcrumbs':
            breadcrumbs,
            'recent': [con_al, con_nl],
            'expanded': [
                exp_ale, exp_alc, exp_alw, exp_alwc, exp_nle, exp_nlc, exp_nlw,
                exp_nlwc,
            ],
            'dialogs': [
                dialog('31', 'Arizona Diamondbacks', [head_2998, body_31]),
                dialog('40', 'Detroit Tigers', tables),
                dialog('44', 'Los Angeles Angels', [head_2998, body_la]),
                dialog('45', 'Los Angeles Dodgers', [head_2998, body_la]),
                dialog('47', 'Minnesota Twins', tables),
                dialog('48', 'New York Yankees', [head_2998, body_ny]),
                dialog('49', 'New York Mets', [head_2998, body_ny]),
                dialog('55', 'San Francisco Giants', [head_2998, body_55]),
            ]
        }  # yapf: disable
        self.assertEqual(actual, expected)

        al_east = ['T33', 'T34', 'T48', 'T57', 'T59']
        al_central = ['T35', 'T38', 'T40', 'T43', 'T47']
        al_west = ['T42', 'T44', 'T50', 'T54', 'T58']
        nl_east = ['T32', 'T41', 'T49', 'T51', 'T60']
        nl_central = ['T36', 'T37', 'T46', 'T52', 'T56']
        nl_west = ['T31', 'T39', 'T45', 'T53', 'T55']

        mock_call.assert_has_calls([
            mock.call('condensed_league', ('American League', [
                ('East', _table(al_east, statsplus_table)),
                ('Central', _table(al_central, statsplus_table)),
                ('West', _table(al_west, statsplus_table)),
            ])),
            mock.call('expanded_league', ('American League', [
                ('East', _table(al_east, table_)),
                ('Central', _table(al_central, table_)),
                ('West', _table(al_west, table_)),
            ])),
            mock.call('condensed_league', ('National League', [
                ('East', _table(nl_east, statsplus_table)),
                ('Central', _table(nl_central, statsplus_table)),
                ('West', _table(nl_west, statsplus_table)),
            ])),
            mock.call('expanded_league', ('National League', [
                ('East', _table(nl_east, table_)),
                ('Central', _table(nl_central, table_)),
                ('West', _table(nl_west, table_)),
            ])),
            mock.call('unofficial_score_body', (['T31 4, TLA 2'], )),
            mock.call('unofficial_score_body', (['TNY 1, T55 0'], )),
            mock.call('unofficial_score_body',
                      (['T31 4, TLA 2', 'TNY 5, TLA 3'], )),
            mock.call('unofficial_score_body',
                      (['TNY 1, T55 0', 'TNY 5, TLA 3'], )),
            mock.call('line_score_body', (game_2449, )),
            mock.call('line_score_foot', (game_2449, )),
            mock.call('line_score_body', (game_2469, )),
            mock.call('line_score_foot', (game_2469, )),
            mock.call('line_score_body', (game_2476, )),
            mock.call('line_score_foot', (game_2476, )),
            mock.call('line_score_head', (date, )),
            mock.call('line_score_head', (game_2449['date'], )),
            mock.call('line_score_head', (game_2469['date'], )),
            mock.call('line_score_head', (game_2476['date'], )),
            mock.call('line_score_head', (date, )),
            mock.call('line_score_head', (date, )),
            mock.call('line_score_head', (game_2449['date'], )),
            mock.call('line_score_head', (game_2469['date'], )),
            mock.call('line_score_head', (game_2476['date'], )),
            mock.call('line_score_head', (date, )),
            mock.call('line_score_head', (date, )),
            mock.call('line_score_head', (date, )),
        ])
        self.assertNotCalled(self.mock_open, self.mock_handle.write)


if __name__ in ['__main__', 'tasks.standings.standings_test']:
    main(
        StandingsTest,
        Standings,
        'tasks.standings',
        'tasks/standings', {},
        __name__ == '__main__',
        date=DATE_10260602,
        e=ENV)
