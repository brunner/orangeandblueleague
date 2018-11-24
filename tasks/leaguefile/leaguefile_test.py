#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/tasks/leaguefile', '', _path)
sys.path.append(_root)
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa
from data.thread_.thread_ import Thread  # noqa
from tasks.leaguefile.leaguefile import Leaguefile  # noqa
from common.elements.elements import card  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.datetime_.datetime_ import datetime_datetime_pst  # noqa
from common.jinja2_.jinja2_ import env  # noqa
from common.json_.json_ import dumps  # noqa
from common.secrets.secrets import server  # noqa
from common.test.test import Test  # noqa
from common.test.test import main  # noqa

FILE_HOST = 'www.orangeandblueleaguebaseball.com'
FILE_NAME = 'orange_and_blue_league_baseball.tar.gz'
FILE_URL = 'https://{}/StatsLab/league_file/{}'.format(FILE_HOST, FILE_NAME)

_channel = 'C1234'
_env = env()
_now = datetime_datetime_pst(2018, 1, 29)
_now_encoded = '2018-01-29T00:00:00-08:00'
_server = server()
_then = datetime_datetime_pst(2018, 1, 28)
_then_encoded = '2018-01-28T00:00:00-08:00'
_ts = '123456789'
_year = datetime_datetime_pst(2019, 1, 1)
_year_encoded = '2019-01-01T00:00:00-08:00'


def _data(completed=[],
          date=_then_encoded,
          download=None,
          now=_now_encoded,
          stalled=False,
          then=_then_encoded,
          upload=None):
    return {
        'completed': completed,
        'date': date,
        'download': download,
        'now': now,
        'stalled': stalled,
        'then': then,
        'upload': upload
    }


