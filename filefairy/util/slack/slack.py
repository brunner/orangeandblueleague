#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/util/slack', '', _path))
from util.secrets.secrets import filefairy  # noqa
from util.urllib_.urllib_ import urlopen  # noqa

logger_ = logging.getLogger('fairylab')
_filefairy = filefairy()


def _call(method, params):
    url = 'https://slack.com/api/{}'.format(method)
    obj = {'ok': False}
    try:
        response = urlopen(url, params).decode('utf-8')
        obj = json.loads(response)
    except:
        logger_.log(logging.WARNING, 'Handled warning.', exc_info=True)
    return obj


def channels_history(channel, latest):
    return _call('channels.history', {
        'token': _filefairy,
        'channel': channel,
        'count': 1000,
        'latest': latest,
    })


def channels_list():
    return _call('channels.list', {
        'token': _filefairy,
        'exclude_members': True,
        'exclude_archived': True
    })


def chat_post_message(channel, text, attachments=[]):
    return _call(
        'chat.postMessage', {
            'token': _filefairy,
            'channel': channel,
            'text': text,
            'as_user': 'true',
            'attachments': attachments,
            'link_names': 'true'
        })


def files_upload(content, filename, channel):
    return _call(
        'files.upload', {
            'token': _filefairy,
            'content': content,
            'filename': filename,
            'channels': channel,
        })


def pins_add(channel, timestamp):
    return _call('pins.add', {
        'token': _filefairy,
        'channel': channel,
        'timestamp': timestamp,
    })


def reactions_add(name, channel, timestamp):
    return _call(
        'reactions.add', {
            'token': _filefairy,
            'name': name,
            'channel': channel,
            'timestamp': timestamp,
        })


def rtm_connect():
    return _call('rtm.connect', {'token': _filefairy})


def users_list():
    return _call('users.list', {'token': _filefairy})
