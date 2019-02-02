#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/tasks/oldgameday', '', _path)
sys.path.append(_root)

from common.elements.elements import anchor  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.teams.teams import icon_absolute  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from tasks.oldgameday.oldgameday import Oldgameday  # noqa

_channel = 'C1234'
_env = env()
_now = datetime_datetime_pst(1985, 10, 27, 0, 0, 0)
_then = datetime_datetime_pst(1985, 10, 26, 0, 2, 30)
_ts = '123456789'


def bold(text):
    return span(['text-bold'], text)


def secondary(text):
    return span(['text-secondary'], text)


_fairylab_root = re.sub(r'/filefairy', '/fairylab/static', _root)

_s31 = icon_absolute('T31', anchor('/oldgameday/2998/',
                                   'Arizona Diamondbacks'))
_s32 = icon_absolute('T32', secondary('Atlanta Braves'))
_s33 = icon_absolute('T33', secondary('Baltimore Orioles'))
_s34 = icon_absolute('T34', secondary('Boston Red Sox'))
_s35 = icon_absolute('T35', secondary('Chicago White Sox'))
_s36 = icon_absolute('T36', secondary('Chicago Cubs'))
_s37 = icon_absolute('T37', secondary('Cincinnati Reds'))
_s38 = icon_absolute('T38', secondary('Cleveland Indians'))
_s39 = icon_absolute('T39', secondary('Colorado Rockies'))
_s40 = icon_absolute('T40', secondary('Detroit Tigers'))
_s41 = icon_absolute('T41', secondary('Miami Marlins'))
_s42 = icon_absolute('T42', secondary('Houston Astros'))
_s43 = icon_absolute('T43', secondary('Kansas City Royals'))
_s44 = icon_absolute('T44', secondary('Los Angeles Angels'))
_s45 = icon_absolute('T45', anchor('/oldgameday/2998/', 'Los Angeles Dodgers'))
_s46 = icon_absolute('T46', secondary('Milwaukee Brewers'))
_s47 = icon_absolute('T47', secondary('Minnesota Twins'))
_s48 = icon_absolute('T48', secondary('New York Yankees'))
_s49 = icon_absolute('T49', secondary('New York Mets'))
_s50 = icon_absolute('T50', secondary('Oakland Athletics'))
_s51 = icon_absolute('T51', secondary('Philadelphia Phillies'))
_s52 = icon_absolute('T52', secondary('Pittsburgh Pirates'))
_s53 = icon_absolute('T53', secondary('San Diego Padres'))
_s54 = icon_absolute('T54', secondary('Seattle Mariners'))
_s55 = icon_absolute('T55', secondary('San Francisco Giants'))
_s56 = icon_absolute('T56', secondary('St. Louis Cardinals'))
_s57 = icon_absolute('T57', secondary('Tampa Bay Rays'))
_s58 = icon_absolute('T58', secondary('Texas Rangers'))
_s59 = icon_absolute('T59', secondary('Toronto Blue Jays'))
_s60 = icon_absolute('T60', secondary('Washington Nationals'))

_players = {
    'P101': {
        'name': 'Jim Unknown',
        'number': '1',
        'bats': 'R',
        'throws': 'R'
    },
    'P102': {
        'name': 'Jim Alpha',
        'number': '2',
        'bats': 'S',
        'throws': 'R'
    },
    'P103': {
        'name': 'Jim Beta',
        'number': '3',
        'bats': 'L',
        'throws': 'R'
    },
    'P104': {
        'name': 'Jim Charlie',
        'number': '4',
        'bats': 'R',
        'throws': 'R'
    },
    'P105': {
        'name': 'Jim Delta',
        'number': '5',
        'bats': 'R',
        'throws': 'R'
    },
    'P106': {
        'name': 'Jim Echo',
        'number': '6',
        'bats': 'L',
        'throws': 'R'
    }
}

