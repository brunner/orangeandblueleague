#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/plugin/gameday', '', _path)
sys.path.append(_root)
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from plugin.gameday.gameday import Gameday  # noqa
from util.component.component import anchor  # noqa
from util.component.component import bold  # noqa
from util.component.component import secondary  # noqa
from util.component.component import table  # noqa
from util.datetime_.datetime_ import datetime_datetime_pst  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.json_.json_ import dumps  # noqa
from util.test.test import Test  # noqa
from util.test.test import main  # noqa
from util.team.team import logo_absolute  # noqa

_channel = 'C1234'
_env = env()
_now = datetime_datetime_pst(1985, 10, 27, 0, 0, 0)
_then = datetime_datetime_pst(1985, 10, 26, 0, 2, 30)
_ts = '123456789'

_fairylab_root = re.sub(r'/filefairy', '/fairylab/static', _root)

_s31 = logo_absolute('31', anchor('/gameday/2998/', 'Arizona Diamondbacks'),
                     'left')
_s32 = logo_absolute('32', secondary('Atlanta Braves'), 'left')
_s33 = logo_absolute('33', secondary('Baltimore Orioles'), 'left')
_s34 = logo_absolute('34', secondary('Boston Red Sox'), 'left')
_s35 = logo_absolute('35', secondary('Chicago White Sox'), 'left')
_s36 = logo_absolute('36', secondary('Chicago Cubs'), 'left')
_s37 = logo_absolute('37', secondary('Cincinnati Reds'), 'left')
_s38 = logo_absolute('38', secondary('Cleveland Indians'), 'left')
_s39 = logo_absolute('39', secondary('Colorado Rockies'), 'left')
_s40 = logo_absolute('40', secondary('Detroit Tigers'), 'left')
_s41 = logo_absolute('41', secondary('Miami Marlins'), 'left')
_s42 = logo_absolute('42', secondary('Houston Astros'), 'left')
_s43 = logo_absolute('43', secondary('Kansas City Royals'), 'left')
_s44 = logo_absolute('44', secondary('Los Angeles Angels'), 'left')
_s45 = logo_absolute('45', anchor('/gameday/2998/', 'Los Angeles Dodgers'),
                     'left')
_s46 = logo_absolute('46', secondary('Milwaukee Brewers'), 'left')
_s47 = logo_absolute('47', secondary('Minnesota Twins'), 'left')
_s48 = logo_absolute('48', secondary('New York Yankees'), 'left')
_s49 = logo_absolute('49', secondary('New York Mets'), 'left')
_s50 = logo_absolute('50', secondary('Oakland Athletics'), 'left')
_s51 = logo_absolute('51', secondary('Philadelphia Phillies'), 'left')
_s52 = logo_absolute('52', secondary('Pittsburgh Pirates'), 'left')
_s53 = logo_absolute('53', secondary('San Diego Padres'), 'left')
_s54 = logo_absolute('54', secondary('Seattle Mariners'), 'left')
_s55 = logo_absolute('55', secondary('San Francisco Giants'), 'left')
_s56 = logo_absolute('56', secondary('St. Louis Cardinals'), 'left')
_s57 = logo_absolute('57', secondary('Tampa Bay Rays'), 'left')
_s58 = logo_absolute('58', secondary('Texas Rangers'), 'left')
_s59 = logo_absolute('59', secondary('Toronto Blue Jays'), 'left')
_s60 = logo_absolute('60', secondary('Washington Nationals'), 'left')

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

_gameday = {
    'breadcrumbs': [{
        'href': '/',
        'name': 'Fairylab'
    }, {
        'href': '',
        'name': 'Gameday'
    }],
    'schedule': [
        table(
            clazz='table-fixed border border-bottom-0 mt-3',
            head=['American League East']),
        table(
            clazz='table-fixed border',
            bcols=[' class="position-relative text-truncate"'],
            body=[
                [_s33],
                [_s34],
                [_s48],
                [_s57],
                [_s59],
            ]),
        table(
            clazz='table-fixed border border-bottom-0 mt-3',
            head=['American League Central']),
        table(
            clazz='table-fixed border',
            bcols=[' class="position-relative text-truncate"'],
            body=[
                [_s35],
                [_s38],
                [_s40],
                [_s43],
                [_s47],
            ]),
        table(
            clazz='table-fixed border border-bottom-0 mt-3',
            head=['American League West']),
        table(
            clazz='table-fixed border',
            bcols=[' class="position-relative text-truncate"'],
            body=[
                [_s42],
                [_s44],
                [_s50],
                [_s54],
                [_s58],
            ]),
        table(
            clazz='table-fixed border border-bottom-0 mt-3',
            head=['National League East']),
        table(
            clazz='table-fixed border',
            bcols=[' class="position-relative text-truncate"'],
            body=[
                [_s32],
                [_s41],
                [_s49],
                [_s51],
                [_s60],
            ]),
        table(
            clazz='table-fixed border border-bottom-0 mt-3',
            head=['National League Central']),
        table(
            clazz='table-fixed border',
            bcols=[' class="position-relative text-truncate"'],
            body=[
                [_s36],
                [_s37],
                [_s46],
                [_s52],
                [_s56],
            ]),
        table(
            clazz='table-fixed border border-bottom-0 mt-3',
            head=['National League West']),
        table(
            clazz='table-fixed border',
            bcols=[' class="position-relative text-truncate"'],
            body=[
                [_s31],
                [_s39],
                [_s45],
                [_s53],
                [_s55],
            ])
    ]
}

