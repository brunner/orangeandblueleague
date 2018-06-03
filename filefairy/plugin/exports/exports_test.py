#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import datetime
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugin/exports', '', _path))
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from plugin.exports.exports import Exports  # noqa
from util.component.component import card  # noqa
from util.component.component import span  # noqa
from util.component.component import table  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.json_.json_ import dumps  # noqa
from util.team.team import logo_absolute  # noqa
from util.test.test import Test  # noqa
from util.test.test import main  # noqa

DATA = Exports._data()
ENV = env()
EXPORTS_100 = [('31', 'New'), ('32', 'New'), ('33', 'New')]
EXPORTS_LOCK = [('31', 'New'), ('32', 'Old'), ('33', 'New')]
EXPORTS_OLD = [('31', 'Old'), ('32', 'Old'), ('33', 'Old')]
EXPORTS_NEW = [('31', 'New'), ('32', 'Old'), ('33', 'Old')]
EXPORTS_NEW_HOME = [('33', 'New'), ('34', 'New'), ('35', 'New'), ('40', 'New'),
                    ('42', 'New'), ('44', 'New')]
EXPORTS_OLD_HOME = [('33', 'New'), ('34', 'New'), ('35', 'New'), ('40', 'New'),
                    ('42', 'Old'), ('44', 'Old')]
HOME = {'breadcrumbs': [], 'table': {}}
INDEX = 'html/fairylab/exports/index.html'
NOW = datetime.datetime(1985, 10, 26, 0, 2, 30)
NOW_ENCODED = '1985-10-26T00:02:30'
FORM_CANONICAL = ''
FORM_TRUNCATED = 'nonnnonnno'
FORM_ALIVE = 'ooooooooon'
FORM_DEAD = 'nooooooooo'
FORM_EMPTY = ''
FORM_NEW = 'n'
FORM_NEW_TRUNCATED = 'onnnonnnon'
FORM_OLD = 'o'
FORM_OLD_TRUNCATED = 'onnnonnnoo'
INFO_LOCK = 'Ongoing sim contains <span class="text-success border px-1">4 new</span>, 2 old, <span class="text-secondary">0 ai</span>.'
INFO_NEW = 'Upcoming sim contains <span class="text-success border px-1">6 new</span>, 0 old, <span class="text-secondary">0 ai</span>.'
INFO_OLD = 'Upcoming sim contains <span class="text-success border px-1">4 new</span>, 2 old, <span class="text-secondary">0 ai</span>.'
TABLE = table(body=[['AL East', 'BAL', 'BOS']])
THEN = datetime.datetime(1985, 10, 26, 0, 0, 0)
THEN_ENCODED = '1985-10-26T00:00:00'
URL = 'https://orangeandblueleaguebaseball.com/StatsLab/exports.php'
URLOPEN = '<html><head><title>Export Tracker - StatsLab for ...'
BREADCRUMBS = [{
    'href': '/fairylab/',
    'name': 'Home'
}, {
    'href': '',
    'name': 'Exports'
}]
TABLE_COLS = [''] + [' class="text-center"'] * 2
STANDINGS_COLS = [
    'class="position-relative"', ' class="text-center w-25"',
    ' class="text-center w-25"'
]
TS = '123456789'


class ExportsTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_urlopen = mock.patch('plugin.exports.exports.urlopen')
        self.addCleanup(patch_urlopen.stop)
        self.mock_urlopen = patch_urlopen.start()

        patch_chat = mock.patch.object(Exports, '_chat')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_log = mock.patch('plugin.exports.exports.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_reactions = mock.patch('plugin.exports.exports.reactions_add')
        self.addCleanup(patch_reactions.stop)
        self.mock_reactions = patch_reactions.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_urlopen.return_value = bytes(URLOPEN, 'utf-8')
        self.mock_chat.return_value = {'ok': True, 'ts': TS}

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_urlopen.reset_mock()
        self.mock_chat.reset_mock()
        self.mock_log.reset_mock()
        self.mock_reactions.reset_mock()

    def create_plugin(self, data, exports=None):
        self.init_mocks(data)
        plugin = Exports(date=NOW, e=ENV)

        self.mock_open.assert_called_once_with(DATA, 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        if exports:
            plugin.exports = exports

        return plugin

    @mock.patch.object(Exports, '_unlock_internal')
    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock_internal')
    def test_notify__with_unlocked_other(self, mock_lock, mock_render,
                                         mock_unlock):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read)
        response = plugin._notify_internal(notify=Notify.OTHER, date=NOW)
        self.assertEqual(response, Response())

        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        mock_unlock.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Exports, '_unlock_internal')
    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock_internal')
    def test_notify__with_unlocked_sim(self, mock_lock, mock_render,
                                       mock_unlock):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read)

        form = {k: copy.deepcopy(FORM_NEW) for k in ['31', '32', '33']}

        def fake_lock(*args, **kwargs):
            plugin.data['form'] = form
            plugin.data['locked'] = True

        mock_lock.side_effect = fake_lock

        response = plugin._notify_internal(
            notify=Notify.STATSPLUS_SIM, date=NOW)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = {'ai': [], 'date': NOW_ENCODED, 'form': form, 'locked': True}
        mock_lock.assert_called_once_with()
        mock_render.assert_called_once_with(
            notify=Notify.STATSPLUS_SIM, date=NOW)
        mock_unlock.assert_not_called()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_with(dumps(write) + '\n')
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Exports, '_unlock_internal')
    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock_internal')
    def test_notify__with_unlocked_file(self, mock_lock, mock_render,
                                        mock_unlock):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read)
        response = plugin._notify_internal(
            notify=Notify.LEAGUEFILE_FINISH, date=NOW)
        self.assertEqual(response, Response())

        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        mock_unlock.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Exports, '_unlock_internal')
    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock_internal')
    def test_notify__with_locked_other(self, mock_lock, mock_render,
                                       mock_unlock):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': True}
        plugin = self.create_plugin(read)
        response = plugin._notify_internal(notify=Notify.OTHER, date=NOW)
        self.assertEqual(response, Response())

        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        mock_unlock.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Exports, '_unlock_internal')
    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock_internal')
    def test_notify__with_locked_sim(self, mock_lock, mock_render,
                                     mock_unlock):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': True}
        plugin = self.create_plugin(read)
        response = plugin._notify_internal(
            notify=Notify.STATSPLUS_SIM, date=NOW)
        self.assertEqual(response, Response())

        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        mock_unlock.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Exports, '_unlock_internal')
    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock_internal')
    def test_notify__with_locked_file(self, mock_lock, mock_render,
                                      mock_unlock):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': True}
        plugin = self.create_plugin(read)

        def fake_unlock(*args, **kwargs):
            plugin.data['locked'] = False

        mock_unlock.side_effect = fake_unlock

        response = plugin._notify_internal(
            notify=Notify.LEAGUEFILE_FINISH, date=NOW)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = {'ai': [], 'date': NOW_ENCODED, 'form': form, 'locked': False}
        mock_lock.assert_not_called()
        mock_render.assert_called_once_with(
            notify=Notify.LEAGUEFILE_FINISH, date=NOW)
        mock_unlock.assert_called_once_with()
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message(self):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read)
        response = plugin._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock_internal')
    @mock.patch.object(Exports, '_exports')
    def test_run__with_exports_new(self, mock_exports, mock_lock, mock_render):
        mock_exports.return_value = EXPORTS_NEW

        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD)
        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = {'ai': [], 'date': NOW_ENCODED, 'form': form, 'locked': False}
        mock_exports.assert_called_once_with(URLOPEN)
        mock_lock.assert_not_called()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_called_once_with(URL)
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_NEW)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock_internal')
    @mock.patch.object(Exports, '_exports')
    def test_run__with_exports_old(self, mock_exports, mock_lock, mock_render):
        mock_exports.return_value = EXPORTS_OLD

        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD)
        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, Response())

        mock_exports.assert_called_once_with(URLOPEN)
        mock_lock.assert_not_called()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(URL)
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_OLD)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock_internal')
    @mock.patch.object(Exports, '_exports')
    def test_run__with_exports_ai(self, mock_exports, mock_lock, mock_render):
        mock_exports.return_value = EXPORTS_NEW

        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {
            'ai': ['31', '32', '33'],
            'date': THEN_ENCODED,
            'form': form,
            'locked': False
        }
        plugin = self.create_plugin(read, exports=EXPORTS_OLD)
        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = {
            'ai': ['32', '33'],
            'date': NOW_ENCODED,
            'form': form,
            'locked': False
        }
        mock_exports.assert_called_once_with(URLOPEN)
        mock_lock.assert_not_called()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_called_once_with(URL)
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_NEW)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock_internal')
    @mock.patch.object(Exports, '_exports')
    def test_run__with_exports_empty(self, mock_exports, mock_lock,
                                     mock_render):
        mock_exports.return_value = []

        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD)
        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, Response())

        mock_exports.assert_called_once_with(URLOPEN)
        mock_lock.assert_not_called()
        mock_render.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(URL)
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_OLD)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock_internal')
    @mock.patch.object(Exports, '_exports')
    def test_run__with_exports_lock_internal(self, mock_exports, mock_lock,
                                             mock_render):
        mock_exports.return_value = EXPORTS_LOCK

        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_NEW)

        def fake_lock(*args, **kwargs):
            plugin.data['locked'] = True

        mock_lock.side_effect = fake_lock

        response = plugin._run_internal(date=NOW)
        self.assertEqual(response, Response(notify=[Notify.EXPORTS_EMAILS]))

        write = {'ai': [], 'date': NOW_ENCODED, 'form': form, 'locked': True}
        mock_exports.assert_called_once_with(URLOPEN)
        mock_lock.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_urlopen.assert_called_once_with(URL)
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_LOCK)

    @mock.patch.object(Exports, '_home')
    def test_render(self, mock_home):
        mock_home.return_value = HOME

        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD)
        value = plugin._render_internal(date=NOW)
        self.assertEqual(value, [(INDEX, '', 'exports.html', HOME)])

        mock_home.assert_called_once_with(date=NOW)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_OLD)

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_exports')
    def test_setup(self, mock_exports, mock_render):
        mock_exports.return_value = EXPORTS_OLD

        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read)
        response = plugin._setup_internal()
        self.assertEqual(response, Response())

        mock_exports.assert_called_once_with(URLOPEN)
        mock_render.assert_called_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_called_once_with(URL)
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_OLD)

    def test_shadow(self):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read)
        value = plugin._shadow_internal()
        self.assertEqual(value, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_exports__with_valid_input(self):
        text = '<td><a href="../teams/team_36.html">Chicago Cubs</a>' + \
               '<br><span>February 3, 2018<br>New Export</span></td>' + \
               '<td><a href="../teams/team_37.html">Cincinnati Reds</a>' + \
               '<br><span>February 3, 2018<br>Old Export</span></td>'
        actual = Exports._exports(text)
        expected = [('36', 'New'), ('37', 'Old')]
        self.assertEqual(actual, expected)

    def test_exports__with_invalid_input(self):
        text = '<td></td>'
        actual = Exports._exports(text)
        expected = []
        self.assertEqual(actual, expected)

    @mock.patch.object(Exports, '_table')
    @mock.patch.object(Exports, '_sorted')
    @mock.patch('plugin.exports.exports.divisions')
    def test_home__without_old(self, mock_divisions, mock_sorted, mock_table):
        mock_divisions.return_value = [('AL East', ['33', '34']),
                                       ('AL Central', ['35', '40']),
                                       ('AL West', ['42', '44'])]
        mock_sorted.side_effect = ['BAL', 'BOS', 'CWS', 'DET', 'HOU', 'LAA']
        mock_table.return_value = TABLE

        keys = ['33', '34', '35', '40', '42', '44']
        form = {k: copy.deepcopy(FORM_NEW) for k in keys}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_NEW_HOME)
        response = plugin._home(date=THEN)
        l = card(title='100%', info=INFO_NEW, table=TABLE, ts='0s ago')
        e = table(
            hcols=STANDINGS_COLS,
            bcols=STANDINGS_COLS,
            head=['AL East', 'Last 10', 'Streak'],
            body=[[logo_absolute('33', 'Baltimore', 'left'), '1 - 0', 'W1'],
                  [logo_absolute('34', 'Boston', 'left'), '1 - 0', 'W1']])
        c = table(
            hcols=STANDINGS_COLS,
            bcols=STANDINGS_COLS,
            head=['AL Central', 'Last 10', 'Streak'],
            body=[[logo_absolute('35', 'Chicago', 'left'), '1 - 0', 'W1'],
                  [logo_absolute('40', 'Detroit', 'left'), '1 - 0', 'W1']])
        w = table(
            hcols=STANDINGS_COLS,
            bcols=STANDINGS_COLS,
            head=['AL West', 'Last 10', 'Streak'],
            body=[[logo_absolute('42', 'Houston', 'left'), '1 - 0', 'W1'],
                  [logo_absolute('44', 'Los Angeles', 'left'), '1 - 0', 'W1']])
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'live': l,
            'standings': [e, c, w]
        }
        self.assertEqual(response, expected)

        mock_divisions.assert_called_once_with()
        calls = [mock.call(k) for k in ['33', '34', '35', '40', '42', '44']]
        mock_sorted.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Exports, '_table')
    @mock.patch.object(Exports, '_sorted')
    @mock.patch('plugin.exports.exports.divisions')
    def test_home__with_old(self, mock_divisions, mock_sorted, mock_table):
        mock_divisions.return_value = [('AL East', ['33', '34']),
                                       ('AL Central', ['35', '40']),
                                       ('AL West', ['42', '44'])]
        mock_sorted.side_effect = ['BAL', 'BOS', 'CWS', 'DET', 'HOU', 'LAA']
        mock_table.return_value = TABLE

        keys = ['33', '34', '35', '40', '42', '44']
        form = {k: copy.deepcopy(FORM_NEW) for k in keys}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD_HOME)
        response = plugin._home(date=THEN)
        l = card(title='67%', info=INFO_OLD, table=TABLE, ts='0s ago')
        e = table(
            hcols=STANDINGS_COLS,
            bcols=STANDINGS_COLS,
            head=['AL East', 'Last 10', 'Streak'],
            body=[[logo_absolute('33', 'Baltimore', 'left'), '1 - 0', 'W1'],
                  [logo_absolute('34', 'Boston', 'left'), '1 - 0', 'W1']])
        c = table(
            hcols=STANDINGS_COLS,
            bcols=STANDINGS_COLS,
            head=['AL Central', 'Last 10', 'Streak'],
            body=[[logo_absolute('35', 'Chicago', 'left'), '1 - 0', 'W1'],
                  [logo_absolute('40', 'Detroit', 'left'), '1 - 0', 'W1']])
        w = table(
            hcols=STANDINGS_COLS,
            bcols=STANDINGS_COLS,
            head=['AL West', 'Last 10', 'Streak'],
            body=[[logo_absolute('42', 'Houston', 'left'), '1 - 0', 'W1'],
                  [logo_absolute('44', 'Los Angeles', 'left'), '1 - 0', 'W1']])
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'live': l,
            'standings': [e, c, w]
        }
        self.assertEqual(response, expected)

        mock_divisions.assert_called_once_with()
        calls = [mock.call(k) for k in ['33', '34', '35', '40', '42', '44']]
        mock_sorted.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Exports, '_table')
    @mock.patch.object(Exports, '_sorted')
    @mock.patch('plugin.exports.exports.divisions')
    def test_home__with_lock_internal(self, mock_divisions, mock_sorted,
                                      mock_table):
        mock_divisions.return_value = [('AL East', ['33', '34']),
                                       ('AL Central', ['35', '40']),
                                       ('AL West', ['42', '44'])]
        mock_sorted.side_effect = ['BAL', 'BOS', 'CWS', 'DET', 'HOU', 'LAA']
        mock_table.return_value = TABLE

        keys = ['33', '34', '35', '40', '42', '44']
        form = {k: copy.deepcopy(FORM_NEW) for k in keys}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': True}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD_HOME)
        response = plugin._home(date=THEN)
        l = card(title='67%', info=INFO_LOCK, table=TABLE, ts='0s ago')
        e = table(
            hcols=STANDINGS_COLS,
            bcols=STANDINGS_COLS,
            head=['AL East', 'Last 10', 'Streak'],
            body=[[logo_absolute('33', 'Baltimore', 'left'), '1 - 0', 'W1'],
                  [logo_absolute('34', 'Boston', 'left'), '1 - 0', 'W1']])
        c = table(
            hcols=STANDINGS_COLS,
            bcols=STANDINGS_COLS,
            head=['AL Central', 'Last 10', 'Streak'],
            body=[[logo_absolute('35', 'Chicago', 'left'), '1 - 0', 'W1'],
                  [logo_absolute('40', 'Detroit', 'left'), '1 - 0', 'W1']])
        w = table(
            hcols=STANDINGS_COLS,
            bcols=STANDINGS_COLS,
            head=['AL West', 'Last 10', 'Streak'],
            body=[[logo_absolute('42', 'Houston', 'left'), '1 - 0', 'W1'],
                  [logo_absolute('44', 'Los Angeles', 'left'), '1 - 0', 'W1']])
        expected = {
            'breadcrumbs': BREADCRUMBS,
            'live': l,
            'standings': [e, c, w]
        }
        self.assertEqual(response, expected)

        mock_divisions.assert_called_once_with()
        calls = [mock.call(k) for k in ['33', '34', '35', '40', '42', '44']]
        mock_sorted.assert_has_calls(calls)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_lock_internal')
    def test_lock(self, mock_lock, mock_render):
        form = {k: copy.deepcopy(FORM_TRUNCATED) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_LOCK)
        plugin.lock(date=NOW)

        write = {'ai': [], 'date': NOW_ENCODED, 'form': form, 'locked': False}
        mock_lock.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_log.assert_called_once_with(
            'Exports', date=NOW, s='Locked tracker.')
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Exports, '_render')
    @mock.patch.object(Exports, '_unlock_internal')
    def test_unlock(self, mock_unlock, mock_render):
        form = {k: copy.deepcopy(FORM_TRUNCATED) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_LOCK)
        plugin.unlock(date=NOW)

        write = {'ai': [], 'date': NOW_ENCODED, 'form': form, 'locked': False}
        mock_unlock.assert_called_once_with()
        mock_render.assert_called_once_with(date=NOW)
        self.mock_open.assert_called_once_with(DATA, 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_log.assert_called_once_with(
            'Exports', date=NOW, s='Unlocked tracker.')
        self.mock_reactions.assert_not_called()

    def test_lock_internal__with_truncation(self):
        form = {k: copy.deepcopy(FORM_TRUNCATED) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_LOCK)
        plugin._lock_internal()

        form = {
            '31': FORM_NEW_TRUNCATED,
            '32': FORM_OLD_TRUNCATED,
            '33': FORM_NEW_TRUNCATED
        }
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.data['ai'], [])
        self.assertEqual(plugin.data['form'], form)
        self.assertTrue(plugin.data['locked'], True)
        self.assertEqual(plugin.exports, EXPORTS_LOCK)

    def test_lock_internal__with_ai_added(self):
        form = {k: copy.deepcopy(FORM_DEAD) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_LOCK)
        plugin._lock_internal()

        form = {'31': FORM_ALIVE, '32': FORM_EMPTY, '33': FORM_ALIVE}
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.data['ai'], ['32'])
        self.assertEqual(plugin.data['form'], form)
        self.assertTrue(plugin.data['locked'], True)
        self.assertEqual(plugin.exports, EXPORTS_LOCK)

    def test_lock_internal__with_100(self):
        form = {k: copy.deepcopy(FORM_TRUNCATED) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_100)
        plugin._lock_internal()

        form = {
            '31': FORM_NEW_TRUNCATED,
            '32': FORM_NEW_TRUNCATED,
            '33': FORM_NEW_TRUNCATED
        }
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_called_once_with('100', 'fairylab', TS)
        self.assertEqual(plugin.data['ai'], [])
        self.assertEqual(plugin.data['form'], form)
        self.assertTrue(plugin.data['locked'], True)
        self.assertEqual(plugin.exports, EXPORTS_100)

    def test_lock_internal__with_palm_tree(self):
        form = {k: copy.deepcopy(FORM_TRUNCATED) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD)
        plugin._lock_internal()

        form = {
            '31': FORM_OLD_TRUNCATED,
            '32': FORM_OLD_TRUNCATED,
            '33': FORM_OLD_TRUNCATED
        }
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_called_once_with('fairylab', 'Tracker locked.')
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_called_once_with('palm_tree', 'fairylab', TS)
        self.assertEqual(plugin.data['ai'], [])
        self.assertEqual(plugin.data['form'], form)
        self.assertTrue(plugin.data['locked'], True)
        self.assertEqual(plugin.exports, EXPORTS_OLD)

    def test_new(self):
        form = {k: copy.deepcopy(FORM_CANONICAL) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_NEW)

        actual = plugin._new()
        expected = (1, 3)
        self.assertEqual(actual, expected)

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_streak(self):
        form = {'31': FORM_NEW_TRUNCATED, '32': FORM_OLD_TRUNCATED}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read)

        actual = plugin._streak('31')
        expected = 'W1'
        self.assertEqual(actual, expected)
        actual = plugin._streak('32')
        expected = 'L2'
        self.assertEqual(actual, expected)

    @mock.patch('plugin.exports.exports.teamid_to_abbreviation')
    def test_sorted(self, mock_name):
        mock_name.side_effect = ['ARI', 'ATL']

        form = {'31': FORM_NEW_TRUNCATED, '32': FORM_OLD_TRUNCATED}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD)

        actual = plugin._sorted('31')
        expected = [-0.7, -7, -1, -float(1) / 3, 'ARI']
        mock_name.assert_called_once_with('31')
        self.assertEqual(actual, expected)

        mock_name.reset_mock()

        actual = plugin._sorted('32')
        expected = [-0.6, -6, 2, -0.25, 'ATL']
        mock_name.assert_called_once_with('32')
        self.assertEqual(actual, expected)

    @mock.patch('plugin.exports.exports.divisions')
    def test_table(self, mock_divisions):
        mock_divisions.return_value = [('AL East', ['33', '34']),
                                       ('AL Central', ['35', '40']),
                                       ('AL West', ['42', '44'])]

        keys = ['33', '34', '35', '40', '42', '44']
        form = {k: copy.deepcopy(FORM_NEW) for k in keys}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': False}
        plugin = self.create_plugin(read, exports=EXPORTS_OLD_HOME)
        actual = plugin._table()
        body = [[
            'AL East',
            span(['text-success', 'border', 'px-1'], 'BAL'),
            span(['text-success', 'border', 'px-1'], 'BOS')
        ], [
            'AL Central',
            span(['text-success', 'border', 'px-1'], 'CWS'),
            span(['text-success', 'border', 'px-1'], 'DET')
        ], ['AL West', 'HOU', 'LAA']]
        expected = table(
            clazz='table-sm', hcols=TABLE_COLS, bcols=TABLE_COLS, body=body)
        self.assertEqual(actual, expected)

    def test_unlock_internal(self):
        form = {k: copy.deepcopy(FORM_TRUNCATED) for k in ['31', '32', '33']}
        read = {'ai': [], 'date': THEN_ENCODED, 'form': form, 'locked': True}
        plugin = self.create_plugin(read, exports=EXPORTS_LOCK)
        plugin._unlock_internal()

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_urlopen.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(plugin.exports, EXPORTS_LOCK)
        self.assertFalse(plugin.data['locked'])


if __name__ in ['__main__', 'plugin.exports.exports_test']:
    _main = __name__ == '__main__'
    _pkg = 'plugin.exports'
    _pth = 'plugin/exports'
    main(ExportsTest, Exports, _pkg, _pth, {}, _main, date=NOW, e=ENV)