_oldgameday = {
    'schedule': [
        table(
            clazz='table-fixed border border-bottom-0 mt-3',
            head=[[cell(content='American League East')]]),
        table(
            clazz='table-fixed border',
            bcols=[col(clazz='position-relative text-truncate')],
            body=[
                [cell(content=_s33)],
                [cell(content=_s34)],
                [cell(content=_s48)],
                [cell(content=_s57)],
                [cell(content=_s59)],
            ]),
        table(
            clazz='table-fixed border border-bottom-0 mt-3',
            head=[[cell(content='American League Central')]]),
        table(
            clazz='table-fixed border',
            bcols=[col(clazz='position-relative text-truncate')],
            body=[
                [cell(content=_s35)],
                [cell(content=_s38)],
                [cell(content=_s40)],
                [cell(content=_s43)],
                [cell(content=_s47)],
            ]),
        table(
            clazz='table-fixed border border-bottom-0 mt-3',
            head=[[cell(content='American League West')]]),
        table(
            clazz='table-fixed border',
            bcols=[col(clazz='position-relative text-truncate')],
            body=[
                [cell(content=_s42)],
                [cell(content=_s44)],
                [cell(content=_s50)],
                [cell(content=_s54)],
                [cell(content=_s58)],
            ]),
        table(
            clazz='table-fixed border border-bottom-0 mt-3',
            head=[[cell(content='National League East')]]),
        table(
            clazz='table-fixed border',
            bcols=[col(clazz='position-relative text-truncate')],
            body=[
                [cell(content=_s32)],
                [cell(content=_s41)],
                [cell(content=_s49)],
                [cell(content=_s51)],
                [cell(content=_s60)],
            ]),
        table(
            clazz='table-fixed border border-bottom-0 mt-3',
            head=[[cell(content='National League Central')]]),
        table(
            clazz='table-fixed border',
            bcols=[col(clazz='position-relative text-truncate')],
            body=[
                [cell(content=_s36)],
                [cell(content=_s37)],
                [cell(content=_s46)],
                [cell(content=_s52)],
                [cell(content=_s56)],
            ]),
        table(
            clazz='table-fixed border border-bottom-0 mt-3',
            head=[[cell(content='National League West')]]),
        table(
            clazz='table-fixed border',
            bcols=[col(clazz='position-relative text-truncate')],
            body=[
                [cell(content=_s31)],
                [cell(content=_s39)],
                [cell(content=_s45)],
                [cell(content=_s53)],
                [cell(content=_s55)],
            ])
    ]
}

_player = '<div class="profile position-absolute {}-{}-front"></div><span ' + \
          'class="align-middle d-block pl-84p">{}: {} #{} ({})<br>{}<br>' + \
          '{}</span>'

