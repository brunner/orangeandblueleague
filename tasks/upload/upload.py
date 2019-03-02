#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Alerts whenever a new league file is uploaded."""

import datetime
import logging
import os
import re
import sys

_logger = logging.getLogger('filefairy')
_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/tasks/upload', '', _path))

from api.registrable.registrable import Registrable  # noqa
from common.datetime_.datetime_ import datetime_as_pst  # noqa
from common.datetime_.datetime_ import datetime_datetime_cst  # noqa
from common.datetime_.datetime_ import encode_datetime  # noqa
from common.re_.re_ import search  # noqa
from common.requests_.requests_ import get  # noqa
from common.slack.slack import chat_post_message  # noqa
from data.notify.notify import Notify  # noqa
from data.response.response import Response  # noqa

EXPORTS_URL = 'https://statsplus.net/oblootp/exports/'


class Upload(Registrable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return ''

    @staticmethod
    def _info():
        return 'Monitors league file upload status.'

    @staticmethod
    def _title():
        return 'upload'

    def _run_internal(self, **kwargs):
        date = self._get_date()
        if date is not None and date != self.data['date']:
            _logger.log(logging.INFO, 'File is up.')
            chat_post_message('fairylab', 'File is up.')

            self.data['date'] = date
            self.write()

            return Response(notify=[Notify.UPLOAD_FINISH])

        return Response()

    @staticmethod
    def _get_date():
        text = re.sub('[.,]', '', get(EXPORTS_URL))
        match = search(r'(?s)League File: (\w+ \d+ \d+ \d+:\d+ \w+) CST', text)
        if match:
            month, remainder = match.split(' ', 1)
            match = month[:3] + ' ' + remainder

            d = datetime.datetime.strptime(match.title(), '%b %d %Y %I:%M %p')
            c = datetime_datetime_cst(d.year, d.month, d.day, d.hour, d.minute)

            return encode_datetime(datetime_as_pst(c))
