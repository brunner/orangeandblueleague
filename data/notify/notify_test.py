#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for notify.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/data/notify', '', _path))

from data.notify.notify import Notify  # noqa


class NotifyTest(unittest.TestCase):
    def test_enum(self):
        self.assertEqual(Notify.BASE, 1)
        self.assertEqual(Notify.DOWNLOAD_FINISH, 2)
        self.assertEqual(Notify.DOWNLOAD_YEAR, 3)
        self.assertEqual(Notify.EXPORTS_EMAILS, 4)
        self.assertEqual(Notify.FILEFAIRY_DAY, 5)
        self.assertEqual(Notify.FILEFAIRY_DEPLOY, 6)
        self.assertEqual(Notify.STATSPLUS_FINISH, 7)
        self.assertEqual(Notify.STATSPLUS_PARSE, 8)
        self.assertEqual(Notify.STATSPLUS_START, 9)
        self.assertEqual(Notify.UPLOAD_FINISH, 10)
        self.assertEqual(Notify.OTHER, 11)


if __name__ == '__main__':
    unittest.main()