_atbat = '<div class="profile position-absolute {}-{}-front"></div><span ' + \
         'class="align-middle d-block pl-84p">ᴀᴛ ʙᴀᴛ: #{} ({})<br>{}<br>' + \
         '{}</span>'
_pitching = '<div class="profile position-absolute {}-{}-front"></div><sp' + \
            'an class="align-middle d-block pl-84p">ᴘɪᴛᴄʜɪɴɢ: #{} {}ʜᴘ<br' + \
            '>{}<br>{}</span>'

_log_body = [
    ['Pitching: Jim Unknown', ''],
    [_pitching.format('dodgers', 'home', '1', 'ʀ', 'Jim Unknown', '0.0 IP, 0 H, 0 R, 0 BB, 0 K'), ''],
    [_atbat.format('diamondbacks', 'away', '2', 'ꜱ', 'Jim Alpha', '0-0'), ''],
    [Gameday._badge('1', 'Ball'), '1-0'],
    [Gameday._badge('2', 'In play, out(s)'), ''],
    ['Jim Alpha flies out to left fielder  (zone 7LSF). ' + bold('1 out.'), ''],
    ['&nbsp;', '&nbsp;'],
    [_pitching.format('dodgers', 'home', '1', 'ʀ', 'Jim Unknown', '0.1 IP, 0 H, 0 R, 0 BB, 0 K'), ''],
    [_atbat.format('diamondbacks', 'away', '3', 'ʟ', 'Jim Beta', '0-0'), ''],
    [Gameday._badge('1', 'In play, no out'), ''],
    ['Jim Beta singles on a ground ball to left fielder  (zone 56).', ''],
    ['&nbsp;', '&nbsp;'],
    [_pitching.format('dodgers', 'home', '1', 'ʀ', 'Jim Unknown', '0.1 IP, 1 H, 0 R, 0 BB, 0 K'), ''],
    [_atbat.format('diamondbacks', 'away', '4', 'ʀ', 'Jim Charlie', '0-0'), ''],
    [Gameday._badge('1', 'In play, no out'), ''],
    ['Jim Charlie singles on a ground ball to shortstop  (infield hit) (zone 6MS). Jim Beta to second.', ''],
    ['&nbsp;', '&nbsp;'],
    [_pitching.format('dodgers', 'home', '1', 'ʀ', 'Jim Unknown', '0.1 IP, 2 H, 0 R, 0 BB, 0 K'), ''],
    [_atbat.format('diamondbacks', 'away', '5', 'ʀ', 'Jim Delta', '0-0'), ''],
    [Gameday._badge('1', 'In play, out(s)'), ''],
    ['Jim Delta flies out to right fielder  (zone 9). ' + bold('2 out.'), ''],
    ['&nbsp;', '&nbsp;'],
    [_pitching.format('dodgers', 'home', '1', 'ʀ', 'Jim Unknown', '0.2 IP, 2 H, 0 R, 0 BB, 0 K'), ''],
    [_atbat.format('diamondbacks', 'away', '6', 'ʟ', 'Jim Echo', '0-0'), ''],
    [Gameday._badge('1', 'Swinging Strike'), '0-1'],
    [Gameday._badge('2', 'Foul'), '0-2'],
    [Gameday._badge('3', 'Swinging Strike'), '0-3'],
    ['Jim Echo strikes out swinging. ' + bold('3 out.'), '']
]  # yapf: disable

_plays_body = [
    ['Pitching: Jim Unknown'],
    ['Jim Alpha flies out to left fielder  (zone 7LSF). ' + bold('1 out.')],
    ['Jim Beta singles on a ground ball to left fielder  (zone 56).'],
    ['Jim Charlie singles on a ground ball to shortstop  (infield hit) (zone 6MS). Jim Beta to second.'],
    ['Jim Delta flies out to right fielder  (zone 9). ' + bold('2 out.')],
    ['Jim Echo strikes out swinging. ' + bold('3 out.')]
]  # yapf: disable

_r31 = '31/raw/31'
_r45 = '45/raw/45'

