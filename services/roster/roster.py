#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for storing gameday player information."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/roster', '', _path))

from common.datetime_.datetime_ import suffix  # noqa
from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import span  # noqa
from common.elements.elements import row  # noqa
from common.elements.elements import table  # noqa
from common.events.events import get_position  # noqa
from common.events.events import get_title  # noqa
from common.events.events import get_written  # noqa
from common.math.math import crange  # noqa
from common.reference.reference import player_to_bats  # noqa
from common.reference.reference import player_to_name  # noqa
from common.reference.reference import player_to_name_sub  # noqa
from common.reference.reference import player_to_number  # noqa
from common.reference.reference import player_to_throws  # noqa
from common.service.service import call_service  # noqa
from common.teams.teams import encoding_to_lower  # noqa

BALLPARK = """<div class="ballpark css-style-ballpark">
<svg class="ballpark-inner"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink">
<image xlink:href="https://brunnerj.com/fairylab/images/teams/{0}/{0}-ballpark.png"
       width="256" height="256"></image>
<circle cx="128" cy="184" r="6"
        stroke="#000000" stroke-width="2" fill="#ffffff"></circle>
</svg>
{1}
{2}
"""

SMALLCAPS = {k: v for k, v in zip('BCDFHLPRS', 'ʙᴄᴅꜰʜʟᴘʀs')}


