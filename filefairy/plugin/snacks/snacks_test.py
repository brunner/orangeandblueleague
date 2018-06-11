#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
import unittest
import unittest.mock as mock

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_path)
_root = re.sub(r'/plugin/snacks', '', _path)
sys.path.append(_root)
from core.notify.notify import Notify  # noqa
from core.response.response import Response  # noqa
from core.task.task import Task  # noqa
from plugin.snacks.snacks import Snacks  # noqa
from plugin.snacks.snacks import _chooselist  # noqa
from plugin.snacks.snacks import _snacklist  # noqa
from util.json_.json_ import dumps  # noqa

_collect = {'U1234': ['reply.', 'foo.', 'bar.', 'baz.']}
_members_new = {
    'U1234': {
        'latest': '1000.789'
    },
    'U5678': {
        'latest': '100.456'
    }
}
_members_old = {'U1234': {'latest': '100.123'}, 'U5678': {'latest': '100.456'}}
_members_bot = {
    'U1234': {
        'latest': '100.123'
    },
    'U5678': {
        'latest': '100.456'
    },
    'U3ULC7DBP': {
        'latest': '1000.789'
    },
}
_now = datetime.datetime(1985, 10, 27, 0, 0, 0)
_then = datetime.datetime(1985, 10, 26, 0, 2, 30)


def _data(members=_members_old):
    return {'members': members}


