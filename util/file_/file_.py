#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/util/file_', '', _path)
sys.path.append(_root)
from util.subprocess_.subprocess_ import check_output  # noqa

_download = os.path.join(_root, 'resource/download')
_host = 'www.orangeandblueleaguebaseball.com'
_name = 'orange_and_blue_league_baseball.tar.gz'
_url = 'https://' + _host + '/StatsLab/league_file/' + _name


def ping():
    return check_output(['ping', '-c', '1', _host], timeout=8)


def recreate(dirname):
    check_output(['rm', '-rf', dirname])
    check_output(['mkdir', dirname])


def wget_file():
    recreate(_download)
    cwd = os.getcwd()
    os.chdir(_download)

    output = check_output(['wget', _url], timeout=4800)
    if not output.get('ok'):
        return output

    output = check_output(['tar', '-xzf', _name])
    os.chdir(cwd)
    return output