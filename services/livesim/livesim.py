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


class State(object):
    def __init__(self, data):
        self.away_team = data['away_team']
        self.home_team = data['home_team']

        self.runs = {self.away_team: 0, self.home_team: 0}

        self.colors = {}
        self.colors[self.away_team] = data['away_colors'].split()
        self.colors[self.home_team] = data['home_colors'].split()

        self.pitchers = {}
        self.pitchers[self.away_team] = data['away_pitcher']
        self.pitchers[self.home_team] = data['home_pitcher']

        self.batting = self.home_team
        self.throwing = self.away_team

        self.batter = None
        self.pitcher = self.pitchers[self.home_team]

        self.half = 0
        self.change = True
        self.outs = 0

        self.pitch = 0
        self.balls = 0
        self.strikes = 0

        self.bases = [None, None, None]
        self.scored = []

    @staticmethod
    def _get_pitch_clazz(text):
        if 'Ball' in text:
            return 'success'
        if 'In play' in text:
            return 'primary'
        return 'danger'

    def create_batter_table(self, tables):
        clazz = 'border mb-3'
        hc = [col(colspan='2', clazz='font-weight-bold text-dark')]
        bc = [col(), col(clazz='text-right w-50p')]
        head = [[cell(content=self.to_head_str())]]

        body = tables.get_body()
        body.append(self.create_player_row(False))
        body.append(self.create_player_row(True))

        table_ = table(clazz=clazz, hcols=hc, bcols=bc, head=head, body=body)
        tables.append_table(table_)
        tables.reset_body()

    def create_player_row(self, bats):
        team = self.batting if bats else self.throwing
        player = self.batter if bats else self.pitcher
        position = ''

        title = 'ᴀᴛ ʙᴀᴛ' if bats else 'ᴘɪᴛᴄʜɪɴɢ'
        hand = player_to_bats(player) if bats else player_to_throws(player)
        name = player_to_name(player)
        num = player_to_number(player)
        pos = ''.join(SMALLCAPS.get(c, c) for c in position)
        stats = ''

        s = '{}: {} #{} ({})<br>{}<br>{}'
        s = s.format(title, pos, num, SMALLCAPS.get(hand, 'ʀ'), name, stats)

        args = (team, self.colors[team], num, 'back')
        img = call_service('uniforms', 'jersey_absolute', args)
        spn = span(classes=['profile-text', 'align-middle', 'd-block'], text=s)
        inner = img + spn

        content = '<div class="position-relative h-58p">{}</div>'.format(inner)
        return [cell(col=col(colspan='2'), content=content)]

    def create_pitch_row(self, text, tables):
        clazz = self._get_pitch_clazz(text)
        pill = '<div class="badge badge-pill pitch alert-{}">{}</div>'
        left = cell(content=(pill.format(clazz, self.pitch) + text))
        count = '{} - {}'.format(self.balls, self.strikes)
        right = cell(content=span(classes=['text-secondary'], text=count))
        tables.append_body([left, right])

    def create_batting_substitution_row(self, args, tables):
        title = 'Offensive Substitution'
        text = 'Pinch hitter: {}'.format(*args)
        tables.append_body(self.create_titled_row(title, text))

    def create_fielding_substitution_row(self, args, tables):
        title = 'Defensive Substitution'
        text = 'Now in {}: {}'.format(*args)
        tables.append_body(self.create_titled_row(title, text))

    def create_pitching_substitution_row(self, args, tables):
        pitcher, = args
        title = 'Pitching Substitution'
        text = '{} replaces {}.'.format(pitcher, self.pitchers[self.throwing])
        tables.append_body(self.create_titled_row(title, text))

    def create_running_substitution_row(self, args, tables):
        title = 'Offensive Substitution'
        text = 'Pinch runner at {}: {}'.format(*args)
        tables.append_body(self.create_titled_row(title, text))

    def create_titled_row(self, title, text):
        content = player_to_name_sub('<b>{}</b><br>{}'.format(title, text))
        return [cell(col=col(colspan='2'), content=content)]

    def create_summary_row(self, tables):
        content = player_to_name_sub(' '.join(tables.get_summary()))
        if 'out' in content:
            content += ' <b>{}</b>'.format(self.to_outs_str())
        tables.append_body([cell(col=col(colspan='2'), content=content)])

    def get_batter(self):
        return self.batter

    def get_change_inning(self):
        return self.change

    def get_styles(self):
        jerseys = [(team, self.colors[team]) for team in self.colors]
        return call_service('uniforms', 'jersey_style', (*jerseys, ))

    def handle_batter_to_base(self, base):
        for i in range(base, 0, -1):
            if self.bases[i - 1]:
                self.handle_runner_to_base(self.bases[i - 1], base + 1)
                self.bases[i - 1] = None
        self.bases[base - 1] = self.batter

    def handle_change_batter(self, args):
        self.batter, = args
        self.pitch = 0
        self.balls = 0
        self.strikes = 0

    def handle_change_inning(self, tables):
        self.half += 1
        self.change = False
        self.batting, self.throwing = self.throwing, self.batting
        self.batter = None
        self.pitcher = self.pitchers[self.throwing]
        self.outs = 0
        self.bases = [None, None, None]
        tables.append_table(topper(self.to_inning_str()))

    def handle_change_pitcher(self, pitcher):
        self.pitcher = pitcher
        self.pitchers[self.throwing] = pitcher

    def handle_out_batter(self):
        self.handle_out()

    def handle_out_runner(self, base):
        self.handle_out()
        self.bases[base - 1] = None

    def handle_out(self):
        self.outs += 1

    def handle_pitch_ball(self):
        self.handle_pitch()
        self.balls += 1

    def handle_pitch_foul(self):
        self.handle_pitch()
        self.strikes = min(2, self.strikes + 1)

    def handle_pitch_strike(self):
        self.handle_pitch()
        self.strikes += 1

    def handle_pitch(self):
        self.pitch += 1

    def handle_runner_to_base(self, player, base):
        if base > 3:
            self.scored.append(player)
            return
        elif self.bases[base - 1]:
            self.handle_runner_to_base(self.bases[base - 1], base + 1)
        self.bases[base - 1] = player

    def is_change_pitcher(self, pitcher):
        return pitcher != self.pitcher

    def is_strikeout(self):
        return self.strikes == 3

    def set_change_inning(self):
        self.change = True

    def to_bases_str(self):
        first, second, third = self.bases
        if first and second and third:
            return 'Bases loaded'
        if first and second:
            return 'Runners on 1st and 2nd'
        if first and third:
            return 'Runners on 1st and 3rd'
        if second and third:
            return 'Runners on 2nd and 3rd'
        if first:
            return 'Runner on 1st'
        if second:
            return 'Runner on 2nd'
        if third:
            return 'Runner on 3rd'
        return 'Bases empty'

    def to_head_str(self):
        return '{} &nbsp;|&nbsp; {}, {}'.format(self.to_score_str(),
                                                self.to_bases_str(),
                                                self.to_outs_str())

    def to_inning_str(self):
        s = 'Top' if self.half % 2 == 1 else 'Bottom'
        n = (self.half + 1) // 2
        return '{} {}{}'.format(s, n, suffix(n))

    def to_outs_str(self):
        return '{} out'.format(self.outs)

    def to_score_str(self):
        s = '{} {} · {} {}'.format(
            self.away_team,
            self.runs[self.away_team],
            self.home_team,
            self.runs[self.home_team],
        )
        return encoding_to_abbreviation_sub(s)