class LeaguefileTest(Test):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_chat = mock.patch.object(Leaguefile, '_chat')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_log = mock.patch('tasks.leaguefile.leaguefile._logger.log')
        self.addCleanup(patch_log.stop)
        self.mock_log = patch_log.start()

        patch_reactions = mock.patch(
            'tasks.leaguefile.leaguefile.reactions_add')
        self.addCleanup(patch_reactions.stop)
        self.mock_reactions = patch_reactions.start()

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
        self.mock_log.reset_mock()
        self.mock_reactions.reset_mock()

    def create_leaguefile(self, data):
        self.init_mocks(data)
        leaguefile = Leaguefile(date=_now, e=_env)

        self.mock_open.assert_called_once_with(Leaguefile._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertEqual(leaguefile.data, data)

        self.reset_mocks()
        self.init_mocks(data)

        return leaguefile

    def test_notify(self):
        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._notify_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message(self):
        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._on_message_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_valid_input(self, mock_check_download,
                                   mock_check_upload, mock_download,
                                   mock_render):
        check_u = ('100000', 'Jan 29 16:00',
                   'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_c = ('345678901', 'Jan 27 12:00',
                   'orange_and_blue_league_baseball.tar.gz', True)
        mock_check_upload.return_value = iter([check_u, check_c])

        read = _data()
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.LEAGUEFILE_START]))

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 16:00',
            'now': '2018-01-29T00:00:00-08:00'
        }
        write = _data(upload=upload)
        mock_check_download.assert_not_called()
        mock_check_upload.assert_called_once_with()
        mock_download.assert_not_called()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_with('fairylab', 'Upload started.')
        self.mock_log.assert_called_once_with(logging.INFO, 'Upload started.')
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_no_change(self, mock_check_download, mock_check_upload,
                                 mock_download, mock_render):
        check_u = ('100000', 'Jan 29 16:00',
                   'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_c = ('345678901', 'Jan 27 12:00',
                   'orange_and_blue_league_baseball.tar.gz', True)
        mock_check_upload.return_value = iter([check_u, check_c])

        upload = {
            'start': 'Jan 29 15:00',
            'size': '100000',
            'end': 'Jan 29 16:00',
            'now': '2018-01-29T16:02:00-08:00'
        }
        completed = {
            'size': '345678901',
            'date': 'Jan 27 12:00',
            'dstart': 'Jan 27 12:00',
            'dend': 'Jan 27 12:00',
            'ustart': 'Jan 27 12:00',
            'uend': 'Jan 27 12:00'
        }
        leaguefile = self.create_leaguefile(
            _data(upload=upload, completed=[completed]))
        response = leaguefile._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        mock_check_download.assert_not_called()
        mock_check_upload.assert_called_once_with()
        mock_download.assert_not_called()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_file_is_up_fast(self, mock_check_download,
                                       mock_check_upload, mock_download,
                                       mock_render):
        check = ('328706052', 'Jan 29 15:55',
                 'orange_and_blue_league_baseball.tar.gz', False)
        mock_check_upload.return_value = iter([check])
        thread_ = Thread(target='_download_internal', kwargs={'date': _now})
        mock_download.return_value = Response(thread_=[thread_])

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00-08:00'
        }
        completed = {
            'size': '345678901',
            'date': 'Jan 27 12:00',
            'dstart': 'Jan 27 12:00',
            'dend': 'Jan 27 12:00',
            'ustart': 'Jan 27 8:00',
            'uend': 'Jan 27 12:00'
        }
        leaguefile = self.create_leaguefile(
            _data(upload=upload, completed=[completed]))
        response = leaguefile._run_internal(date=_now)
        self.assertEqual(
            response,
            Response(notify=[Notify.LEAGUEFILE_FINISH], thread_=[thread_]))

        upload = {
            'start': 'Jan 29 16:00',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'date': 'Jan 29 15:55',
            'now': '2018-01-29T00:00:00-08:00'
        }
        write = _data(upload=upload, completed=[completed])
        mock_check_download.assert_not_called()
        mock_check_upload.assert_called_once_with()
        mock_download.assert_called_once_with(date=_now)
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_log.assert_called_once_with(logging.INFO, 'File is up.')
        self.mock_reactions.assert_called_once_with('zap', _channel, _ts)

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_file_is_up_slow(self, mock_check_download,
                                       mock_check_upload, mock_download,
                                       mock_render):
        check = ('328706052', 'Jan 29 07:55',
                 'orange_and_blue_league_baseball.tar.gz', False)
        mock_check_upload.return_value = iter([check])
        thread_ = Thread(target='_download_internal', kwargs={'date': _now})
        mock_download.return_value = Response(thread_=[thread_])

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00-08:00'
        }
        completed = {
            'size': '345678901',
            'date': 'Jan 27 12:00',
            'dstart': 'Jan 27 12:00',
            'dend': 'Jan 27 12:00',
            'ustart': 'Jan 27 11:00',
            'uend': 'Jan 27 12:00'
        }
        leaguefile = self.create_leaguefile(
            _data(upload=upload, completed=[completed]))
        response = leaguefile._run_internal(date=_now)
        self.assertEqual(
            response,
            Response(notify=[Notify.LEAGUEFILE_FINISH], thread_=[thread_]))

        upload = {
            'start': 'Jan 29 16:00',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'date': 'Jan 29 07:55',
            'now': '2018-01-29T00:00:00-08:00'
        }
        write = _data(upload=upload, completed=[completed])
        mock_check_download.assert_not_called()
        mock_check_upload.assert_called_once_with()
        mock_download.assert_called_once_with(date=_now)
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_log.assert_called_once_with(logging.INFO, 'File is up.')
        timer = 'timer_clock'
        self.mock_reactions.assert_called_once_with(timer, _channel, _ts)

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_file_is_up_typical(self, mock_check_download,
                                          mock_check_upload, mock_download,
                                          mock_render):
        check_c = ('328706052', 'Jan 29 12:55',
                   'orange_and_blue_league_baseball.tar.gz', False)
        mock_check_upload.return_value = iter([check_c])
        thread_ = Thread(target='_download_internal', kwargs={'date': _now})
        mock_download.return_value = Response(thread_=[thread_])

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00-08:00'
        }
        completed = {
            'size': '345678901',
            'date': 'Jan 27 12:00',
            'dstart': 'Jan 27 12:00',
            'dend': 'Jan 27 12:00',
            'ustart': 'Jan 27 10:00',
            'uend': 'Jan 27 12:00'
        }
        leaguefile = self.create_leaguefile(
            _data(upload=upload, completed=[completed]))
        response = leaguefile._run_internal(date=_now)
        self.assertEqual(
            response,
            Response(notify=[Notify.LEAGUEFILE_FINISH], thread_=[thread_]))

        upload = {
            'start': 'Jan 29 16:00',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'date': 'Jan 29 12:55',
            'now': '2018-01-29T00:00:00-08:00'
        }
        write = _data(upload=upload, completed=[completed])
        mock_check_download.assert_not_called()
        mock_check_upload.assert_called_once_with()
        mock_download.assert_called_once_with(date=_now)
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_called_once_with('fairylab', 'File is up.')
        self.mock_log.assert_called_once_with(logging.INFO, 'File is up.')
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_download_in_progress(self, mock_check_download,
                                            mock_check_upload, mock_download,
                                            mock_render):
        check_d = ('100000', 'Jan 29 18:10',
                   'orange_and_blue_league_baseball.tar.gz', True)
        mock_check_download.return_value = check_d
        check_c = ('328706052', 'Jan 29 12:55',
                   'orange_and_blue_league_baseball.tar.gz', False)
        mock_check_upload.return_value = iter([check_c])

        download = {
            'start': 'Jan 29 18:05',
            'size': '20000',
            'end': 'Jan 29 18:05',
            'now': '2018-01-29T00:00:00-08:00'
        }
        upload = {
            'start': 'Jan 29 16:00',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00-08:00'
        }
        leaguefile = self.create_leaguefile(
            _data(download=download, upload=upload))
        response = leaguefile._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        download = {
            'start': 'Jan 29 18:05',
            'size': '100000',
            'end': 'Jan 29 00:00',
            'now': '2018-01-29T00:00:00-08:00'
        }
        write = _data(download=download, upload=upload)
        mock_check_download.assert_called_once_with()
        mock_check_upload.assert_not_called()
        mock_download.assert_not_called()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, 'download')
    @mock.patch.object(Leaguefile, '_check_upload')
    @mock.patch.object(Leaguefile, '_check_download')
    def test_run__with_download_completed(self, mock_check_download,
                                          mock_check_upload, mock_download,
                                          mock_render):
        check_d = ('328706052', 'Jan 29 18:00',
                   'orange_and_blue_league_baseball.tar.gz', False)
        mock_check_download.return_value = check_d
        check_c = ('328706052', 'Jan 29 12:55',
                   'orange_and_blue_league_baseball.tar.gz', False)
        mock_check_upload.return_value = iter([check_c])

        download = {
            'start': 'Jan 29 18:05',
            'size': '100000',
            'end': 'Jan 29 18:10',
            'now': '2018-01-29T00:00:00-08:00'
        }
        upload = {
            'start': 'Jan 29 16:00',
            'date': 'Jan 29 12:55',
            'size': '328706052',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T00:00:00-08:00'
        }
        leaguefile = self.create_leaguefile(
            _data(download=download, upload=upload))
        response = leaguefile._run_internal(date=_now)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        completed = {
            'size': '328706052',
            'date': 'Jan 29 12:55',
            'ustart': 'Jan 29 16:00',
            'uend': 'Jan 29 18:00',
            'dstart': 'Jan 29 18:05',
            'dend': 'Jan 29 18:10'
        }
        write = _data(completed=[completed])
        mock_check_download.assert_called_once_with()
        mock_check_upload.assert_not_called()
        mock_download.assert_not_called()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_home')
    def test_render(self, mock_home):
        home = {'breadcrumbs': [], 'upload': {}, 'completed': {}}
        mock_home.return_value = home

        leaguefile = self.create_leaguefile(_data())
        response = leaguefile._render_internal(date=_now)
        index = 'leaguefile/index.html'
        self.assertEqual(response, [(index, '', 'leaguefile.html', home)])

        mock_home.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check_upload')
    def test_setup__with_valid_input(self, mock_check, mock_render):
        check_u = ('100000', 'Jan 29 16:00',
                   'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_c = ('345678901', 'Jan 27 12:00',
                   'orange_and_blue_league_baseball.tar.gz', True)
        mock_check.return_value = iter([check_u, check_c])

        upload = {
            'start': 'Jan 29 15:00',
            'size': '50000',
            'end': 'Jan 29 15:00',
            'now': '2018-01-28T23:55:00'
        }
        read = _data(upload=upload)
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._setup_internal(date=_now)
        self.assertEqual(response, Response())

        upload = {
            'start': 'Jan 29 15:00',
            'size': '100000',
            'end': 'Jan 29 16:00',
            'now': '2018-01-29T00:00:00-08:00'
        }
        write = _data(upload=upload)
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check_upload')
    def test_setup__with_no_change(self, mock_check, mock_render):
        check = ('345678901', 'Jan 27 12:00',
                 'orange_and_blue_league_baseball.tar.gz', False)
        mock_check.return_value = iter([check])

        completed = {
            'size': '345678901',
            'date': 'Jan 27 12:00',
            'dstart': 'Jan 27 12:00',
            'dend': 'Jan 27 12:00',
            'ustart': 'Jan 27 12:00',
            'uend': 'Jan 27 12:00'
        }
        read = _data(completed=[completed])
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._setup_internal(date=_now)
        self.assertEqual(response, Response())

        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check_upload')
    def test_setup__with_no_upload(self, mock_check, mock_render):
        check = ('345678901', 'Jan 27 12:00',
                 'orange_and_blue_league_baseball.tar.gz', False)
        mock_check.return_value = iter([check])

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 16:00',
            'now': '2018-01-29T00:00:00-08:00'
        }
        completed = {
            'size': '345678901',
            'date': 'Jan 27 12:00',
            'dstart': 'Jan 27 12:00',
            'dend': 'Jan 27 12:00',
            'ustart': 'Jan 27 12:00',
            'uend': 'Jan 27 12:00'
        }
        read = _data(upload=upload, completed=[completed])
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._setup_internal(date=_now)
        self.assertEqual(response, Response())

        write = _data(completed=[completed])
        mock_check.assert_called_once_with()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Leaguefile, '_render')
    @mock.patch.object(Leaguefile, '_check_upload')
    def test_setup__with_download(self, mock_check, mock_render):
        check = ('345678901', 'Jan 27 12:00',
                 'orange_and_blue_league_baseball.tar.gz', False)
        mock_check.return_value = iter([check])

        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 16:00',
            'now': '2018-01-28T23:55:00'
        }
        download = {'start': 'Jan 28 12:00', 'now': '2018-01-28T12:00:00'}
        read = _data(upload=upload, download=download)
        leaguefile = self.create_leaguefile(read)
        response = leaguefile._setup_internal(date=_now)
        self.assertEqual(
            response,
            Response(thread_=[
                Thread(target='_download_internal', kwargs={'date': _now})
            ]))

        download = {
            'start': 'Jan 29 00:00',
            'now': '2018-01-29T00:00:00-08:00'
        }
        write = _data(upload=upload, download=download)
        mock_check.assert_not_called()
        mock_render.assert_called_once_with(date=_now)
        self.mock_open.assert_called_once_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_chat.assert_not_called()
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download started.')
        self.mock_reactions.assert_not_called()

    def test_shadow(self):
        completed = {
            'size': '345678901',
            'date': 'Jan 27 12:00',
            'dstart': 'Jan 27 12:00',
            'dend': 'Jan 27 12:00',
            'ustart': 'Jan 27 12:00',
            'uend': 'Jan 27 12:00'
        }
        leaguefile = self.create_leaguefile(_data(completed=[completed]))
        value = leaguefile._shadow_internal()
        self.assertEqual(value, [
            Shadow(
                destination='statsplus',
                key='leaguefile.now',
                info=_now_encoded)
        ])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_not_called()

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
        actual = Leaguefile._time(s, e, _now)
        expected = '2h 0m'
        self.assertEqual(actual, expected)

    @mock.patch('tasks.leaguefile.leaguefile._logger.log')
    @mock.patch('tasks.leaguefile.leaguefile.check_output')
    def test_check_download__with_filepart(self, mock_check, mock_log):
        ls = 'total 60224\n' + \
             '-rw-rw-r-- 1 user user 100000 Jan 29 16:00 ' + \
             'orange_and_blue_league_baseball.tar.gz'
        mock_check.return_value = {'ok': True, 'stdout': ls}

        actual = Leaguefile._check_download()
        expected = ('100000', 'Jan 29 16:00',
                    'orange_and_blue_league_baseball.tar.gz', True)
        self.assertEqual(actual, expected)

        mock_check.assert_called_once_with(
            ['ls', '-l', os.path.join(_root, 'resource/download')], timeout=8)
        mock_log.assert_not_called()

    @mock.patch('tasks.leaguefile.leaguefile._logger.log')
    @mock.patch('tasks.leaguefile.leaguefile.check_output')
    def test_check_download__without_filepart(self, mock_check, mock_log):
        ls = 'total 60224\n' + \
             'drwxrwxr-x 4 user user      4096 Jan 29 00:00 news\n' + \
             '-rw-rw-r-- 1 user user 345678901 Jan 29 16:00 ' + \
             'orange_and_blue_league_baseball.tar.gz'
        mock_check.return_value = {'ok': True, 'stdout': ls}

        actual = Leaguefile._check_download()
        expected = ('345678901', 'Jan 29 16:00',
                    'orange_and_blue_league_baseball.tar.gz', False)
        self.assertEqual(actual, expected)

        mock_check.assert_called_once_with(
            ['ls', '-l', os.path.join(_root, 'resource/download')], timeout=8)
        mock_log.assert_not_called()

    @mock.patch('tasks.leaguefile.leaguefile._logger.log')
    @mock.patch('tasks.leaguefile.leaguefile.check_output')
    def test_check_download__with_ok_false(self, mock_check, mock_log):
        mock_check.return_value = {'ok': False}

        actual = Leaguefile._check_download()
        expected = ('0', '', '', False)
        self.assertEqual(actual, expected)

        mock_check.assert_called_once_with(
            ['ls', '-l', os.path.join(_root, 'resource/download')], timeout=8)
        mock_log.assert_not_called()

    @mock.patch('tasks.leaguefile.leaguefile._logger.log')
    @mock.patch('tasks.leaguefile.leaguefile.check_output')
    def test_check_upload__with_filepart(self, mock_check, mock_log):
        ls = 'total 321012\n' + \
             '-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html\n' + \
             '-rwxrwxrwx 1 user user 345678901 Jan 27 12:00 ' + \
             'orange_and_blue_league_baseball.tar.gz\n' + \
             '-rwxrwxrwx 1 user user 100000 Jan 29 16:00 ' + \
             'orange_and_blue_league_baseball.tar.gz.filepart'
        mock_check.return_value = {'ok': True, 'stdout': ls}

        actual = Leaguefile._check_upload()
        check_u = ('100000', 'Jan 29 16:00',
                   'orange_and_blue_league_baseball.tar.gz.filepart', True)
        check_c = ('345678901', 'Jan 27 12:00',
                   'orange_and_blue_league_baseball.tar.gz', True)
        expected = iter([check_u, check_c])
        self.assertCountEqual(actual, expected)

        mock_check.assert_called_once_with(
            [
                'ssh', 'brunnerj@' + _server,
                'ls -l /var/www/html/StatsLab/league_file'
            ],
            timeout=8)
        mock_log.assert_not_called()

    @mock.patch('tasks.leaguefile.leaguefile._logger.log')
    @mock.patch('tasks.leaguefile.leaguefile.check_output')
    def test_check_upload__without_filepart(self, mock_check, mock_log):
        ls = 'total 321012\n' + \
             '-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html\n' + \
             '-rwxrwxrwx 1 user user 328706052 Jan 29 12:55 ' + \
             'orange_and_blue_league_baseball.tar.gz'
        mock_check.return_value = {'ok': True, 'stdout': ls}

        actual = Leaguefile._check_upload()
        check_c = ('328706052', 'Jan 29 12:55',
                   'orange_and_blue_league_baseball.tar.gz', False)
        expected = iter([check_c])
        self.assertCountEqual(actual, expected)

        mock_check.assert_called_once_with(
            [
                'ssh', 'brunnerj@' + _server,
                'ls -l /var/www/html/StatsLab/league_file'
            ],
            timeout=8)
        mock_log.assert_not_called()

    @mock.patch('tasks.leaguefile.leaguefile._logger.log')
    @mock.patch('tasks.leaguefile.leaguefile.check_output')
    def test_check_upload__with_ok_false(self, mock_check, mock_log):
        mock_check.return_value = {
            'ok': False,
            'stdout': 'out',
            'stderr': 'err'
        }

        actual = Leaguefile._check_upload()
        expected = iter([])
        self.assertCountEqual(actual, expected)

        mock_check.assert_called_once_with(
            [
                'ssh', 'brunnerj@' + _server,
                'ls -l /var/www/html/StatsLab/league_file'
            ],
            timeout=8)
        mock_log.assert_not_called()

    @mock.patch('tasks.leaguefile.leaguefile.check_output')
    def test_download__with_ok_false(self, mock_check):
        mock_check.return_value = {
            'ok': False,
            'stdout': 'out',
            'stderr': 'err'
        }

        completed = {
            'size': '345678901',
            'date': 'Jan 27 12:00',
            'dstart': 'Jan 27 12:00',
            'dend': 'Jan 27 12:00',
            'ustart': 'Jan 27 12:00',
            'uend': 'Jan 27 12:00'
        }
        leaguefile = self.create_leaguefile(_data(upload=completed))
        response = leaguefile.download(date=_now)
        self.assertEqual(response, Response())

        self.mock_log.assert_called_once_with(
            logging.WARNING,
            'Download failed.',
            extra={
                'stdout': 'out',
                'stderr': 'err'
            })
        self.assertFalse(leaguefile.data['download'])

    @mock.patch('tasks.leaguefile.leaguefile.check_output')
    def test_download__with_ok_true(self, mock_check):
        mock_check.return_value = {'ok': True}

        completed = {
            'size': '345678901',
            'date': 'Jan 27 12:00',
            'dstart': 'Jan 27 12:00',
            'dend': 'Jan 27 12:00',
            'ustart': 'Jan 27 12:00',
            'uend': 'Jan 27 12:00'
        }
        leaguefile = self.create_leaguefile(_data(upload=completed))
        response = leaguefile.download(date=_now)
        self.assertEqual(
            response,
            Response(thread_=[
                Thread(target='_download_internal', kwargs={'date': _now})
            ]))

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download started.')
        self.assertEqual(leaguefile.data['download'], {
            'start': 'Jan 29 00:00',
            'now': _now_encoded
        })

    @mock.patch('tasks.leaguefile.leaguefile.extract_file')
    @mock.patch('tasks.leaguefile.leaguefile.download_file')
    def test_download_internal__with_new_year(self, mock_download_file,
                                              mock_extract_file):
        mock_extract_file.return_value = _year
        mock_download_file.return_value = {'ok': True}

        download = {
            'start': 'Jan 29 18:05',
            'now': '2018-01-29T00:00:00-08:00'
        }
        leaguefile = self.create_leaguefile(
            _data(download=download, now=_then_encoded))

        response = leaguefile._download_internal(v=True)
        notify = [Notify.LEAGUEFILE_DOWNLOAD, Notify.LEAGUEFILE_YEAR]
        shadow = leaguefile._shadow_internal()
        self.assertEqual(response, Response(notify=notify, shadow=shadow))

        write = _data(download=download, now=_year_encoded)
        mock_download_file.assert_called_once_with(FILE_URL)
        mock_extract_file.assert_called_once_with(_then)
        self.mock_open.assert_called_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download finished.')

    @mock.patch('tasks.leaguefile.leaguefile.extract_file')
    @mock.patch('tasks.leaguefile.leaguefile.download_file')
    def test_download_internal__with_same_year(self, mock_download_file,
                                               mock_extract_file):
        mock_download_file.return_value = {'ok': True}
        mock_extract_file.return_value = _now

        download = {
            'start': 'Jan 29 18:05',
            'now': '2018-01-29T00:00:00-08:00'
        }
        leaguefile = self.create_leaguefile(
            _data(download=download, now=_then_encoded))

        response = leaguefile._download_internal(v=True)
        notify = [Notify.LEAGUEFILE_DOWNLOAD]
        shadow = leaguefile._shadow_internal()
        self.assertEqual(response, Response(notify=notify, shadow=shadow))

        write = _data(download=download, now=_now_encoded)
        mock_download_file.assert_called_once_with(FILE_URL)
        mock_extract_file.assert_called_once_with(_then)
        self.mock_open.assert_called_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_log.assert_called_once_with(logging.INFO,
                                              'Download finished.')

    @mock.patch('tasks.leaguefile.leaguefile.extract_file')
    @mock.patch('tasks.leaguefile.leaguefile.download_file')
    def test_download_internal__with_ok_false(self, mock_download_file,
                                              mock_extract_file):
        mock_download_file.return_value = {'ok': False}

        download = {
            'start': 'Jan 29 18:05',
            'now': '2018-01-29T00:00:00-08:00'
        }
        leaguefile = self.create_leaguefile(
            _data(download=download, now=_then_encoded))

        response = leaguefile._download_internal(v=True)
        self.assertEqual(response, Response())

        write = _data(now=_then_encoded)
        mock_download_file.assert_called_once_with(FILE_URL)
        mock_extract_file.assert_not_called()
        self.mock_open.assert_called_with(Leaguefile._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_log.assert_called_once_with(logging.INFO, 'Download failed.')

    def test_home__with_empty(self):
        leaguefile = self.create_leaguefile(_data())
        actual = leaguefile._home(date=_now)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        cols = [
            col(),
            col(clazz='text-center'),
            col(clazz='text-center'),
            col(clazz='text-right')
        ]
        completed = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='Date'),
                cell(content='Upload'),
                cell(content='Download'),
                cell(content='Size')
            ],
            body=[])
        expected = {
            'breadcrumbs': breadcrumbs,
            'upload': None,
            'download': None,
            'completed': completed
        }
        self.assertEqual(actual, expected)

    def test_home__with_upload(self):
        upload = {
            'start': 'Jan 29 16:00',
            'size': '100000',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T18:04:00-08:00'
        }
        leaguefile = self.create_leaguefile(_data(upload=upload))
        actual = leaguefile._home(date=_now)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        upload = card(
            title='Jan 29',
            table=table(
                clazz='table-sm',
                hcols=[col(clazz='w-55p'), col()],
                bcols=[col(clazz='w-55p'), col()],
                body=[[cell(content='Time: '),
                       cell(content='2h 0m')],
                      [cell(content='Size: '),
                       cell(content='100,000')]]),
            ts='18:04:00 PST (2018-01-29)',
            success='ongoing')
        cols = [
            col(),
            col(clazz='text-center'),
            col(clazz='text-center'),
            col(clazz='text-right')
        ]
        completed = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='Date'),
                cell(content='Upload'),
                cell(content='Download'),
                cell(content='Size')
            ],
            body=[])
        expected = {
            'breadcrumbs': breadcrumbs,
            'upload': upload,
            'download': None,
            'completed': completed
        }
        self.assertEqual(actual, expected)

    def test_home__with_download(self):
        download = {
            'start': 'Jan 29 18:05',
            'size': '100000',
            'end': 'Jan 29 18:10',
            'now': '2018-01-29T18:14:00-08:00'
        }
        upload = {
            'start': 'Jan 29 16:00',
            'size': '345678901',
            'end': 'Jan 29 18:00',
            'now': '2018-01-29T18:02:00-08:00'
        }
        leaguefile = self.create_leaguefile(
            _data(download=download, upload=upload))
        actual = leaguefile._home(date=_now)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        upload = card(
            title='Jan 29',
            table=table(
                clazz='table-sm',
                hcols=[col(clazz='w-55p'), col()],
                bcols=[col(clazz='w-55p'), col()],
                body=[[cell(content='Time: '),
                       cell(content='2h 0m')],
                      [cell(content='Size: '),
                       cell(content='345,678,901')]]),
            ts='18:02:00 PST (2018-01-29)',
            success='completed')
        download = card(
            title='Jan 29',
            table=table(
                clazz='table-sm',
                hcols=[col(clazz='w-55p'), col()],
                bcols=[col(clazz='w-55p'), col()],
                body=[[cell(content='Time: '),
                       cell(content='5m')],
                      [cell(content='Size: '),
                       cell(content='100,000')]]),
            ts='18:14:00 PST (2018-01-29)',
            success='ongoing')
        cols = [
            col(),
            col(clazz='text-center'),
            col(clazz='text-center'),
            col(clazz='text-right')
        ]
        completed = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='Date'),
                cell(content='Upload'),
                cell(content='Download'),
                cell(content='Size')
            ],
            body=[])
        expected = {
            'breadcrumbs': breadcrumbs,
            'upload': upload,
            'download': download,
            'completed': completed
        }
        self.assertEqual(actual, expected)

    def test_home__with_completed(self):
        completed = {
            'size': '345678901',
            'ustart': 'Jan 27 12:00',
            'uend': 'Jan 27 12:00',
            'dstart': 'Jan 27 12:00',
            'dend': 'Jan 27 12:00',
            'date': 'Jan 27 12:00'
        }
        leaguefile = self.create_leaguefile(_data(completed=[completed]))
        actual = leaguefile._home(date=_now)
        breadcrumbs = [{
            'href': '/',
            'name': 'Fairylab'
        }, {
            'href': '',
            'name': 'Leaguefile'
        }]
        cols = [
            col(),
            col(clazz='text-center'),
            col(clazz='text-center'),
            col(clazz='text-right')
        ]
        completed = table(
            hcols=cols,
            bcols=cols,
            head=[
                cell(content='Date'),
                cell(content='Upload'),
                cell(content='Download'),
                cell(content='Size')
            ],
            body=[[
                cell(content='Jan 27'),
                cell(content='0m'),
                cell(content='0m'),
                cell(content='345,678,901')
            ]])
        expected = {
            'breadcrumbs': breadcrumbs,
            'upload': None,
            'download': None,
            'completed': completed
        }
        self.assertEqual(actual, expected)


if __name__ in ['__main__', 'tasks.leaguefile.leaguefile_test']:
    _main = __name__ == '__main__'
    _pkg = 'tasks.leaguefile'
    _pth = 'tasks/leaguefile'
    main(LeaguefileTest, Leaguefile, _pkg, _pth, {}, _main, date=_now, e=_env)
