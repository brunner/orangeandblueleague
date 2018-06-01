#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/subprocess_', '', _path))
from util.subprocess_.subprocess_ import check_output  # noqa


class SubprocessTest(unittest.TestCase):
    @mock.patch('util.subprocess_.subprocess_.subprocess.run')
    def test_run__ok(self, mock_run):
        cmd = ['cmd', 'foo', 'bar']
        t = 10
        mock_run.return_value = subprocess.CompletedProcess(
            args=cmd, returncode=0, stdout=b'ret', stderr=None)

        actual = check_output(cmd, timeout=t)
        expected = {'ok': True, 'output': 'ret'}
        self.assertEqual(actual, expected)

        mock_run.assert_called_once_with(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=t,
            check=True)

    @mock.patch('util.subprocess_.subprocess_.subprocess.run')
    def test_run__exception(self, mock_run):
        cmd = ['cmd', 'foo', 'bar']
        t = 10
        mock_run.side_effect = subprocess.TimeoutExpired(cmd, t)

        actual = check_output(cmd, timeout=t)
        ret = 'Command \'{0}\' timed out after {1} seconds'.format(cmd, t)
        expected = {'ok': False, 'output': ret}
        self.assertEqual(actual, expected)

        mock_run.assert_called_once_with(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=t,
            check=True)


if __name__ == '__main__':
    unittest.main()