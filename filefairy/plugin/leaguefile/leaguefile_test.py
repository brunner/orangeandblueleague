#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugin/leaguefile', '', _path)
sys.path.append(_root)
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from plugin.leaguefile.leaguefile import Leaguefile  # noqa
from util.component.component import card  # noqa
from util.component.component import table  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.json_.json_ import dumps  # noqa
from util.secrets.secrets import server  # noqa
from util.test.test import Test  # noqa
from util.test.test import main  # noqa

_data = Leaguefile._data()
_server = server()
DATA = Leaguefile._data()
ENV = env()
CHECK_FILEPART = ('100000', 'Jan 29 16:00',
                  'orange_and_blue_league_baseball.tar.gz.filepart', True)
CHECK_FAST_FALSE = ('328706052', 'Jan 29 15:55',
                    'orange_and_blue_league_baseball.tar.gz', False)
CHECK_SLOW_FALSE = ('328706052', 'Jan 29 07:55',
                    'orange_and_blue_league_baseball.tar.gz', False)
CHECK_UP_FALSE = ('328706052', 'Jan 29 12:55',
                  'orange_and_blue_league_baseball.tar.gz', False)
CHECK_UP_TRUE = ('345678901', 'Jan 27 12:00',
                 'orange_and_blue_league_baseball.tar.gz', True)
FILEPART = {
    'start': 'Jan 29 16:00',
    'size': '100000',
    'end': 'Jan 29 18:00',
    'now': '2018-01-29T15:01:30'
}
SETUP_FILEPART = {
    'start': 'Jan 29 16:00',
    'size': '100000',
    'end': 'Jan 29 16:00',
    'now': '2018-01-29T15:01:30'
}
FAST_FILEPART = {
    'start': 'Jan 29 16:00',
    'size': '328706052',
    'end': 'Jan 29 18:00',
    'date': 'Jan 29 15:55'
}
SLOW_FILEPART = {
    'start': 'Jan 29 16:00',
    'size': '328706052',
    'end': 'Jan 29 18:00',
    'date': 'Jan 29 07:55'
}
UP_FILEPART = {
    'start': 'Jan 29 16:00',
    'size': '328706052',
    'end': 'Jan 29 18:00',
    'date': 'Jan 29 12:55'
}
UP_NOW = {
    'start': 'Jan 29 12:55',
    'size': '328706052',
    'end': 'Jan 29 12:55',
    'date': 'Jan 29 12:55'
}
UP_THEN = {
    'start': 'Jan 27 12:00',
    'size': '345678901',
    'end': 'Jan 27 12:00',
    'date': 'Jan 27 12:00'
}
HOME = {'breadcrumbs': [], 'fp': {}, 'up': {}}
INDEX = 'html/fairylab/leaguefile/index.html'
NOW = datetime.datetime(2018, 1, 29, 15, 1, 30)
THEN = datetime.datetime(2018, 1, 27, 12, 0, 0)
LS_WITH_FILEPART = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 345678901 Jan 27 12:00 orange_and_blue_league_baseball.tar.gz
-rwxrwxrwx 1 user user 100000 Jan 29 16:00 orange_and_blue_league_baseball.tar.gz.filepart
"""
LS_WITHOUT_FILEPART = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 328706052 Jan 29 12:55 orange_and_blue_league_baseball.tar.gz
"""
BREADCRUMBS = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Leaguefile'
}]
TS = '123456789'


class LeaguefileTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_chat = mock.patch.object(Leaguefile, '_chat')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_reactions = mock.patch(
            'plugin.leaguefile.leaguefile.reactions_add')
        self.addCleanup(patch_reactions.stop)
        self.mock_reactions = patch_reactions.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_chat.return_value = {'ok': True, 'ts': TS}

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_chat.reset_mock()
        self.mock_reactions.reset_mock()

    def create_plugin(self, data):
        self.init_mocks(data)
        plugin = Leaguefile(date=NOW, e=ENV)

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return plugin

    def test_notify(self):
        read = {'fp': None, 'up': []}
        plugin = self.create_plugin(read)
        response = plugin._notify_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message(self):
        read = {'fp': None, 'up': []}
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_run__with_valid_input(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_FILEPART, CHECK_UP_TRUE])

        read = {'fp': None, 'up': []}
        plugin = self.create_plugin(read)
        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_START]))

        write = {'fp': SETUP_FILEPART, 'up': []}
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_with('fairylab', 'Upload started.')
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_run__with_no_filepart_change(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_FILEPART, CHECK_UP_TRUE])

        read = {'fp': FILEPART, 'up': [UP_THEN]}
        plugin = self.create_plugin(read)
        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_run__with_no_up_change(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_UP_FALSE])

        read = {'fp': None, 'up': [UP_THEN]}
        plugin = self.create_plugin(read)
        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, Response())

        mock_check.assert_called_once_with()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_run__with_empty_filepart_fast(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_FAST_FALSE])

        read = {'fp': FILEPART, 'up': []}
        plugin = self.create_plugin(read)
        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_FINISH]))

        write = {'fp': None, 'up': [FAST_FILEPART]}
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_reactions.assert_called_once_with('zap', 'fairylab', TS)

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_run__with_empty_filepart_slow(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_SLOW_FALSE])

        read = {'fp': FILEPART, 'up': []}
        plugin = self.create_plugin(read)
        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_FINISH]))

        write = {'fp': None, 'up': [SLOW_FILEPART]}
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        timer = 'timer_clock'
        self.mock_reactions.assert_called_once_with(timer, 'fairylab', TS)

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_run__with_empty_filepart_typical(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_UP_FALSE])

        read = {'fp': FILEPART, 'up': []}
        plugin = self.create_plugin(read)
        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_FINISH]))

        write = {'fp': None, 'up': [UP_FILEPART]}
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_home')
    def test_render(self, mock_home):
        mock_home.return_value = HOME

        read = {'fp': None, 'up': []}
        plugin = self.create_plugin(read)
        response = plugin._render_internal(date=NOW)
        self.assertEqual(response, [(INDEX, '', 'leaguefile.html', HOME)])

        mock_home.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_setup__with_valid_input(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_FILEPART, CHECK_UP_TRUE])

        read = {'fp': None, 'up': []}
        plugin = self.create_plugin(read)
        response = plugin._setup_internal(date=NOW)
        self.assertEqual(response, Response())

        write = {'fp': SETUP_FILEPART, 'up': [UP_THEN]}
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_setup__with_no_filepart_change(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_FILEPART, CHECK_UP_TRUE])

        read = {'fp': FILEPART, 'up': [UP_THEN]}
        plugin = self.create_plugin(read)
        response = plugin._setup_internal(date=NOW)
        self.assertEqual(response, Response())

        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_setup__with_no_up_change(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_UP_TRUE])

        read = {'fp': None, 'up': [UP_THEN]}
        plugin = self.create_plugin(read)
        response = plugin._setup_internal(date=NOW)
        self.assertEqual(response, Response())

        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_setup__with_empty_filepart(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_UP_FALSE])

        read = {'fp': FILEPART, 'up': []}
        plugin = self.create_plugin(read)
        response = plugin._setup_internal(date=NOW)
        self.assertEqual(response, Response())

        write = {'fp': None, 'up': [UP_NOW]}
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check')
    def test_setup__with_new_up(self, mock_check, mock_render):
        mock_check.return_value = iter([CHECK_UP_FALSE])

        read = {'fp': FILEPART, 'up': [UP_THEN]}
        plugin = self.create_plugin(read)
        response = plugin._setup_internal(date=NOW)
        self.assertEqual(response, Response())

        write = {'fp': None, 'up': [UP_NOW, UP_THEN]}
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_shadow(self):
        read = {'fp': None, 'up': [UP_THEN]}
        plugin = self.create_plugin(read)
        value = plugin._shadow_internal()
        self.assertEqual(value, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_filedate(self):
        s = 'Jan 29 15:55'
        actual = Leaguefile._filedate(s)
        expected = 'Jan 29'
        self.assertEqual(actual, expected)

    def test_size(self):
        s = '328706052'
        actual = Leaguefile._size(s)
        expected = '328,706,052'
        self.assertEqual(actual, expected)

    def test_time(self):
        s = 'Jan 29 14:00'
        e = 'Jan 29 16:00'
        actual = Leaguefile._time(s, e)
        expected = '2h 0m'
        self.assertEqual(actual, expected)

    @mock.patch('plugin.leaguefile.leaguefile.check_output')
    def test_check__with_filepart(self, mock_check):
        mock_check.return_value = {'ok': True, 'output': LS_WITH_FILEPART}

        actual = Leaguefile._check()
        expected = iter([CHECK_FILEPART, CHECK_UP_TRUE])
        self.assertCountEqual(actual, expected)

        mock_check.assert_called_once_with(
            [
                'ssh', 'brunnerj@' + _server,
                'ls -l /var/www/html/StatsLab/league_file'
            ],
            timeout=8)

    @mock.patch('plugin.leaguefile.leaguefile.check_output')
    def test_check__without_filepart(self, mock_check):
        mock_check.return_value = {'ok': True, 'output': LS_WITHOUT_FILEPART}

        actual = Leaguefile._check()
        expected = iter([CHECK_UP_FALSE])
        self.assertCountEqual(actual, expected)

        mock_check.assert_called_once_with(
            [
                'ssh', 'brunnerj@' + _server,
                'ls -l /var/www/html/StatsLab/league_file'
            ],
            timeout=8)

    def test_home__with_empty(self):
        read = {'fp': None, 'up': []}
        plugin = self.create_plugin(read)
        value = plugin._home(date=NOW)
        up = table(
            hcols=['', '', ''],
            bcols=['', '', ''],
            head=['Date', 'Time', 'Size'],
            body=[])
        expected = {'breadcrumbs': BREADCRUMBS, 'fp': None, 'up': up}
        self.assertEqual(value, expected)

    def test_home__with_filepart(self):
        read = {'fp': FILEPART, 'up': []}
        plugin = self.create_plugin(read)
        value = plugin._home(date=NOW)
        fp = card(
            title='Jan 29',
            table=table(
                clazz='table-sm',
                hcols=['', ' class="w-100"'],
                bcols=['', ' class="w-100"'],
                body=[['Time: ', '2h 0m'], ['Size: ', '100,000']]),
            ts='0s ago',
            success='ongoing')
        up = table(
            hcols=['', '', ''],
            bcols=['', '', ''],
            head=['Date', 'Time', 'Size'],
            body=[])
        expected = {'breadcrumbs': BREADCRUMBS, 'fp': fp, 'up': up}
        self.assertEqual(value, expected)

    def test_home__with_up(self):
        read = {'fp': None, 'up': [UP_THEN]}
        plugin = self.create_plugin(read)
        value = plugin._home(date=NOW)
        up = table(
            hcols=['', '', ''],
            bcols=['', '', ''],
            head=['Date', 'Time', 'Size'],
            body=[['Jan 27', '0m', '345,678,901']])
        expected = {'breadcrumbs': BREADCRUMBS, 'fp': None, 'up': up}
        self.assertEqual(value, expected)


if __name__ in ['__main__', 'plugin.leaguefile.leaguefile_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugin.leaguefile'
    _pth = 'plugin/leaguefile'
    main(LeaguefileTest, Leaguefile, _pkg, _pth, {}, _main, date=NOW, e=ENV)
