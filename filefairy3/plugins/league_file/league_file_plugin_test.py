#!/usr/bin/env python

from league_file_plugin import LeagueFilePlugin

import mock
import os
import re
import unittest
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/plugins/league_file', '', _path))
from utils.testing.testing_util import write  # noqa

_data = LeagueFilePlugin._data()

_started = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 345678901 Jan 27 12:00 orange_and_blue_league_baseball.tar.gz
-rwxrwxrwx 1 user user 310000000 Jan 29 19:26 orange_and_blue_league_baseball.tar.gz.filepart
"""

_stopped = """total 321012
-rwxrwxrwx 1 user user       421 Aug 19 13:48 index.html
-rwxrwxrwx 1 user user 328706052 Jan 29 14:55 orange_and_blue_league_baseball.tar.gz
"""


class LeagueFilePluginTest(unittest.TestCase):
    @mock.patch('league_file_plugin.check_output')
    @mock.patch('league_file_plugin.chat_post_message')
    def test_run__with_empty_started(self, mock_post, mock_check):
        mock_check.return_value = _started
        data = {'fp': None, 'up': []}
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp': {
                'size': '310000000',
                'start': 'Jan 29 19:26',
                'end': 'Jan 29 19:26'
            },
            'up': []
        }
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()

    @mock.patch('league_file_plugin.check_output')
    @mock.patch('league_file_plugin.chat_post_message')
    def test_run__with_filepart_started(self, mock_post, mock_check):
        mock_check.return_value = _started
        data = {
            'fp': {
                'size': '300000000',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:23'
            },
            'up': []
        }
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp': {
                'size': '310000000',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:26'
            },
            'up': [],
        }
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()

    @mock.patch('league_file_plugin.check_output')
    @mock.patch('league_file_plugin.chat_post_message')
    def test_run__with_finished_started(self, mock_post, mock_check):
        mock_check.return_value = _started
        data = {
            'fp':
            None,
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp': {
                'size': '310000000',
                'start': 'Jan 29 19:26',
                'end': 'Jan 29 19:26'
            },
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()

    @mock.patch('league_file_plugin.check_output')
    @mock.patch('league_file_plugin.chat_post_message')
    def test_run__with_both_started(self, mock_post, mock_check):
        mock_check.return_value = _started
        data = {
            'fp': {
                'size': '300000000',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:23'
            },
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp': {
                'size': '310000000',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:26'
            },
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()

    @mock.patch('league_file_plugin.check_output')
    @mock.patch('league_file_plugin.chat_post_message')
    def test_run__with_empty_stopped(self, mock_post, mock_check):
        mock_check.return_value = _stopped
        data = {'fp': None, 'up': []}
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {'fp': None, 'up': []}
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()

    @mock.patch('league_file_plugin.check_output')
    @mock.patch('league_file_plugin.chat_post_message')
    def test_run__with_filepart_stopped(self, mock_post, mock_check):
        mock_check.return_value = _stopped
        data = {
            'fp': {
                'size': '300000000',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:23'
            },
            'up': []
        }
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp':
            None,
            'up': [{
                'size': '328706052',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:23',
                'date': 'Jan 29 14:55'
            }]
        }
        self.assertEqual(actual, expected)
        mock_post.assert_called_once_with('general', 'File is up.')

    @mock.patch('league_file_plugin.check_output')
    @mock.patch('league_file_plugin.chat_post_message')
    def test_run__with_finished_stopped(self, mock_post, mock_check):
        mock_check.return_value = _stopped
        data = {
            'fp':
            None,
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp':
            None,
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        self.assertEqual(actual, expected)
        mock_post.assert_not_called()

    @mock.patch('league_file_plugin.check_output')
    @mock.patch('league_file_plugin.chat_post_message')
    def test_run__with_both_stopped(self, mock_post, mock_check):
        mock_check.return_value = _stopped
        data = {
            'fp': {
                'size': '300000000',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:23'
            },
            'up': [{
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        original = write(_data, data)
        plugin = LeagueFilePlugin()
        plugin._run()
        actual = write(_data, original)
        expected = {
            'fp':
            None,
            'up': [{
                'size': '328706052',
                'start': 'Jan 29 15:00',
                'end': 'Jan 29 19:23',
                'date': 'Jan 29 14:55'
            }, {
                'size': '345678901',
                'start': 'Jan 27 12:05',
                'end': 'Jan 27 16:00',
                'date': 'Jan 27 12:00'
            }]
        }
        self.assertEqual(actual, expected)
        mock_post.assert_called_once_with('general', 'File is up.')


if __name__ == '__main__':
    unittest.main()