class SnacksTest(unittest.TestCase):
    def setUp(self):
        patch_open = mock.patch(
            'api.serializable.serializable.open', create=True)
        self.addCleanup(patch_open.stop)
        self.mock_open = patch_open.start()

        patch_cfd = mock.patch('plugin.snacks.snacks.cfd')
        self.addCleanup(patch_cfd.stop)
        self.mock_cfd = patch_cfd.start()

        patch_chat = mock.patch('plugin.snacks.snacks.chat_post_message')
        self.addCleanup(patch_chat.stop)
        self.mock_chat = patch_chat.start()

        patch_collect = mock.patch('plugin.snacks.snacks.collect')
        self.addCleanup(patch_collect.stop)
        self.mock_collect = patch_collect.start()

        patch_reactions = mock.patch('plugin.snacks.snacks.reactions_add')
        self.addCleanup(patch_reactions.stop)
        self.mock_reactions = patch_reactions.start()

    def init_mocks(self, data):
        mo = mock.mock_open(read_data=dumps(data))
        self.mock_handle = mo()
        self.mock_open.side_effect = [mo.return_value]
        self.mock_collect.return_value = _collect

    def reset_mocks(self):
        self.mock_open.reset_mock()
        self.mock_handle.write.reset_mock()
        self.mock_cfd.reset_mock()
        self.mock_chat.reset_mock()
        self.mock_collect.reset_mock()
        self.mock_reactions.reset_mock()

    def create_plugin(self, data, cfds=None, names=None):
        self.init_mocks(data)
        plugin = Snacks(date=_now)
        plugin.loaded = True

        self.mock_open.assert_called_once_with(Snacks._data(), 'r')
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

        self.reset_mocks()
        self.init_mocks(data)

        if cfds:
            plugin.cfds = cfds
        if names:
            plugin.names = names

        return plugin

    def test_notify__with_day(self):
        plugin = self.create_plugin(_data())
        plugin._setup(date=_then)

        self.reset_mocks()

        response = plugin._notify_internal(notify=Notify.FAIRYLAB_DAY)
        self.assertEqual(response, Response(task=[Task(target='_load')]))

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_notify__with_other(self):
        plugin = self.create_plugin(_data())
        plugin._setup(date=_then)

        self.reset_mocks()

        response = plugin._notify_internal(notify=Notify.OTHER)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugin.snacks.snacks.random.choice')
    def test_on_message__with_choose_text_multiple(self, mock_random):
        mock_random.side_effect = ['{}. Did you even need to ask?', 'a']

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> choose a or b',
            'ts': '1000.789',
            'user': 'U1234',
        }
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(members=_members_new)
        calls = [mock.call(_chooselist), mock.call(['a', 'b'])]
        mock_random.assert_has_calls(calls)
        self.mock_open.assert_called_once_with(Snacks._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0',
                                               'A. Did you even need to ask?')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugin.snacks.snacks.random.choice')
    def test_on_message__with_choose_text_single(self, mock_random):
        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> choose a',
            'ts': '1000.789',
            'user': 'U1234',
        }
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response())

        mock_random.assert_not_called()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugin.snacks.snacks.discuss')
    def test_on_message__with_discuss_text_empty(self, mock_discuss):
        mock_discuss.return_value = ''

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> discuss topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(members=_members_new)
        mock_discuss.assert_called_once_with('topic', {}, 4, 8, 30)
        self.mock_open.assert_called_once_with(Snacks._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with(
            'C9YE6NQG0', 'I don\'t know anything about topic.')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugin.snacks.snacks.discuss')
    def test_on_message__with_discuss_text_valid(self, mock_discuss):
        mock_discuss.return_value = 'response'

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> discuss topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(members=_members_new)
        mock_discuss.assert_called_once_with('topic', {}, 4, 8, 30)
        self.mock_open.assert_called_once_with(Snacks._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0', 'response')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugin.snacks.snacks.imitate')
    def test_on_message__with_imitate_text_empty(self, mock_imitate):
        mock_imitate.return_value = ''

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> imitate <@U5678>',
            'ts': '1000.789',
            'user': 'U1234',
        }
        cfds = {'U5678': {}}
        names = {'U5678': 'user'}
        plugin = self.create_plugin(_data(), cfds=cfds, names=names)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(members=_members_new)
        mock_imitate.assert_called_once_with({}, 4, 8, 30)
        self.mock_open.assert_called_once_with(Snacks._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with(
            'C9YE6NQG0', '<@U5678> doesn\'t know anything.')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugin.snacks.snacks.imitate')
    def test_on_message__with_imitate_text_valid(self, mock_imitate):
        mock_imitate.return_value = 'response'

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> imitate <@U5678>',
            'ts': '1000.789',
            'user': 'U1234',
        }
        cfds = {'U5678': {}}
        names = {'U5678': 'user'}
        plugin = self.create_plugin(_data(), cfds=cfds, names=names)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(members=_members_new)
        mock_imitate.assert_called_once_with({}, 4, 8, 30)
        self.mock_open.assert_called_once_with(Snacks._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0', 'response')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugin.snacks.snacks.discuss')
    def test_on_message__with_imitate_topic_text_empty(self, mock_discuss):
        mock_discuss.return_value = ''

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> imitate <@U5678> topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        cfds = {'U5678': {}}
        names = {'U5678': 'user'}
        plugin = self.create_plugin(_data(), cfds=cfds, names=names)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(members=_members_new)
        mock_discuss.assert_called_once_with('topic', {}, 4, 8, 30)
        self.mock_open.assert_called_once_with(Snacks._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with(
            'C9YE6NQG0', '<@U5678> doesn\'t know anything about topic.')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugin.snacks.snacks.discuss')
    def test_on_message__with_imitate_topic_text_user(self, mock_discuss):
        mock_discuss.return_value = 'response'

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> imitate <@U5678> <@U1234>',
            'ts': '1000.789',
            'user': 'U1234',
        }
        cfds = {'U5678': {}}
        names = {'U5678': 'user'}
        plugin = self.create_plugin(_data(), cfds=cfds, names=names)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(members=_members_new)
        mock_discuss.assert_called_once_with('<@U1234>', {}, 4, 8, 30)
        self.mock_open.assert_called_once_with(Snacks._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0', 'response')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugin.snacks.snacks.discuss')
    def test_on_message__with_imitate_topic_text_valid(self, mock_discuss):
        mock_discuss.return_value = 'response'

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> imitate <@U5678> topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        cfds = {'U5678': {}}
        names = {'U5678': 'user'}
        plugin = self.create_plugin(_data(), cfds=cfds, names=names)
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(members=_members_new)
        mock_discuss.assert_called_once_with('topic', {}, 4, 8, 30)
        self.mock_open.assert_called_once_with(Snacks._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0', 'response')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message__with_say_text(self):
        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> say topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(members=_members_new)
        self.mock_open.assert_called_once_with(Snacks._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_called_once_with('C9YE6NQG0', 'topic')
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Snacks, '_snacks')
    @mock.patch('plugin.snacks.snacks.pins_add')
    def test_on_message__with_snack_me_text_filefairy(self, mock_pins,
                                                      mock_snacks):
        mock_snacks.return_value = ['a', 'star']

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> snack me',
            'ts': '1000.789',
            'user': 'U3ULC7DBP',
        }
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(members=_members_bot)
        mock_pins.assert_called_once_with('C9YE6NQG0', '1000.789')
        mock_snacks.assert_called_once_with()
        self.mock_open.assert_called_once_with(Snacks._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        calls = [
            mock.call('a', 'C9YE6NQG0', '1000.789'),
            mock.call('star', 'C9YE6NQG0', '1000.789')
        ]
        self.mock_reactions.assert_has_calls(calls)

    @mock.patch.object(Snacks, '_snacks')
    @mock.patch('plugin.snacks.snacks.pins_add')
    def test_on_message__with_snack_me_text_user(self, mock_pins, mock_snacks):
        mock_snacks.return_value = ['a', 'star']

        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> snack me',
            'ts': '1000.789',
            'user': 'U1234',
        }
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response(notify=[Notify.BASE]))

        write = _data(members=_members_new)
        mock_pins.assert_not_called()
        mock_snacks.assert_called_once_with()
        self.mock_open.assert_called_once_with(Snacks._data(), 'w')
        self.mock_handle.write.assert_called_once_with(dumps(write) + '\n')
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        calls = [
            mock.call('a', 'C9YE6NQG0', '1000.789'),
            mock.call('star', 'C9YE6NQG0', '1000.789')
        ]
        self.mock_reactions.assert_has_calls(calls)

    def test_on_message__with_invalid_channel(self):
        obj = {
            'channel': 'C1234',
            'text': '<@U3ULC7DBP> discuss topic',
            'ts': '1000.789',
            'user': 'U1234',
        }
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message__with_invalid_text(self):
        obj = {
            'channel': 'C9YE6NQG0',
            'text': 'invalid',
            'ts': '1000.789',
            'user': 'U1234',
        }
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_on_message__with_invalid_timestamp(self):
        obj = {
            'channel': 'C9YE6NQG0',
            'text': '<@U3ULC7DBP> discuss topic',
            'ts': '105.456',
            'user': 'U1234',
        }
        plugin = self.create_plugin(_data())
        response = plugin._on_message_internal(obj=obj)
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_run(self):
        plugin = self.create_plugin(_data())
        response = plugin._run_internal()
        self.assertEqual(response, Response())

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_setup(self):
        plugin = self.create_plugin(_data())
        response = plugin._setup_internal(date=_then)
        self.assertEqual(
            response, Response(task=[Task(target='_load_internal')]))

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    def test_shadow(self):
        plugin = self.create_plugin(_data())
        value = plugin._shadow_internal()
        self.assertEqual(value, [])

        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()

    @mock.patch('plugin.snacks.snacks.os.listdir')
    def test_fnames(self, mock_listdir):
        mock_listdir.return_value = ['C1234.txt', 'C5678.txt']

        actual = Snacks._fnames()
        expected = [
            os.path.join(_root, 'resource/corpus', 'C1234.txt'),
            os.path.join(_root, 'resource/corpus', 'C5678.txt')
        ]
        self.assertEqual(actual, expected)

    @mock.patch('plugin.snacks.snacks.users_list')
    def test_names(self, mock_users):
        mock_users.return_value = {
            'ok': True,
            'members': [{
                'id': 'U1234',
                'name': 'user'
            }]
        }

        actual = Snacks._names()
        expected = {'U1234': 'user'}
        self.assertEqual(actual, expected)

    @mock.patch('plugin.snacks.snacks.random.choice')
    def test_snacks__with_different_values(self, mock_random):
        mock_random.side_effect = ['a', 'b']

        actual = Snacks._snacks()
        expected = ['a', 'b']
        self.assertEqual(actual, expected)

        calls = [mock.call(_snacklist), mock.call(_snacklist)]
        mock_random.assert_has_calls(calls)

    @mock.patch('plugin.snacks.snacks.random.choice')
    def test_snacks__with_same_value(self, mock_random):
        mock_random.side_effect = ['a', 'a']

        actual = Snacks._snacks()
        expected = ['a', 'star']
        self.assertEqual(actual, expected)

        calls = [mock.call(_snacklist), mock.call(_snacklist)]
        mock_random.assert_has_calls(calls)

    @mock.patch('plugin.snacks.snacks.open', create=True)
    @mock.patch('plugin.snacks.snacks.channels_list')
    def test_corpus(self, mock_channels, mock_open):
        mock_channels.return_value = {
            'ok': True,
            'channels': [{
                'id': 'C1234'
            }]
        }
        mo = mock.mock_open(read_data='')
        mock_handle = mo()
        mock_open.side_effect = [mo.return_value]

        names = {'U1234': 'foo', 'U5678': 'bar'}
        plugin = self.create_plugin(_data(), names=names)
        plugin._corpus()

        mock_channels.assert_called_once_with()
        mock_open.assert_called_once_with(
            os.path.join(_root, 'resource/corpus', 'U1234.txt'), 'w')
        mock_handle.write.assert_called_once_with('reply.\nfoo.\nbar.\nbaz.')
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_called_once_with('C1234', {
            'U1234': 'foo',
            'U5678': 'bar'
        })
        self.mock_reactions.assert_not_called()

    @mock.patch.object(Snacks, '_load_internal')
    @mock.patch.object(Snacks, '_corpus')
    def test_load(self, mock_corpus, mock_load_internal):
        mock_load_internal.return_value = Response()

        names = {'U1234': 'foo', 'U5678': 'bar'}
        plugin = self.create_plugin(_data(), names=names)
        plugin.loaded = False
        response = plugin._load()
        self.assertEqual(response, Response())

        mock_corpus.assert_called_once_with()
        mock_load_internal.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        self.mock_cfd.assert_not_called()
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertFalse(plugin.loaded)

    @mock.patch.object(Snacks, '_names')
    @mock.patch.object(Snacks, '_fnames')
    def test_load_internal(self, mock_fnames, mock_names):
        fpath = os.path.join(_root, 'resource/corpus', '{}.txt')
        fnames = [fpath.format(u) for u in ['U1234', 'U5678']]
        mock_fnames.return_value = fnames

        names = {'U1234': 'foo', 'U5678': 'bar'}
        plugin = self.create_plugin(_data(), names=names)
        plugin.loaded = False
        response = plugin._load_internal()
        self.assertEqual(response, Response())

        mock_fnames.assert_called_once_with()
        mock_names.assert_called_once_with()
        self.mock_open.assert_not_called()
        self.mock_handle.write.assert_not_called()
        calls = [
            mock.call(4, *[fnames[0]]),
            mock.call(4, *[fnames[1]]),
            mock.call(4, *fnames)
        ]
        self.mock_cfd.assert_has_calls(calls)
        self.mock_chat.assert_not_called()
        self.mock_collect.assert_not_called()
        self.mock_reactions.assert_not_called()
        self.assertTrue(plugin.loaded)


if __name__ == '__main__':
    unittest.main()