class Roster(object):
    def __init__(self, data):
        self.away_team = data['away_team']
        self.home_team = data['home_team']

        self.colors = {}
        self.colors[self.away_team] = data['away_colors'].split()
        self.colors[self.home_team] = data['home_colors'].split()

        self.batting = self.away_team
        self.throwing = self.home_team

        self.batters = {}
        self.indices = {self.away_team: 0, self.home_team: 0}
        self.fielders = {self.away_team: {}, self.home_team: {}}
        self.lineups = {self.away_team: [], self.home_team: []}
        for team in ['away', 'home']:
            encoding = data[team + '_team']
            fielders = self.fielders[encoding]
            lineups = self.lineups[encoding]
            for line in data[team + '_batting']:
                player, pos, _ = line.split()
                curr, change = self.pop_change(pos)
                i = len(lineups)
                fielders[curr] = player
                lineups.append([player])
                self.batters[player] = [curr, change, i, None]
            for line in data[team + '_bench']:
                player, pos, _, prev = line.split()
                self.batters[player] = [None, pos, self.batters[prev][2], prev]
            if 'P' not in fielders:
                fielders['P'] = data[team + '_pitcher']

        self.pitchers = {}
        self.pitchers[self.away_team] = [data['away_pitcher']]
        self.pitchers[self.home_team] = [data['home_pitcher']]

        self.injuries = data['injuries']

    def create_ballpark_table(self):
        aargs = (self.away_team, self.colors[self.away_team], None, 'front',
                 ['jersey-ballpark', 'jersey-left'])
        aimg = call_service('uniforms', 'jersey_absolute', aargs)
        hargs = (self.home_team, self.colors[self.home_team], None, 'front',
                 ['jersey-ballpark', 'jersey-right'])
        himg = call_service('uniforms', 'jersey_absolute', hargs)

        lower = encoding_to_lower(self.home_team)
        clazz = 'border mb-3'
        bcols = [col(clazz='p-0')]
        body = [row(cells=[cell(content=BALLPARK.format(lower, aimg, himg))])]
        return table(clazz=clazz, bcols=bcols, body=body)

    def create_live_batter_table(self):
        return self.create_batter_table(True)

    def create_old_batter_table(self):
        return self.create_batter_table(False)

    def create_batter_table(self, live):
        team = self.batting
        player = self.get_batter()

        hand = SMALLCAPS.get(player_to_bats(player), 'ʀ')
        name = player_to_name(player)
        num = player_to_number(player)
        curr = self.batters[player][0]
        pos = ''.join(SMALLCAPS.get(c, c) for c in curr) + ' '
        stats = ''
        num_text, pos_text = num, pos

        if live:
            hand = span(id_='livesimBatterHand', text=hand)
            name = span(id_='livesimBatterName', text=name)
            num_text = span(id_='livesimBatterNum', text=num)
            pos_text = span(id_='livesimBatterPos', text=pos)

        s = 'ᴀᴛ ʙᴀᴛ: {}#{} ({})<br>{}<br>{}'
        s = s.format(pos_text, num_text, hand, name, stats)
        content = self.create_jersey_content(team, num, 'back', s)
        body = [row(cells=[cell(content=content)])]
        id_ = 'livesimBatterTable' if live else ''
        clazz = 'border' if live else 'border border-bottom-0'
        return table(id_=id_, clazz=clazz, body=body)

    def create_live_pitcher_table(self):
        return self.create_pitcher_table(True)

    def create_old_pitcher_table(self):
        return self.create_pitcher_table(False)

    def create_pitcher_table(self, live):
        team = self.throwing
        player = self.get_pitcher()

        hand = SMALLCAPS.get(player_to_throws(player), 'ʀ')
        name = player_to_name(player)
        num = player_to_number(player)
        num_text = num

        if live:
            hand = span(id_='livesimPitcherHand', text=hand)
            name = span(id_='livesimPitcherName', text=name)
            num_text = span(id_='livesimPitcherNum', text=num)

        pos = ''
        stats = ''

        s = 'ᴘɪᴛᴄʜɪɴɢ: {}#{} ({})<br>{}<br>{}'
        s = s.format(pos, num_text, hand, name, stats)
        content = self.create_jersey_content(team, num, 'back', s)
        body = [row(cells=[cell(content=content)])]
        return table(clazz='border border-bottom-0', body=body)

    def create_due_up_row(self):
        due = []
        i = self.get_index()
        for j in crange((i + 1) % 9, (i + 3) % 9, 9):
            due.append(self.get_batter_at(j))

        s = 'ᴅᴜᴇ ᴜᴘ:<br>{}<br>'.format(player_to_name_sub(', '.join(due)))
        content = self.create_jersey_content(self.batting, None, 'front', s)
        return row(cells=[cell(content=content)])

    def create_jersey_content(self, team, num, side, s):
        args = (team, self.colors[team], num, side)
        img = call_service('uniforms', 'jersey_absolute', args, [])
        spn = span(classes=['jersey-profile-text', 'align-middle', 'd-block'],
                   text=s)
        inner = img + spn

        div = ('<div class="position-relative css-style-h-58px css-style-jerse'
               'y">{}</div>')
        return div.format(inner)

    def create_bolded_row(self, title, text):
        content = player_to_name_sub('<b>{}</b><br>{}'.format(title, text))
        return [cell(col=col(colspan='2'), content=content)]

    def get_batter_at(self, i):
        return self.lineups[self.batting][i][0]

    def get_batter(self):
        return self.get_batter_at(self.get_index())

    def get_fielder(self, position):
        return self.fielders[self.throwing][position]

    def get_index(self):
        return self.indices[self.batting]

    def get_pitcher(self):
        return self.pitchers[self.throwing][0]

    def get_scoring(self, scoring):
        zones = scoring.replace('U', '').split('-')
        zones = [self.get_title_fielder(get_position(z, False)) for z in zones]

        if len(zones) > 1:
            return ' to '.join(zones)
        return zones[0] + ' unassisted'

    def get_styles(self):
        jerseys = [(team, self.colors[team]) for team in self.colors]
        return call_service('uniforms', 'jersey_style', (*jerseys, ))

    def get_title_fielder(self, position):
        return get_title(position) + ' ' + self.get_fielder(position)

    def handle_change_batter(self, batter, tables):
        start = self.get_index()
        end = (start + 8) % 9
        for i in crange(start, end, 9):
            if batter == self.get_batter_at(i):
                self.indices[self.batting] = i
                break
        else:
            _1, change, i, prev = self.batters[batter]
            curr, change = self.pop_change(change)
            self.batters[batter] = [curr, change, i, prev]
            self.lineups[self.batting][i].insert(0, batter)
            self.indices[self.batting] = i
            self.handle_possible_injury(prev, tables)
            bold = 'Offensive Substitution'
            text = 'Pinch hitter {} replaces {}.'.format(batter, prev)
            tables.append_old_body(self.create_bolded_row(bold, text))

        player = self.get_batter()
        hand = SMALLCAPS.get(player_to_bats(player), 'ʀ')
        tables.append_live_event(('change', 0, '#livesimBatterHand', hand))
        name = player_to_name(player)
        tables.append_live_event(('change', 0, '#livesimBatterName', name))
        num = player_to_number(player)
        tables.append_live_event(('change', 0, '#livesimBatterNum', num))
        curr = self.batters[player][0]
        pos = ''.join(SMALLCAPS.get(c, c) for c in curr) + ' '
        tables.append_live_event(('change', 0, '#livesimBatterPos', pos))

    def handle_change_fielder(self, player, tables):
        curr, change, i, prev = self.batters[player]
        position, change = self.pop_change(change)

        if curr is None:
            self.handle_possible_injury(prev, tables)
            bold = 'Defensive Substitution'
            title = get_title(self.batters[prev][0])
            title = title + ' ' if title else ''
            text = '{} replaces {}{}, batting {}{}, playing {}.'.format(
                player, title, prev, i + 1, suffix(i + 1),
                get_written(position))
            tables.append_old_body(self.create_bolded_row(bold, text))
        elif curr == 'PH' or curr == 'PR':
            bold = 'Defensive Switch'
            text = '{} remains in the game as the {}.'.format(
                player, get_title(position))
            tables.append_old_body(self.create_bolded_row(bold, text))
        else:
            bold = 'Defensive Switch'
            text = 'Defensive switch from {} to {} for {}.'.format(
                get_title(curr), get_title(position), player)
            tables.append_old_body(self.create_bolded_row(bold, text))

        self.batters[player] = [position, change, i, prev]
        self.lineups[self.throwing][i].insert(0, player)

        fielder = self.fielders[self.throwing][position]
        _1, _2, j, _3 = self.batters[fielder]
        if self.lineups[self.throwing][j][0] == fielder:
            self.handle_change_fielder(fielder, tables)

        self.fielders[self.throwing][position] = player

    def handle_change_inning(self):
        self.batting, self.throwing = self.throwing, self.batting

    def handle_change_pitcher(self, pitcher, tables):
        prev = self.get_pitcher()
        self.handle_possible_injury(prev, tables)

        bold = 'Pitching Substitution'
        if pitcher in self.batters:
            _, change, i, prev = self.batters[pitcher]
            curr, change = self.pop_change(change)
            title = get_title(self.batters[prev][0])
            title = title + ' ' if title else ''
            text = '{} replaces {}, batting {}{}, replacing {}{}.'.format(
                pitcher, prev, i + 1, suffix(i + 1), title, prev)
            tables.append_old_body(self.create_bolded_row(bold, text))
            self.batters[pitcher] = [curr, change, i, prev]
            self.lineups[self.throwing][i].insert(0, pitcher)
        else:
            text = '{} replaces {}.'.format(pitcher, prev)
            tables.append_old_body(self.create_bolded_row(bold, text))

        self.pitchers[self.throwing].insert(0, pitcher)
        self.fielders[self.throwing]['P'] = pitcher

    def handle_change_runner(self, runner, tables):
        _, change, i, prev = self.batters[runner]
        if change.startswith('PR,'):
            curr, change = self.pop_change(change)
        else:
            curr = 'PR'
        self.batters[runner] = [curr, change, i, prev]
        self.lineups[self.batting][i].insert(0, runner)
        self.handle_possible_injury(prev, tables)
        bold = 'Offensive Substitution'
        text = 'Pinch runner {} replaces {}.'.format(runner, prev)
        tables.append_old_body(self.create_bolded_row(bold, text))

    def handle_possible_injury(self, player, tables):
        if player in self.injuries:
            bold = 'Injury Delay'
            text = '{} was injured {}.'.format(player, self.injuries[player])
            tables.append_old_body(self.create_bolded_row(bold, text))

    def is_change_pitcher(self, pitcher):
        return pitcher != self.get_pitcher()

    def pop_change(self, change):
        curr, change = (change + ',').split(',', 1)
        return (curr, change.strip(','))


def create_roster(data):
    return Roster(data)
