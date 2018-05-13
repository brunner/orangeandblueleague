#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import mock
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugins/recap', '', _path)
sys.path.append(_root)
from plugins.recap.recap_plugin import RecapPlugin  # noqa
from utils.component.component_util import table  # noqa
from utils.jinja2.jinja2_util import env  # noqa
from utils.json.json_util import dumps  # noqa
from utils.test.test_util import TestUtil  # noqa
from utils.test.test_util import main  # noqa
from utils.unicode.unicode_util import deunicode  # noqa
from value.notify.notify_value import NotifyValue  # noqa
from value.response.response_value import ResponseValue  # noqa

_leagues = os.path.join(_root, 'file/news/txt/leagues')
_injuries = os.path.join(_leagues, 'league_100_injuries.txt')
_news = os.path.join(_leagues, 'league_100_news.txt')
_transactions = os.path.join(_leagues, 'league_100_transactions.txt')

DATA = RecapPlugin._data()
NOW = datetime.datetime(1985, 10, 26, 0, 2, 30)
INJ_AFTER = '20220817\t<a href=\"../teams/team_47.html\">Minnesota Twins</a>: 1B <a href=\"../players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
INJ_BEFORE = '20220815\t<a href=\"../teams/team_44.html\">Los Angeles Angels</a>: CF <a href=\"../players/player_0.html\">Alex Aristy</a> was injured while running the bases.  The Diagnosis: knee inflammation. He\'s expected to miss about 3 weeks.'
INJ_CONTENT = '20220817\t<a href=\"../teams/team_57.html\">Tampa Bay Rays</a>: <a href=\"../players/player_1.html\">Zack Weiss</a> diagnosed with a strained hamstring, will miss 4 weeks.\n20220817\t<a href=\"../teams/team_39.html\">Colorado Rockies</a>: RF <a href=\"../players/player_24198.html\">Eddie Hoffman</a> was injured being hit by a pitch.  The Diagnosis: bruised knee. This is a day-to-day injury expected to last 5 days.'
INJ_HASH = '965572a66c'
INJ_UPDATE = {'content': INJ_CONTENT, 'hash': INJ_HASH}
INJ_CALL = mock.call('injuries', _injuries)
INJ_TABLE = table(
    clazz='border mt-3',
    hcols=[''],
    bcols=[''],
    head=['Wednesday, August 17th, 2022'],
    body=[[
        'Minnesota Twins: 1B <a href=\"/StatsLab/reports/news/html/players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
    ]])
NEWS_AFTER = '20220818\t<a href=\"../teams/team_41.html\">Miami Marlins</a>: <a href=\"../players/player_131.html\">Jake Ehret</a> got suspended 3 games after ejection following a brawl.'
NEWS_BEFORE = '20220815\t<a href=\"../teams/team_57.html\">Tampa Bay Rays</a>: <a href=\"../players/player_27.html\">A.J. Reed</a> got suspended 4 games after ejection following arguing a strike call.'
NEWS_CONTENT = '20220818\t<a href=\"../teams/team_42.html\">Houston Astros</a>: <a href=\"../players/player_39044.html\">Mark Appel</a> pitches a 2-hit shutout against the <a href=\"../teams/team_44.html\">Los Angeles Angels</a> with 8 strikeouts and 0 BB allowed!\n20220818\t<a href=\"../teams/team_39.html\">Colorado Rockies</a>: <a href=\"../players/player_30965.html\">Spencer Taylor</a> got suspended 3 games after ejection following a brawl.'
NEWS_HASH = '2b9934d013'
NEWS_UPDATE = {'content': NEWS_CONTENT, 'hash': NEWS_HASH}
NEWS_CALL = mock.call('news', _news)
NEWS_TABLE = table(
    clazz='border mt-3',
    hcols=[''],
    bcols=[''],
    head=['Thursday, August 18th, 2022'],
    body=[[
        'Miami Marlins: <a href=\"/StatsLab/reports/news/html/players/player_131.html\">Jake Ehret</a> got suspended 3 games after ejection following a brawl.'
    ]])
