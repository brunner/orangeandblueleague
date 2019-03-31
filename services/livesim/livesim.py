#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for displaying live sim data."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/livesim', '', _path))

from common.datetime_.datetime_ import suffix  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import table  # noqa
from common.elements.elements import tbody  # noqa
from common.elements.elements import topper  # noqa
from common.json_.json_ import loads  # noqa
from common.reference.reference import player_to_bats  # noqa
from common.reference.reference import player_to_name  # noqa
from common.reference.reference import player_to_name_sub  # noqa
from common.reference.reference import player_to_number  # noqa
from common.reference.reference import player_to_throws  # noqa
from common.service.service import call_service  # noqa
from common.teams.teams import encoding_to_abbreviation_sub  # noqa
from common.teams.teams import encoding_to_nickname  # noqa
from data.event.event import Event  # noqa

SMALLCAPS = {k: v for k, v in zip('BCDFHLPRS', 'ʙᴄᴅꜰʜʟᴘʀs')}


def _change(title, text):
    content = player_to_name_sub('<b>{}</b><br>{}'.format(title, text))
    return [cell(col=col(colspan='2'), content=content)]


def _inning(half):
    s = 'Top' if half % 2 == 0 else 'Bottom'
    n = (half // 2) + 1
    return '{} {}{}'.format(s, n, suffix(n))


def _pitch(clazz, pitch, balls, strikes, text):
    pill = '<div class="badge badge-pill pitch alert-{}">{}</div>'
    left = cell(content=(pill.format(clazz, pitch) + text))
    count = '{} - {}'.format(balls, strikes)
    right = cell(content=span(classes=['text-secondary'], text=count))
    return [left, right]


def _play(text, runs):
    content = player_to_name_sub(text)
    return [cell(col=col(colspan='2'), content=content)]


def _profile(team, num, colors, s):
    args = (team, colors, num, 'back')
    img = call_service('uniforms', 'jersey_absolute', args)
    spn = '<span class="profile-text align-middle d-block">{}</span>'.format(s)
    return '<div class="position-relative h-58p">{}</div>'.format(img + spn)


def _player(bats, team, player, fielding, colors):
    title = 'ᴀᴛ ʙᴀᴛ' if bats else 'ᴘɪᴛᴄʜɪɴɢ'
    hand = player_to_bats(player) if bats else player_to_throws(player)
    name = player_to_name(player)
    num = player_to_number(player)
    pos = ''.join(SMALLCAPS.get(c, c) for c in fielding)
    stats = ''

    s = '{}: {} #{} ({})<br>{}<br>{}'.format(
        title,
        pos,
        num,
        SMALLCAPS.get(hand, 'ʀ'),
        name,
        stats,
    )
    return [cell(col=col(colspan='2'), content=_profile(team, num, colors, s))]


def _head(score, bases, outs):
    text = encoding_to_abbreviation_sub(score) + ' &nbsp;|&nbsp; '

    first, second, third = bases
    if first and second and third:
        text += 'Bases loaded'
    elif first and second:
        text += 'Runners on 1st and 2nd'
    elif first and third:
        text += 'Runners on 1st and 3rd'
    elif second and third:
        text += 'Runners on 2nd and 3rd'
    elif first:
        text += 'Runner on 1st'
    elif second:
        text += 'Runner on 2nd'
    elif third:
        text += 'Runner on 3rd'
    else:
        text += 'Bases empty'

    text += ', '
    if outs == 2:
        text += '2 outs'
    elif outs == 1:
        text += '1 out'
    else:
        text += '0 outs'

    return [[cell(content=text)]]


def _table(score, bases, outs, body):
    clazz = 'border mb-3'
    hcols = [col(colspan='2', clazz='font-weight-bold text-dark')]
    bcols = [col(), col(clazz='text-right w-50p')]
    head = _head(score, bases, outs)
    return table(clazz=clazz, hcols=hcols, bcols=bcols, head=head, body=body)


def get_html(game_in):
    """Gets template data for a given game data object.

    Args:
        game_in: The game data file path.

    Returns:
        The template data.
    """
    data = loads(game_in)
    if not data['events']:
        return None

    away_team = data['away_team']
    home_team = data['home_team']

    colors = {
        away_team: data['away_colors'].split(),
        home_team: data['home_colors'].split(),
    }
    pitchers = {
        away_team: data['away_pitcher'],
        home_team: data['home_pitcher'],
    }
    runs = {away_team: 0, home_team: 0}

    jerseys = [(encoding, colors[encoding]) for encoding in colors]
    styles = call_service('uniforms', 'jersey_style', (*jerseys, ))

    batting, throwing = home_team, away_team
    batter, pitcher = None, pitchers[home_team]
    half, inning, outs, pitch, balls, strikes = 0, True, 0, 0, 0, 0
    bases = [None, None, None]

    t, body, tables = table(), [], []
    for encoding in data['events']:
        e, args = Event.decode(encoding)
        if e == Event.CHANGE_INNING:
            inning = True
        elif inning:
            tables.append(topper(_inning(half)))
            batting, throwing = throwing, batting
            batter, pitcher = None, pitchers[throwing]
            half, inning, outs = half + 1, False, 0
            bases = [None, None, None]

        if e in [Event.CHANGE_BATTER, Event.CHANGE_PINCH_HITTER]:
            batter, = args
            pitch, balls, strikes = 0, 0, 0
            score = '{} {} · {} {}'.format(away_team, runs[away_team],
                                           home_team, runs[home_team])
            if e == Event.CHANGE_PINCH_HITTER:
                _title = 'Offensive Substitution'
                _text = 'Pinch hitting: {}'.format(batter)
                body.append(_change(_title, _text))
            t, body = _table(score, bases, outs, body), []
            tbody(t, _player(False, throwing, pitcher, '', colors[throwing]))
            tbody(t, _player(True, batting, batter, '', colors[batting]))
            tables.append(t)
            continue
        if e == Event.CHANGE_PITCHER:
            pitcher, = args
            if pitcher == pitchers[throwing]:
                continue
            _title = 'Pitching Substitution'
            _text = '{} replaces {}.'.format(pitcher, pitchers[throwing])
            body.append(_change(_title, _text))
            pitchers[throwing] = pitcher
            continue

        row = None
        if e == Event.PITCHER_BALL:
            pitch, balls = pitch + 1, balls + 1
            row = _pitch('success', pitch, balls, strikes, 'Ball')
        if e in [Event.PITCHER_STRIKE_CALL, Event.PITCHER_STRIKE_CALL_TOSSED]:
            pitch, strikes = pitch + 1, strikes + 1
            row = _pitch('danger', pitch, balls, strikes, 'Called Strike')
            if strikes == 3:
                outs += 1
                _text = '{} called out on strikes. <b>{} out</b>'
                body.append(_play(_text.format(batter, outs), None))
            if e == Event.PITCHER_STRIKE_CALL_TOSSED:
                _title = 'Ejection'
                _text = '{} ejected for arguing the call.'.format(batter)
                body.append(_change(_title, _text))
        if e == Event.PITCHER_STRIKE_FOUL:
            pitch, strikes = pitch + 1, min(2, strikes + 1)
            row = _pitch('danger', pitch, balls, strikes, 'Foul Ball')
        if e == Event.PITCHER_STRIKE_SWING:
            pitch, strikes = pitch + 1, strikes + 1
            row = _pitch('danger', pitch, balls, strikes, 'Swinging Strike')
            if strikes == 3:
                outs += 1
                _text = '{} strikes out swinging. <b>{} out</b>'
                body.append(_play(_text.format(batter, outs), None))
        if row:
            tbody(t, row)
            row = None
        if body:
            for _row in body:
                tbody(t, _row)
            body = []

    return {'styles': styles, 'tables': tables}
