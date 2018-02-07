#!/usr/bin/env python

import abc
import os
import re
import sys

sys.path.append(
    re.sub(r'/apis/messageable', '', os.path.dirname(
        os.path.abspath(__file__))))
from apis.nameable.nameable_api import NameableApi  # noqa
from utils.slack.slack_util import chat_post_message, testing_id, testing_name  # noqa


class MessageableApi(NameableApi):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(MessageableApi, self).__init__()

    def _name(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def _on_message_internal(self, obj):
        pass

    def _on_message(self, obj):
        text = obj.get('text', '')
        if obj.get('channel', '') == testing_id and self._name() in text:
            for method in dir(self):
                if method not in text or method.startswith('_'):
                    continue

                item = getattr(self, method)
                if not callable(item):
                    continue

                pattern = r'' + self._name() + '\.' + method + '\((.*)\)'
                match = re.findall(pattern, text)
                if match:
                    return item(a=match[0], v='true')

        return self._on_message_internal(obj)