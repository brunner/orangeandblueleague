#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import urllib.error as error
import urllib.parse as parse
import urllib.request as request

logger_ = logging.getLogger('fairylab')


def urlopen(url, params={}):
    try:
        data = parse.urlencode(params).encode('utf-8')
        with request.urlopen(url, data=data, timeout=8) as f:
            return f.read()
    except error.HTTPError as e:
        if e.code != 403:
            logger_.log(logging.WARNING, 'Handled warning.', exc_info=True)
        return b''
    except:
        logger_.log(logging.WARNING, 'Handled warning.', exc_info=True)
        return b''
