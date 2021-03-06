#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for displaying divisional standings."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/division', '', _path))

from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import row  # noqa
from common.elements.elements import table  # noqa
from common.record.record import decode_record  # noqa
from common.teams.teams import encoding_to_hometown  # noqa
from common.teams.teams import encoding_to_teamid  # noqa
from common.teams.teams import icon_absolute  # noqa
from common.teams.teams import team_badge  # noqa


def _diff(record1, record2):
    w1, l1 = decode_record(record1)
    w2, l2 = decode_record(record2)

    return (w2 - w1 + l1 - l2) / 2.0


def _record(tuple_or_str):
    return tuple_or_str[0] if isinstance(tuple_or_str, tuple) else tuple_or_str


def _sort(table_):
    def sort(team1):
        record1 = _record(table_[team1])
        tw, tl = decode_record(record1)

        records = [_record(table_[team2]) for team2 in table_]
        diff = abs(min([_diff(record1, record2) for record2 in records]))

        pcnt = float(tw) / ((tw + tl) or 1)
        invs = 1.0 / tl if tl else 2
        name = 1.0 / int(encoding_to_teamid(team1))

        return (diff, pcnt, tw, invs, name)

    return sorted(table_, key=sort, reverse=True)


def _expanded(table_, groups, i):
    ret = {}

    teams = _sort(table_)

    if teams[0] in groups:
        i += 1

    for team1 in table_:
        record1 = _record(table_[team1])

        diff = _diff(record1, _record(table_[teams[i]]))
        prefix = '+' if diff < 0 else ''
        gb = '-' if diff == 0 else prefix + str(abs(diff))

        ret[team1] = (record1, gb)

    return ret


def condensed_league(league, tables):
    """Create a condensed-view table for a given league's standings.

    The condensed-view table shows a number of rows (one for each subleague),
    with each row column containing the team logo and record. The rows are
    sorted left to right, first place to last place.

    The expected format for a subleague table is a tuple of two elements, the
    first being the subleague name and the second being a dictionary mapping
    from team encoding to a tuple of team record and a boolean denoting whether
    or not the team badge should be active.

    Args:
        league: The league name.
        tables: The list of subleague tables.

    Returns:
        A renderable table element in the condensed-view style.
    """
    body = []
    colspan = 0

    for _, table_ in tables:
        body_cells = []
        colspan = max(colspan, len(table_))

        records = {k: table_[k][0] for k in table_}
        for team in _sort(records):
            record, active = table_[team]
            body_cells.append(cell(content=team_badge(team, record, active)))

        body.append(row(cells=body_cells))

    remaining = colspan - 2
    bcols = [col(clazz=('css-style-w-20pct badge-team-wrapper pl-2'))]
    bcols += [col(clazz=('css-style-w-20pct badge-team-wrapper'))] * remaining
    bcols += [col(clazz=('css-style-w-20pct badge-team-wrapper pr-2'))]

    hc = 'font-weight-bold text-dark text-center'
    return table(clazz='table-fixed border mb-3',
                 hcols=[col(clazz=hc, colspan=colspan)],
                 bcols=bcols,
                 head=[row(cells=[cell(content=league)])],
                 body=body)


def expanded_impl(league, tables):
    """Transform a given league's standings into expanded-view data.

    The expanded-view data is a list of subleague tuples. Each subleague tuple
    consists of two elements, the first being the combined league + subleague
    name and the second being a dictionary mapping from team encoding to
    another tuple, this one consisting of the team's record and the number of
    games that the team is behind the subleague leader.

    Args:
        league: The league name.
        tables: The list of subleague tables.

    Returns:
        A list of subleague tuples.
    """
    ret = []

    groups = []
    wc = {}

    abbr = ''.join(s[0] for s in league.split(' '))
    for subleague, table_ in tables:
        expanded = _expanded(table_, [], 0)

        group = []
        teams = _sort(expanded)
        for i, team in enumerate(teams):
            if expanded[team][1] == '-':
                group.append(team)
            elif i == 1:
                table_.pop(teams[0])

        groups.append(group)
        wc.update(table_)

        ret.append((abbr + ' ' + subleague, expanded))

    ret.append((abbr + ' Wild Card', _expanded(wc, groups, 1)))
    return ret


def expanded_league(league, tables):
    """Create a expanded-view table list for a given league's standings.

    The expanded-view table list consists of a table for each subleague, sorted
    top to bottom, first place to last place, as well as an additional table
    for the league wild card.

    The expected format for a subleague table is a tuple of two elements, the
    first being the subleague name and the second being a dictionary mapping
    from team encoding to team record.

    Args:
        league: The league name.
        tables: The list of subleague tables.

    Returns:
        A list of renderable table elements in the expanded-view style.
    """
    ret = []

    for subleague, table_ in expanded_impl(league, tables):
        body = []
        for team in _sort(table_)[:5]:
            hometown = encoding_to_hometown(team)
            record, gb = table_[team]
            rw, rl = decode_record(record)

            pct = 0 if rw + rl == 0 else rw / (rw + rl)
            pct = '{:,.3f}'.format(pct).lstrip('0')

            body_cells = []
            contents = [icon_absolute(team, hometown), rw, rl, pct, gb]
            for content in contents:
                body_cells.append(cell(content=str(content)))

            body.append(row(cells=body_cells))

        contents = [subleague, 'W', 'L', '%', 'GB']
        head = [row(cells=[cell(content=content) for content in contents])]

        hc = 'font-weight-bold text-dark '
        clazzes = [
            'position-relative text-truncate',
            'text-right css-style-w-40px',
            'text-right css-style-w-40px',
            'text-right css-style-w-50px',
            'text-right css-style-w-54px',
        ]

        ret.append(
            table(
                clazz='table-fixed border mb-3',
                hcols=[col(clazz=(hc + c)) for c in clazzes],
                bcols=[col(clazz=c) for c in clazzes],
                head=head,
                body=body,
            ))

    return ret
