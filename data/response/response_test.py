#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for response.py."""

import os
import re
import sys
import unittest

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/data/response', '', _path))

from data.debug.debug import Debug  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa
from data.shadow.shadow import Shadow  # noqa
from data.thread_.thread_ import Thread  # noqa

DEBUG = Debug(msg='foo')
NOTIFY = Notify.BASE
SHADOW = Shadow(destination='bar', key='foo.baz')
THREAD = Thread(target='foo')


class ResponseTest(unittest.TestCase):
    def test_init__empty(self):
        response = Response()
        self.assertEqual(response.debug, [])
        self.assertEqual(response.notify, [])
        self.assertEqual(response.shadow, [])
        self.assertEqual(response.thread_, [])

    def test_init__filled(self):
        response = Response(
            debug=[DEBUG], notify=[NOTIFY], shadow=[SHADOW], thread_=[THREAD])
        self.assertEqual(response.debug, [DEBUG])
        self.assertEqual(response.notify, [NOTIFY])
        self.assertEqual(response.shadow, [SHADOW])
        self.assertEqual(response.thread_, [THREAD])

    def test_init__invalid_debug_type(self):
        with self.assertRaises(TypeError):
            Response(debug=Debug(msg='foo'))

    def test_init__invalid_debug_element_value(self):
        with self.assertRaises(ValueError):
            Response(debug=[1])

    def test_init__invalid_notify_type(self):
        with self.assertRaises(TypeError):
            Response(notify=Notify.BASE)

    def test_init__invalid_notify_element_value(self):
        with self.assertRaises(ValueError):
            Response(notify=[1])

    def test_init__invalid_shadow_type(self):
        with self.assertRaises(TypeError):
            Response(shadow=Shadow(destination='bar', key='foo.baz'))

    def test_init__invalid_shadow_element_value(self):
        with self.assertRaises(ValueError):
            Response(shadow=[1])

    def test_init__invalid_thread_type(self):
        with self.assertRaises(TypeError):
            Response(thread_=Thread(target='foo'))

    def test_init__invalid_thread_element_value(self):
        with self.assertRaises(ValueError):
            Response(thread_=[1])

    def test_append__empty(self):
        response = Response()
        response.append()
        self.assertEqual(response.debug, [])
        self.assertEqual(response.notify, [])
        self.assertEqual(response.shadow, [])
        self.assertEqual(response.thread_, [])

    def test_append__filled(self):
        response = Response()
        response.append(
            debug=DEBUG, notify=NOTIFY, shadow=SHADOW, thread_=THREAD)
        self.assertEqual(response.debug, [DEBUG])
        self.assertEqual(response.notify, [NOTIFY])
        self.assertEqual(response.shadow, [SHADOW])
        self.assertEqual(response.thread_, [THREAD])

    def test_append__invalid_debug_element_value(self):
        response = Response()
        with self.assertRaises(ValueError):
            response.append(debug=1)

    def test_append__invalid_notify_element_value(self):
        response = Response()
        with self.assertRaises(ValueError):
            response.append(notify=1)

    def test_append_shadow__invalid_element_value(self):
        response = Response()
        with self.assertRaises(ValueError):
            response.append(shadow=1)

    def test_append_thread__invalid_element_value(self):
        response = Response()
        with self.assertRaises(ValueError):
            response.append(thread_=1)


if __name__ == '__main__':
    unittest.main()