_log_body = [
    [cell(col=col(clazz='bg-light', colspan='2'), content=_player.format('dodgers', 'home', 'ᴘɪᴛᴄʜɪɴɢ', 'sᴘ', '1', 'ʀ', 'Jim Unknown', '0.0 IP, 0 H, 0 R, 0 BB, 0 K'))],
    [cell(col=col(clazz='bg-light', colspan='2'), content=_player.format('diamondbacks', 'away', 'ᴀᴛ ʙᴀᴛ', 'ss', '2', 's', 'Jim Alpha', '0-0'))],
    [cell(content=Oldgameday._pitch('1', 'Ball')), cell(content='1-0')],
    [cell(col=col(colspan='2'), content=Oldgameday._pitch('2', 'In play, out(s)'))],
    [cell(col=col(colspan='2'), content=('Jim Alpha flies out to left fielder  (zone 7LSF). ' + bold('1 out.')))],
    [cell(col=col(clazz='bg-light', colspan='2'), content=_player.format('dodgers', 'home', 'ᴘɪᴛᴄʜɪɴɢ', 'sᴘ', '1', 'ʀ', 'Jim Unknown', '0.1 IP, 0 H, 0 R, 0 BB, 0 K'))],
    [cell(col=col(clazz='bg-light', colspan='2'), content=_player.format('diamondbacks', 'away', 'ᴀᴛ ʙᴀᴛ', 'ʟꜰ', '3', 'ʟ', 'Jim Beta', '0-0'))],
    [cell(col=col(colspan='2'), content=Oldgameday._pitch('1', 'In play, no out'))],
    [cell(col=col(colspan='2'), content='Jim Beta singles on a ground ball to left fielder  (zone 56).')],
    [cell(col=col(clazz='bg-light', colspan='2'), content=_player.format('dodgers', 'home', 'ᴘɪᴛᴄʜɪɴɢ', 'sᴘ', '1', 'ʀ', 'Jim Unknown', '0.1 IP, 1 H, 0 R, 0 BB, 0 K'))],
    [cell(col=col(clazz='bg-light', colspan='2'), content=_player.format('diamondbacks', 'away', 'ᴀᴛ ʙᴀᴛ', '1ʙ', '4', 'ʀ', 'Jim Charlie', '0-0'))],
    [cell(col=col(colspan='2'), content=Oldgameday._pitch('1', 'In play, no out'))],
    [cell(col=col(colspan='2'), content='Jim Charlie singles on a ground ball to shortstop  (infield hit) (zone 6MS). Jim Beta to second.')],
    [cell(col=col(clazz='bg-light', colspan='2'), content=_player.format('dodgers', 'home', 'ᴘɪᴛᴄʜɪɴɢ', 'sᴘ', '1', 'ʀ', 'Jim Unknown', '0.1 IP, 2 H, 0 R, 0 BB, 0 K'))],
    [cell(col=col(clazz='bg-light', colspan='2'), content=_player.format('diamondbacks', 'away', 'ᴀᴛ ʙᴀᴛ', 'ʀꜰ', '5', 'ʀ', 'Jim Delta', '0-0'))],
    [cell(col=col(colspan='2'), content=Oldgameday._pitch('1', 'In play, out(s)'))],
    [cell(col=col(colspan='2'), content=('Jim Delta flies out to right fielder  (zone 9). ' + bold('2 out.')))],
    [cell(col=col(clazz='bg-light', colspan='2'), content=_player.format('dodgers', 'home', 'ᴘɪᴛᴄʜɪɴɢ', 'sᴘ', '1', 'ʀ', 'Jim Unknown', '0.2 IP, 2 H, 0 R, 0 BB, 0 K'))],
    [cell(col=col(clazz='bg-light', colspan='2'), content=_player.format('diamondbacks', 'away', 'ᴀᴛ ʙᴀᴛ', 'ᴄ', '6', 'ʟ', 'Jim Echo', '0-0'))],
    [cell(content=Oldgameday._pitch('1', 'Swinging Strike')), cell(content='0-1')],
    [cell(content=Oldgameday._pitch('2', 'Foul')), cell(content='0-2')],
    [cell(content=Oldgameday._pitch('3', 'Swinging Strike')), cell(content='0-3')],
    [cell(col=col(colspan='2'), content=('Jim Echo strikes out swinging. ' + bold('3 out.')))]
]  # yapf: disable

_plays_body = [
    [cell(content=('Jim Alpha flies out to left fielder  (zone 7LSF). ' + bold('1 out.')))],
    [cell(content='Jim Beta singles on a ground ball to left fielder  (zone 56).')],
    [cell(content='Jim Charlie singles on a ground ball to shortstop  (infield hit) (zone 6MS). Jim Beta to second.')],
    [cell(content=('Jim Delta flies out to right fielder  (zone 9). ' + bold('2 out.')))],
    [cell(content=('Jim Echo strikes out swinging. ' + bold('3 out.')))]
]  # yapf: disable

_r31 = '31/raw/31'
_r45 = '45/raw/45'

_statslab_link = ('https://orangeandblueleaguebaseball.com/StatsLab/'
                  'reports/news/html/')
