#!/usr/bin/env python
# -*- coding: utf-8 -*-


def _team(logo, body):
    img = '<img src="https://orangeandblueleaguebaseball.com/StatsLab/' + \
          'reports/news/html/images/team_logos/{}_40.png" ' + \
          'width="24" height="24" border="0" class="d-inline-block">'
    span = '<span class="d-inline-block align-middle pl-3">{}</span>'
    body[0] = img.format(logo) + span.format(body[0])
    return body


def _secondary(t):
    return '<span class="text-secondary">' + t + '</span>'


def _success(t):
    return '<span class="text-success border px-1">' + t + '</span>'


subtitle = ''

tmpl = 'exports.html'

_t31 = _team('arizona_diamondbacks', ['ARI', '5 - 5', 'W1'])
_t32 = _team('atlanta_braves', ['ATL', '10 - 0', 'W10'])
_t33 = _team('baltimore_orioles', ['BAL', '6 - 4', 'W1'])
_t34 = _team('boston_red_sox', ['BOS', '10 - 0', 'W10'])
_t35 = _team('chicago_white_sox', ['CWS', '9 - 1', 'L1'])
_t36 = _team('chicago_cubs', ['CHC', '8 - 2', 'L1'])
_t37 = _team('cincinnati_reds', ['CIN', '10 - 0', 'W10'])
_t38 = _team('cleveland_indians', ['CLE', '8 - 2', 'W2'])
_t39 = _team('colorado_rockies', ['COL', '10 - 0', 'W10'])
_t40 = _team('detroit_tigers', ['DET', '10 - 0', 'W10'])
_t41 = _team('miami_marlins', ['MIA', '4 - 6', 'W1'])
_t42 = _team('houston_astros', ['HOU', '10 - 0', 'W10'])
_t43 = _team('kansas_city_royals', ['KC', '9 - 1', 'W5'])
_t44 = _team('los_angeles_angels', ['LAA', '7 - 3', 'L1'])
_t45 = _team('los_angeles_dodgers', ['LAD', '5 - 5', 'W2'])
_t46 = _team('milwaukee_brewers', ['MIL', '10 - 0', 'W10'])
_t47 = _team('minnesota_twins', ['MIN', '10 - 0', 'W10'])
_t48 = _team('new_york_yankees', ['NYY', '10 - 0', 'W10'])
_t49 = _team('new_york_mets', ['NYM', '8 - 2', 'L1'])
_t50 = _team('oakland_athletics', ['OAK', '7 - 3', 'L3'])
_t51 = _team('philadelphia_phillies', ['PHI', '3 - 7', 'L5'])
_t52 = _team('pittsburgh_pirates', ['PIT', '6 - 4', 'L1'])
_t53 = _team('san_diego_padres', ['SD', '9 - 1', 'W8'])
_t54 = _team('seattle_mariners', ['SEA', '10 - 0', 'W10'])
_t55 = _team('san_francisco_giants', ['SF', '2 - 8', 'L4'])
_t56 = _team('st_louis_cardinals', ['STL', '10 - 0', 'W10'])
_t57 = _team('tampa_bay_rays', ['TB', '10 - 0', 'W10'])
_t58 = _team('texas_rangers', ['TEX', '9 - 1', 'W9'])
_t59 = _team('toronto_blue_jays', ['TOR', '9 - 1', 'W4'])
_t60 = _team('washington_nationals', ['WAS', '5 - 5', 'L1'])

context = {
    'title':
    'exports',
    'breadcrumbs': [{
        'href': '/fairylab/',
        'name': 'Home'
    }, {
        'href': '',
        'name': 'Exports'
    }],
    'live': {
        'href':
        '',
        'title':
        '53%',
        'info':
        'Upcoming sim contains ' +
        ', '.join([_success('16 new'), '14 old',
                   _secondary('0 ai')]) + '.',
        'table': {
            'clazz':
            'table-sm',
            'cols': [
                '', 'text-center', 'text-center', 'text-center', 'text-center',
                'text-center'
            ],
            'head': [],
            'body':
            [['AL East', 'BAL', 'BOS', 'NYY', 'TB',
              'TOR'], [
                  'AL Central',
                  _success('CWS'), 'CLE',
                  _success('DET'), 'KC',
                  _success('MIN')
              ], [
                  'AL West', 'HOU',
                  _success('LAA'), 'OAK',
                  _success('SEA'),
                  _success('TEX')
              ], [
                  'NL East',
                  _success('ATL'), 'MIA',
                  _success('NYM'), 'PHI',
                  _success('WAS')
              ], [
                  'NL Central',
                  _success('CHC'),
                  _success('CIN'),
                  _success('MIL'), 'PIT',
                  _success('STL')
              ],
             ['NL West', 'ARI', 'COL',
              _success('LAD'),
              _success('SD'), 'SF']]
        },
        'ts':
        '30s ago',
        'success':
        '',
        'danger':
        ''
    },
    'standings': [{
        'clazz': 'border mt-3',
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['AL East', 'Last 10', 'Streak'],
        'body': [_t34, _t48, _t57, _t59, _t33]
    }, {
        'clazz': 'border mt-3',
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['AL Central', 'Last 10', 'Streak'],
        'body': [_t40, _t47, _t43, _t35, _t38]
    }, {
        'clazz': 'border mt-3',
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['AL West', 'Last 10', 'Streak'],
        'body': [_t42, _t54, _t58, _t44, _t50]
    }, {
        'clazz': 'border mt-3',
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['NL East', 'Last 10', 'Streak'],
        'body': [_t32, _t49, _t60, _t41, _t51]
    }, {
        'clazz': 'border mt-3',
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['NL Central', 'Last 10', 'Streak'],
        'body': [_t37, _t46, _t56, _t36, _t52]
    }, {
        'clazz': 'border mt-3',
        'cols': ['', 'text-center w-25', 'text-center w-25'],
        'head': ['NL West', 'Last 10', 'Streak'],
        'body': [_t39, _t53, _t45, _t31, _t55]
    }]
}