_game = {
    'breadcrumbs': [{
        'href': '/',
        'name': 'Fairylab'
    }, {
        'href': '/gameday/',
        'name': 'Gameday'
    }, {
        'href': '',
        'name': 'Diamondbacks at Dodgers, 10/09/2022'
    }],
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
                    hcols=[' colspan="2" class="position-relative"'],
                    bcols=[
                        ' class="position-relative"',
                        ' class="text-center text-secondary w-55p"'
                    ],
                    fcols=[' colspan="2"'],
                    head=[logo_absolute('31', 'Top 1st', 'left')],
                    body=_log_body,
                    foot=[
                        '0 run(s), 2 hit(s), 0 error(s), 2 left on base; '
                        'Arizona Diamondbacks 0 - Los Angeles Dodgers 0'
                    ])
            ]
        }, {
            'name':
            'schedule',
            'title':
            'Schedule',
            'tables': [
                table(
                    clazz='table-fixed border border-bottom-0 mt-3',
                    head=['Arizona Diamondbacks']),
                table(
                    clazz='table-fixed border',
                    body=[
                        [secondary('10/26/1985 @ Los Angeles Dodgers')],
                        [
                            anchor('/gameday/2999/',
                                   '10/27/1985 @ Los Angeles Dodgers')
                        ],
                    ]),
                table(
                    clazz='table-fixed border border-bottom-0 mt-3',
                    head=['Los Angeles Dodgers']),
                table(
                    clazz='table-fixed border',
                    body=[[secondary('10/26/1985 v Arizona Diamondbacks')], [
                        anchor('/gameday/2999/',
                               '10/27/1985 v Arizona Diamondbacks')
                    ]]),
            ]
        }, {
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
                            hcols=[' class="position-relative"'],
                            head=[logo_absolute('31', 'Top 1st', 'left')],
                            body=_plays_body,
                            foot=[
                                '0 run(s), 2 hit(s), 0 error(s), 2 left on '
                                'base; Arizona Diamondbacks 0 - Los Angeles '
                                'Dodgers 0'
                            ])
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
    '2022-10-09T00:00:00-07:00',
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
        'play': [{
            'type': 'sub',
            'subtype': 'P',
            'value': 'P101'
        }, {
            'type': 'matchup',
            'pitcher': {
                'id': 'P101',
                'stats': '0.0 IP, 0 H, 0 R, 0 BB, 0 K'
            },
            'batter': {
                'id': 'P102',
                'stats': '0-0'
            }
        }, {
            'type': 'event',
            'outs': 1,
            'runs': 0,
            'sequence': ['1 1 0 Ball', '2 1 0 In play, out(s)'],
            'value': 'P102 flies out to left fielder  (zone 7LSF).',
        }, {
            'type': 'matchup',
            'pitcher': {
                'id': 'P101',
                'stats': '0.1 IP, 0 H, 0 R, 0 BB, 0 K'
            },
            'batter': {
                'id': 'P103',
                'stats': '0-0'
            }
        }, {
            'type':
            'event',
            'outs':
            0,
            'runs':
            0,
            'sequence': ['1 0 0 In play, no out'],
            'value':
            'P103 singles on a ground ball to left fielder  (zone 56).'
        }, {
            'type': 'matchup',
            'pitcher': {
                'id': 'P101',
                'stats': '0.1 IP, 1 H, 0 R, 0 BB, 0 K'
            },
            'batter': {
                'id': 'P104',
                'stats': '0-0'
            }
        }, {
            'type':
            'event',
            'outs':
            0,
            'runs':
            0,
            'sequence': ['1 0 0 In play, no out'],
            'value':
            'P104 singles on a ground ball to shortstop  (infield hit) '
            '(zone 6MS). P103 to second.'
        }, {
            'type': 'matchup',
            'pitcher': {
                'id': 'P101',
                'stats': '0.1 IP, 2 H, 0 R, 0 BB, 0 K'
            },
            'batter': {
                'id': 'P105',
                'stats': '0-0'
            }
        }, {
            'type': 'event',
            'outs': 1,
            'runs': 0,
            'sequence': ['1 0 0 In play, out(s)'],
            'value': 'P105 flies out to right fielder  (zone 9).'
        }, {
            'type': 'matchup',
            'pitcher': {
                'id': 'P101',
                'stats': '0.2 IP, 2 H, 0 R, 0 BB, 0 K'
            },
            'batter': {
                'id': 'P106',
                'stats': '0-0'
            }
        }, {
            'type':
            'event',
            'outs':
            1,
            'runs':
            0,
            'sequence':
            ['1 0 1 Swinging Strike', '2 0 2 Foul', '3 0 3 Swinging Strike'],
            'value':
            'P106 strikes out swinging.'
        }]
    }]]
}