_game_box_link = 'box_scores/game_box_2998.html'
_log_link = 'game_logs/log_2998.html'
_game = {
    'jerseys': [
        ('diamondbacks', 'away', _r31),
        ('dodgers', 'home', _r45),
    ],
    'tabs': {
        'style':
        'tabs',
        'tabs': [{
            'name':
            'log',
            'title':
            'Game Log',
            'tables': [
                table(
                    clazz='border mt-3',
                    hcols=[col(clazz='position-relative', colspan='2')],
                    bcols=[
                        col(clazz='position-relative'),
                        col(clazz='text-center text-secondary w-55p')
                    ],
                    fcols=[col(colspan='2')],
                    head=[[cell(content=icon_absolute('T31', 'Top 1st'))]],
                    body=_log_body,
                    foot=[[
                        cell(
                            content=('0 run(s), 2 hit(s), 0 error(s), 2 left '
                                     'on base; Arizona Diamondbacks 0 - '
                                     'Los Angeles Dodgers 0'))
                    ]])
            ]
        },
                 {
                     'name':
                     'links',
                     'title':
                     'Links',
                     'tables': [
                         table(
                             clazz='table-fixed border border-bottom-0 mt-3',
                             head=[[cell(content='Oldgameday Sources')]]),
                         table(
                             clazz='table-fixed border',
                             body=[
                                 [
                                     cell(
                                         content=anchor(
                                             _statslab_link + _game_box_link,
                                             '10/26/1985 StatsLab Game Box'))
                                 ],
                                 [
                                     cell(
                                         content=anchor(
                                             _statslab_link + _log_link,
                                             '10/26/1985 StatsLab Log'))
                                 ],
                             ]),
                         table(
                             clazz='table-fixed border border-bottom-0 mt-3',
                             head=[[
                                 cell(content='Arizona Diamondbacks Schedule')
                             ]]),
                         table(
                             clazz='table-fixed border',
                             body=[
                                 [
                                     cell(
                                         content=secondary(
                                             '10/26/1985 @ Los Angeles Dodgers'
                                         ))
                                 ],
                                 [
                                     cell(
                                         content=anchor(
                                             '/oldgameday/2999/',
                                             '10/27/1985 @ Los Angeles Dodgers'
                                         ))
                                 ],
                             ]),
                         table(
                             clazz='table-fixed border border-bottom-0 mt-3',
                             head=[[
                                 cell(content='Los Angeles Dodgers Schedule')
                             ]]),
                         table(
                             clazz='table-fixed border',
                             body=[
                                 [
                                     cell(
                                         content=secondary(
                                             '10/26/1985 v Arizona Diamondbacks'
                                         ))
                                 ],
                                 [
                                     cell(
                                         content=anchor(
                                             '/oldgameday/2999/',
                                             '10/27/1985 v Arizona Diamondbacks'
                                         ))
                                 ]
                             ]),
                     ]
                 },
                 {
                     'name': 'plays',
                     'title': 'Plays',
                     'tabs': {
                         'style':
                         'pills',
                         'tabs': [{
                             'name':
                             'plays-1',
                             'title':
                             '1',
                             'tables': [
                                 table(
                                     clazz='border mt-3',
                                     hcols=[col(clazz='position-relative')],
                                     head=[[
                                         cell(
                                             content=icon_absolute(
                                                 'T31', 'Top 1st'))
                                     ]],
                                     body=_plays_body,
                                     foot=[[
                                         cell(
                                             content=
                                             '0 run(s), 2 hit(s), 0 error(s), '
                                             '2 left on base; Arizona Diamondbacks 0 '
                                             '- Los Angeles Dodgers 0')
                                     ]])
                             ]
                         }]
                     }
                 }]
    }
}
_game_data = {
    'id':
    '2998',
    'away_team':
    'T31',
    'home_team':
    'T45',
    'date':
    '1985-10-26T00:00:00-07:00',
    'players': ['101', '102', '103', '104', '105', '106'],
    'plays': [[{
        'label':
        'Top 1st',
        'batting':
        'T31',
        'pitching':
        'P101',
        'footer':
        '0 run(s), 2 hit(s), 0 error(s), 2 left on base; T31 0 - T45 0',
        'play': [
            {
                'type': 'matchup',
                'pitcher': {
                    'id': 'P101',
                    'pos': 'SP',
                    'stats': '0.0 IP, 0 H, 0 R, 0 BB, 0 K'
                },
                'batter': {
                    'id': 'P102',
                    'pos': 'SS',
                    'stats': '0-0'
                }
            },
            {
                'type': 'event',
                'batter': 'P102',
                'outs': 1,
                'runs': 0,
                'sequence': ['1 1 0 Ball', '2 1 0 In play, out(s)'],
                'value': 'P102 flies out to left fielder  (zone 7LSF).',
            },
            {
                'type': 'matchup',
                'pitcher': {
                    'id': 'P101',
                    'pos': 'SP',
                    'stats': '0.1 IP, 0 H, 0 R, 0 BB, 0 K'
                },
                'batter': {
                    'id': 'P103',
                    'pos': 'LF',
                    'stats': '0-0'
                }
            },
            {
                'type':
                'event',
                'batter':
                'P103',
                'outs':
                0,
                'runs':
                0,
                'sequence': ['1 0 0 In play, no out'],
                'value':
                'P103 singles on a ground ball to left fielder  (zone 56).'
            },
            {
                'type': 'matchup',
                'pitcher': {
                    'id': 'P101',
                    'pos': 'SP',
                    'stats': '0.1 IP, 1 H, 0 R, 0 BB, 0 K'
                },
                'batter': {
                    'id': 'P104',
                    'pos': '1B',
                    'stats': '0-0'
                }
            },
            {
                'type':
                'event',
                'batter':
                'P104',
                'outs':
                0,
                'runs':
                0,
                'sequence': ['1 0 0 In play, no out'],
                'value':
                'P104 singles on a ground ball to shortstop  (infield hit) '
                '(zone 6MS). P103 to second.'
            },
            {
                'type': 'matchup',
                'pitcher': {
                    'id': 'P101',
                    'pos': 'SP',
                    'stats': '0.1 IP, 2 H, 0 R, 0 BB, 0 K'
                },
                'batter': {
                    'id': 'P105',
                    'pos': 'RF',
                    'stats': '0-0'
                }
            },
            {
                'type': 'event',
                'batter': 'P105',
                'outs': 1,
                'runs': 0,
                'sequence': ['1 0 0 In play, out(s)'],
                'value': 'P105 flies out to right fielder  (zone 9).'
            },
            {
                'type': 'matchup',
                'pitcher': {
                    'id': 'P101',
                    'pos': 'SP',
                    'stats': '0.2 IP, 2 H, 0 R, 0 BB, 0 K'
                },
                'batter': {
                    'id': 'P106',
                    'pos': 'C',
                    'stats': '0-0'
                }
            },
            {
                'type':
                'event',
                'batter':
                'P106',
                'outs':
                1,
                'runs':
                0,
                'sequence': [
                    '1 0 1 Swinging Strike', '2 0 2 Foul',
                    '3 0 3 Swinging Strike'
                ],
                'value':
                'P106 strikes out swinging.'
            }
        ]
    }]]
}


