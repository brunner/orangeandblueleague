#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/util/file_', '', _path)
sys.path.append(_root)
from util.file_.file_ import ping  # noqa
from util.file_.file_ import recreate  # noqa
from util.file_.file_ import wget_file  # noqa

_download = os.path.join(_root, 'download')
_host = 'www.orangeandblueleaguebaseball.com'
_name = 'orange_and_blue_league_baseball.tar.gz'
_url = 'https://' + _host + '/StatsLab/league_file/' + _name

OK = {'ok': True}


class FileTest(unittest.TestCase):
    @mock.patch('util.file_.file_.check_output')
    def test_ping(self, mock_check):
        mock_check.return_value = OK

        output = ping()
        self.assertEqual(output, OK)

        mock_check.assert_called_once_with(
            ['ping', '-c', '1', _host], timeout=8)

    @mock.patch('util.file_.file_.check_output')
    def test_recreate(self, mock_check):
        recreate(_download)

        calls = [
            mock.call(['rm', '-rf', _download]),
            mock.call(['mkdir', _download])
        ]
        mock_check.assert_has_calls(calls)

    @mock.patch('util.file_.file_.check_output')
    def test_wget(self, mock_check):
        wget_file()

        calls = [
            mock.call(['rm', '-rf', _download]),
            mock.call(['mkdir', _download]),
            mock.call(['wget', _url]),
            mock.call(['tar', '-xzf', _name])
        ]
        mock_check.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()