TRANS_AFTER = '20220815\t<a href=\"../teams/team_33.html\">Baltimore Orioles</a>: Placed C <a href=\"../players/player_31093.html\">Salvador Perez</a> on waivers.\n'
TRANS_BEFORE = '20220815\t<a href=\"../teams/team_33.html\">Baltimore Orioles</a>: Placed 2B <a href=\"../players/player_292.html\">Austin Slater</a> on the 7-day disabled list, retroactive to 08/12/2022.\n'
TRANS_CONTENT = '20220815\t<a href=\"../teams/team_33.html\">Baltimore Orioles</a>: Placed C <a href=\"../players/player_1439.html\">Evan Skoug</a> on the active roster.\n\n20220815\t<a href=\"../teams/team_33.html\">Baltimore Orioles</a>: Activated C <a href=\"../players/player_1439.html\">Evan Skoug</a> from the disabled list.\n'
TRANS_HASH = 'a17f312e8e'
TRANS_UPDATE = {'content': TRANS_CONTENT, 'hash': TRANS_HASH}
TRANS_CALL = mock.call('transactions', _transactions)
TRANS_TABLE = table(
    clazz='border mt-3',
    hcols=[''],
    bcols=[''],
    head=['Monday, August 15th, 2022'],
    body=[[
        'Baltimore Orioles: Placed C <a href=\"/StatsLab/reports/news/html/players/player_31093.html\">Salvador Perez</a> on waivers.'
    ]])
TABLE_MAP = {
    'injuries': [INJ_TABLE],
    'news': [NEWS_TABLE],
    'transactions': [TRANS_TABLE]
}
UPDATE_MAP = {
    'injuries': INJ_UPDATE,
    'news': NEWS_UPDATE,
    'transactions': TRANS_UPDATE
}
AFTER_MAP = {
    'injuries': {
        'content': INJ_AFTER,
        'hash': INJ_HASH
    },
    'news': {
        'content': NEWS_AFTER,
        'hash': NEWS_HASH
    },
    'transactions': {
        'content': TRANS_AFTER,
        'hash': TRANS_HASH
    }
}
LINE = '<a href=\"../teams/team_47.html\">Minnesota Twins</a>: 1B <a href=\"../players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
LINE_STRIPPED = 'Minnesota Twins: 1B <a href=\"../players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
LINE_REWRITTEN = '<a href=\"../teams/team_47.html\">Minnesota Twins</a>: 1B <a href=\"/StatsLab/reports/news/html/players/player_34032.html\">Nick Castellanos</a> was injured while running the bases.  The Diagnosis: sprained ankle. This is a day-to-day injury expected to last 5 days.'
HOME = {'breadcrumbs': [], 'injuries': [], 'news': [], 'transactions': []}
INDEX = 'html/fairylab/recap/index.html'
BREADCRUMBS = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Recap'
}]
READ = {'standings': {}}
RECORDS1 = {'T31': '76-86', 'T45': '97-65'}
RECORDS2 = {'T32': '77-85', 'T44': '70-92'}
RECORDS3 = {'T31': '75-86', 'T45': '97-64'}