def _data(games=None, players=None, started=False):
    if games is None:
        games = []
    if players is None:
        players = {}
    return {'games': games, 'players': players, 'started': started}


class OldgamedayTest(unittest.TestCase):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_chat = mock.patch.object(Oldgameday, '_chat')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_chat.return_value = {
            'ok': True,
            'channel': _channel,
            'ts': _ts
        }

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_chat.reset_mock()

    def create_oldgameday(self, data):
        self.init_mocks(data)
        oldgameday = Oldgameday(date=_now, e=_env)

        self.mock_open.assert_called_once_with(Oldgameday._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return oldgameday

    def test_notify__with_start(self):
        oldgameday = self.create_oldgameday(_data(games=['2998']))
        response = oldgameday._notify_internal(notify=Notify.STATSPLUS_START)
        self.assertEqual(response, Response())

        write = _data()
        self.mock_open.assert_called_once_with(Oldgameday._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()

    def test_notify__with_other(self):
        oldgameday = self.create_oldgameday(_data(games=['2998']))
        response = oldgameday._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    # @mock.patch.object(Oldgameday, '_schedule_data')
    # @mock.patch('tasks.oldgameday.oldgameday.recreate')
    # @mock.patch('tasks.oldgameday.oldgameday.get_rawid')
    # @mock.patch('tasks.oldgameday.oldgameday.open')
    # @mock.patch('tasks.oldgameday.oldgameday.choose_colors')
    # def test_render_data(self, mock_choose, mock_open, mock_rawid, mock_recreate,
    #                 mock_schedule):
    #     mock_choose.side_effect = [('white', 'home'), ('grey', 'away')]
    #     mo = mock.mock_open(read_data=dumps(_game_data))
    #     mock_open.side_effect = [mo.return_value]
    #     mock_rawid.side_effect = [_r31, _r45]
    #     mock_schedule.return_value = {
    #         'T31': [(_then, 'T45', '@', '2998'), (_now, 'T45', '@', '2999')],
    #         'T45': [(_then, 'T31', 'v', '2998'), (_now, 'T31', 'v', '2999')],
    #     }

    #     oldgameday = self.create_oldgameday(_data(games=['2998'], players=_players))
    #     response = oldgameday._render_data(date=_now)
    #     oldgameday_index = 'oldgameday/index.html'
    #     game_index = 'oldgameday/2998/index.html'
    #     subtitle = 'Diamondbacks at Dodgers, 10/26/1985'
    #     self.assertEqual(response,
    #                      [(oldgameday_index, '', 'oldgameday.html', _oldgameday),
    #                       (game_index, subtitle, 'oldgame.html', _game)])

    #     mock_open.assert_called_once_with(
    #         _root + '/resource/games/game_2998.json', 'r')
    #     mock_recreate.assert_called_once_with(_fairylab_root + '/oldgameday/')
    #     self.mock_open.assert_not_called()
    #     self.mock_handle.write.assert_not_called()
    #     self.mock_chat.assert_not_called()

    @mock.patch.object(Oldgameday, '_render')
    @mock.patch.object(Oldgameday, '_check_games')
    def test_run__with_check_false(self, mock_check, mock_render):
        mock_check.return_value = False

        oldgameday = self.create_oldgameday(_data())
        response = oldgameday._run_internal(date=_then)
        self.assertEqual(response, Response())

        mock_check.assert_called_once_with()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(Oldgameday, '_render')
    @mock.patch.object(Oldgameday, '_check_games')
    def test_run__with_check_true(self, mock_check, mock_render):
        mock_check.return_value = True

        oldgameday = self.create_oldgameday(_data())
        response = oldgameday._run_internal(date=_then)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_then)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch('tasks.oldgameday.oldgameday.os.listdir')
    def test_check_games__with_no_change(self, mock_listdir):
        mock_listdir.return_value = ['game_2998.json']

        oldgameday = self.create_oldgameday(_data(games=['2998']))
        actual = oldgameday._check_games()
        self.assertFalse(actual)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch('tasks.oldgameday.oldgameday.os.listdir')
    def test_check_games__with_started_false(self, mock_listdir):
        mock_listdir.return_value = ['game_2998.json']

        oldgameday = self.create_oldgameday(_data())
        actual = oldgameday._check_games()
        self.assertTrue(actual)

        write = _data(games=['2998'], started=True)
        self.mock_open.assert_called_once_with(Oldgameday._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'Live sim created.')

    @mock.patch('tasks.oldgameday.oldgameday.os.listdir')
    def test_check_games__with_started_true(self, mock_listdir):
        mock_listdir.return_value = ['game_2998.json']

        oldgameday = self.create_oldgameday(_data(started=True))
        actual = oldgameday._check_games()
        self.assertTrue(actual)

        write = _data(games=['2998'], started=True)
        self.mock_open.assert_called_once_with(Oldgameday._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()


if __name__ in ['__main__', 'tasks.oldgameday.oldgameday_test']:
    _main = __name__ == '__main__'
    _pkg = 'tasks.oldgameday'
    _pth = 'tasks/oldgameday'
    main(OldgamedayTest, Oldgameday, _pkg, _pth, {}, _main, date=_now, e=_env)