def _data(games=None, players=None, started=False):
    if games is None:
        games = []
    if players is None:
        players = {}
    return {'games': games, 'players': players, 'started': started}


class GamedayTest(unittest.TestCase):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_chat = mock.patch.object(Gameday, '_chat')
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

    def create_plugin(self, data):
        self.init_mocks(data)
        plugin = Gameday(date=_now, e=_env)

        self.mock_open.assert_called_once_with(Gameday._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    def test_notify__with_start(self):
        plugin = self.create_plugin(_data(started=True))
        response = plugin._notify_internal(notify=Notify.STATSPLUS_SIM)
        self.assertEqual(response, Response())

        write = _data()
        self.mock_open.assert_called_once_with(Gameday._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()

    def test_notify__with_other(self):
        plugin = self.create_plugin(_data(started=True))
        response = plugin._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    def test_on_message(self):
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(Gameday, '_schedule_data')
    @mock.patch('plugin.gameday.gameday.recreate')
    @mock.patch('plugin.gameday.gameday.get_rawid')
    @mock.patch('plugin.gameday.gameday.open')
    @mock.patch('plugin.gameday.gameday.choose_colors')
    def test_render(self, mock_choose, mock_open, mock_rawid, mock_recreate,
                    mock_schedule):
        mock_choose.side_effect = [('white', 'home'), ('grey', 'away')]
        mo = mock.mock_open(read_data=dumps(_game_data))
        mock_open.side_effect = [mo.return_value]
        mock_rawid.side_effect = [_r31, _r45]
        mock_schedule.return_value = {
            'T31': [(_then, 'T45', '@', '2998'), (_now, 'T45', '@', '2999')],
            'T45': [(_then, 'T31', 'v', '2998'), (_now, 'T31', 'v', '2999')],
        }

        plugin = self.create_plugin(_data(games=['2998'], players=_players))
        response = plugin._render_internal(date=_now)
        gameday_index = 'gameday/index.html'
        game_index = 'gameday/2998/index.html'
        subtitle = 'Diamondbacks at Dodgers, 10/09/2022'
        self.assertEqual(response,
                         [(gameday_index, '', 'gameday.html', _gameday),
                          (game_index, subtitle, 'game.html', _game)])

        mock_open.assert_called_once_with(
            _root + '/resource/games/game_2998.json', 'r')
        mock_recreate.assert_called_once_with(_fairylab_root + '/gameday/')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(Gameday, '_render')
    @mock.patch.object(Gameday, '_check_games')
    def test_run__with_check_false(self, mock_check, mock_render):
        mock_check.return_value = False

        plugin = self.create_plugin(_data())
        response = plugin._run_internal(date=_then)
        self.assertEqual(response, Response())

        mock_check.assert_called_once_with()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(Gameday, '_render')
    @mock.patch.object(Gameday, '_check_games')
    def test_run__with_check_true(self, mock_check, mock_render):
        mock_check.return_value = True

        plugin = self.create_plugin(_data())
        response = plugin._run_internal(date=_then)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_then)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(Gameday, '_render')
    def test_setup(self, mock_render):
        plugin = self.create_plugin(_data())
        response = plugin._setup_internal(date=_then)
        self.assertEqual(response, Response())

        mock_render.assert_called_once_with(date=_then)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    def test_shadow(self):
        plugin = self.create_plugin(_data())
        value = plugin._shadow_internal()
        self.assertEqual(value, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch('plugin.gameday.gameday.os.listdir')
    def test_check_games__with_no_change(self, mock_listdir):
        mock_listdir.return_value = ['game_2998.json']

        plugin = self.create_plugin(_data(games=['2998']))
        actual = plugin._check_games()
        self.assertFalse(actual)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch('plugin.gameday.gameday.os.listdir')
    def test_check_games__with_started_false(self, mock_listdir):
        mock_listdir.return_value = ['game_2998.json']

        plugin = self.create_plugin(_data())
        actual = plugin._check_games()
        self.assertTrue(actual)

        write = _data(games=['2998'], started=True)
        self.mock_open.assert_called_once_with(Gameday._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'Live sim created.')

    @mock.patch('plugin.gameday.gameday.os.listdir')
    def test_check_games__with_started_true(self, mock_listdir):
        mock_listdir.return_value = ['game_2998.json']

        plugin = self.create_plugin(_data(started=True))
        actual = plugin._check_games()
        self.assertTrue(actual)

        write = _data(games=['2998'], started=True)
        self.mock_open.assert_called_once_with(Gameday._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()


if __name__ in ['__main__', 'plugin.gameday.gameday_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugin.gameday'
    _pth = 'plugin/gameday'
    main(GamedayTest, Gameday, _pkg, _pth, {}, _main, date=_now, e=_env)