class RecapPluginTest(TestUtil):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable_api.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()
        patch_chat = mock.patch('plugins.recap.recap_plugin.chat_post_message')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

    def init_mocks(self, read):
        mo = mock.mock_open(read_data=dumps(read))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_chat.reset_mock()

    def create_plugin(self, read):
        self.init_mocks(read)
        plugin = RecapPlugin(e=env())

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.assertEqual(plugin.data, read)

        self.reset_mocks()
        self.init_mocks({})

        return plugin

    @mock.patch.object(RecapPlugin, '_standings')
    @mock.patch.object(RecapPlugin, '_render')
    def test_notify__with_download(self, mock_render, mock_standings):
        plugin = self.create_plugin(READ)
        value = plugin._notify_internal(notify=NotifyValue.DOWNLOAD_FINISH)
        self.assertTrue(value)

        mock_render.assert_called_once_with(notify=NotifyValue.DOWNLOAD_FINISH)
        mock_standings.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_called_once_with(
            'fairylab',
            'League news updated.',
            attachments=plugin._attachments())

    @mock.patch.object(RecapPlugin, '_standings')
    @mock.patch.object(RecapPlugin, '_render')
    def test_notify__with_other(self, mock_render, mock_standings):
        plugin = self.create_plugin(READ)
        value = plugin._notify_internal(notify=NotifyValue.OTHER)
        self.assertFalse(value)

        mock_render.assert_not_called()
        mock_standings.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    def test_on_message(self):
        plugin = self.create_plugin(READ)
        response = plugin._on_message_internal()
        self.assertEqual(response, ResponseValue())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    def test_run(self):
        plugin = self.create_plugin(READ)
        response = plugin._run_internal()
        self.assertEqual(response, ResponseValue())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(RecapPlugin, '_home')
    def test_render(self, mock_home):
        mock_home.return_value = HOME

        plugin = self.create_plugin(READ)
        value = plugin._render_internal(date=NOW)
        self.assertEqual(value, [(INDEX, '', 'recap.html', HOME)])

        mock_home.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch.object(RecapPlugin, '_render')
    def test_setup(self, mock_render):
        plugin = self.create_plugin(READ)
        plugin._setup_internal(date=NOW)

        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    def test_shadow(self):
        plugin = self.create_plugin(READ)
        value = plugin._shadow_internal()
        self.assertEqual(value, {})

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    def test_strip_teams(self):
        actual = RecapPlugin._strip_teams(LINE)
        expected = LINE_STRIPPED
        self.assertEqual(actual, expected)

    def test_rewrite_players(self):
        actual = RecapPlugin._rewrite_players(LINE)
        expected = LINE_REWRITTEN
        self.assertEqual(actual, expected)

    @mock.patch.object(RecapPlugin, '_tables')
    def test_home(self, mock_tables):
        plugin = self.create_plugin(READ)

        def fake_tables(*args, **kwargs):
            key = args[0]
            return TABLE_MAP.get(key)

        mock_tables.side_effect = fake_tables

        value = plugin._home(date=NOW)
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'injuries': [INJ_TABLE],
            'news': [NEWS_TABLE],
            'transactions': [TRANS_TABLE]
        }
        self.assertEqual(value, expected)

        mock_tables.assert_has_calls([
            mock.call('injuries'),
            mock.call('news'),
            mock.call('transactions')
        ])
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch('plugins.recap.recap_plugin.records')
    @mock.patch('plugins.recap.recap_plugin.os.listdir')
    def test_standings(self, mock_listdir, mock_records):
        boxes = ['123', '456', '789']
        mock_listdir.return_value = [
            'game_box_{}.html'.format(b) for b in boxes
        ]
        mock_records.side_effect = [RECORDS1, RECORDS2, RECORDS3]

        plugin = self.create_plugin(READ)
        plugin._standings()
        expected = RECORDS1.copy()
        expected.update(RECORDS2)
        self.assertEqual(plugin.data['standings'], expected)

        dpath = os.path.join(_root, 'extract/box_scores')
        mock_listdir.assert_called_once_with(dpath)
        calls = [
            mock.call(os.path.join(dpath, 'game_box_{}.html'.format(b)))
            for b in boxes
        ]
        mock_records.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch('plugins.recap.recap_plugin.open', create=True)
    def test_tables__injuries(self, mock_open):
        mo = mock.mock_open(read_data=INJ_AFTER)
        mock_open.side_effect = [mo.return_value]

        plugin = self.create_plugin(READ)
        actual = plugin._tables('injuries')
        expected = [INJ_TABLE]
        self.assertEqual(actual, expected)

        dpath = os.path.join(_root, 'extract/leagues/{}.txt')
        mock_open.assert_called_once_with(dpath.format('injuries'), 'r')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch('plugins.recap.recap_plugin.open', create=True)
    def test_tables__news(self, mock_open):
        mo = mock.mock_open(read_data=NEWS_AFTER)
        mock_open.side_effect = [mo.return_value]

        plugin = self.create_plugin(READ)
        actual = plugin._tables('news')
        expected = [NEWS_TABLE]
        self.assertEqual(actual, expected)

        dpath = os.path.join(_root, 'extract/leagues/{}.txt')
        mock_open.assert_called_once_with(dpath.format('news'), 'r')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()

    @mock.patch('plugins.recap.recap_plugin.open', create=True)
    def test_tables__transactions(self, mock_open):
        mo = mock.mock_open(read_data=TRANS_AFTER)
        mock_open.side_effect = [mo.return_value]

        plugin = self.create_plugin(READ)
        actual = plugin._tables('transactions')
        expected = [TRANS_TABLE]
        self.assertEqual(actual, expected)

        dpath = os.path.join(_root, 'extract/leagues/{}.txt')
        mock_open.assert_called_once_with(dpath.format('transactions'), 'r')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()


if __name__ in ['__main__', 'plugins.recap.recap_plugin_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugins.recap'
    _pth = 'plugins/recap'
    main(RecapPluginTest, RecapPlugin, _pkg, _pth, {}, _main)