class Tables(object):
    def __init__(self):
        self.body = []
        self.foot = []
        self.summary = []
        self.table = table()
        self.tables = []

    def append_all(self):
        for row in self.body:
            tbody(self.table, row)
        for row in self.foot:
            tbody(self.table, row)

    def append_foot(self, row):
        self.foot.append(row)

    def append_body(self, row):
        self.body.append(row)

    def append_summary(self, s):
        self.summary.append(s)

    def append_table(self, table_):
        self.table = table_
        self.tables.append(table_)

    def get_body(self):
        return list(self.body)

    def get_summary(self):
        return list(self.summary)

    def get_tables(self):
        return self.tables

    def reset_all(self):
        self.body = []
        self.foot = []
        self.summary = []

    def reset_body(self):
        self.body = []

    def reset_summary(self):
        self.summary = []


EVENT_CHANGES = [
    Event.CHANGE_INNING,
    Event.CHANGE_BATTER,
    Event.CHANGE_FIELDER,
    Event.CHANGE_PINCH_HITTER,
    Event.CHANGE_PINCH_RUNNER,
    Event.CHANGE_PITCHER,
]


def _check_change_events(e, args, state, tables):
    if e == Event.CHANGE_INNING:
        state.set_change_inning()
    elif state.get_change_inning():
        state.handle_change_inning(tables)

    if e in [Event.CHANGE_BATTER, Event.CHANGE_PINCH_HITTER]:
        if e == Event.CHANGE_PINCH_HITTER:
            state.create_batting_substitution_row(args, tables)
        state.handle_change_batter(args)
        state.create_batter_table(tables)
    if e == Event.CHANGE_FIELDER:
        state.create_fielding_substitution_row(args, tables)
    if e == Event.CHANGE_PINCH_RUNNER:
        state.create_running_substitution_row(args, tables)
    if e == Event.CHANGE_PITCHER:
        pitcher, = args
        if state.is_change_pitcher(pitcher):
            state.create_pitching_substitution_row(args, tables)
            state.handle_change_pitcher(pitcher)


EVENT_SINGLE_BASES = [
    Event.BATTER_SINGLE,
    Event.BATTER_SINGLE_APPEAL,
    Event.BATTER_SINGLE_BATTED_OUT,
    Event.BATTER_SINGLE_BUNT,
    Event.BATTER_SINGLE_INFIELD,
    Event.BATTER_SINGLE_ERR,
    Event.BATTER_SINGLE_STRETCH,
]


def _check_single_base_events(e, args, state, tables):
    batter = state.get_batter()
    if e in [Event.BATTER_SINGLE, Event.BATTER_SINGLE_INFIELD]:
        state.handle_batter_to_base(1)
        tables.append_summary('{} singles.'.format(batter))
    if e == Event.BATTER_SINGLE_APPEAL:
        state.handle_batter_to_base(1)
        state.handle_out_runner(1)
        s = '{} singles. Out on appeal for missing first base.'.format(batter)
        tables.append_summary(s)
    if e == Event.BATTER_SINGLE_BATTED_OUT:
        state.handle_batter_to_base(1)
        # TODO: Determine which runner is out.
        # state.handle_out_runner(1)
        state.handle_out()
        s = '{} singles. Runner out being hit by batted ball.'.format(batter)
        tables.append_summary(s)
    if e == Event.BATTER_SINGLE_BUNT:
        state.handle_batter_to_base(1)
        tables.append_summary('{} singles on a bunt.'.format(batter))
    if e == Event.BATTER_SINGLE_ERR:
        state.handle_batter_to_base(2)
        s = '{} singles. Advance to second base on error.'.format(batter)
        tables.append_summary(s)
    if e == Event.BATTER_SINGLE_STRETCH:
        state.handle_batter_to_base(1)
        state.handle_out_runner(1)
        s = '{} singles. Batter out trying to stretch hit.'.format(batter)
        tables.append_summary(s)


EVENT_PITCHES = [
    Event.PITCHER_BALL,
    Event.PITCHER_WALK,
    Event.PITCHER_STRIKE_CALL,
    Event.PITCHER_STRIKE_CALL_TOSSED,
    Event.PITCHER_STRIKE_FOUL,
    Event.PITCHER_STRIKE_FOUL_BUNT,
    Event.PITCHER_STRIKE_FOUL_ERR,
    Event.PITCHER_STRIKE_MISS,
    Event.PITCHER_STRIKE_SWING,
    Event.PITCHER_STRIKE_SWING_OUT,
    Event.PITCHER_STRIKE_SWING_PASSED,
    Event.PITCHER_STRIKE_SWING_WILD,
]


def _check_pitch_events(e, args, state, tables):
    if tables.get_summary():
        state.create_summary_row(tables)
        tables.reset_summary()

    batter = state.get_batter()
    if e == Event.PITCHER_BALL:
        state.handle_pitch_ball()
        state.create_pitch_row('Ball', tables)
    if e in [Event.PITCHER_STRIKE_CALL, Event.PITCHER_STRIKE_CALL_TOSSED]:
        state.handle_pitch_strike()
        state.create_pitch_row('Called Strike', tables)
        if state.is_strikeout():
            state.handle_out_batter()
            s = '{} called out on strikes.'.format(batter)
            tables.append_summary(s)
        if e == Event.PITCHER_STRIKE_CALL_TOSSED:
            s = '{} ejected for arguing the call.'.format(batter)
            tables.append_foot(state.create_titled_row('Ejection', s))
    if e == Event.PITCHER_STRIKE_FOUL:
        state.handle_pitch_foul()
        state.create_pitch_row('Foul', tables)
    if e == Event.PITCHER_STRIKE_SWING:
        state.handle_pitch_strike()
        state.create_pitch_row('Swinging Strike', tables)
        if state.is_strikeout():
            state.handle_out_batter()
            s = '{} strikes out swinging.'.format(batter)
            tables.append_summary(s)


def _group(encodings):
    change = None
    group = []
    for encoding in encodings:
        e, _ = Event.decode(encoding)
        c = e in EVENT_CHANGES
        if not group:
            change = c
            group.append(encoding)
        elif change == c:
            group.append(encoding)
        else:
            yield group
            change = c
            group = [encoding]

    if group:
        yield group


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

    state = State(data)
    tables = Tables()

    for group in _group(data['events']):
        for encoding in group:
            e, args = Event.decode(encoding)

            if e in EVENT_CHANGES:
                _check_change_events(e, args, state, tables)
            if e in EVENT_SINGLE_BASES:
                _check_single_base_events(e, args, state, tables)
            if e in EVENT_PITCHES:
                _check_pitch_events(e, args, state, tables)

        if tables.get_summary():
            state.create_summary_row(tables)
            tables.reset_summary()

        tables.append_all()
        tables.reset_all()

    styles = state.get_styles()
    return {'styles': styles, 'tables': tables.get_tables()}
