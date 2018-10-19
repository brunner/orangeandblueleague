#!/usr/bin/env python3
# -*- coding: utf-8 -*-\

import random
import re
from functools import partial


def _team(_1, _2, abbr, colors, chlany, cross, de, en, hn, pre, teamid):
    return {
        'abbreviation': abbr,
        'chlany': chlany,
        'colors': colors,
        'crosstown': cross,
        'decoding': de.format(_1, _2),
        'encoding': en,
        'hometown': hn.format(_1),
        'nickname': hn.format(_2),
        'precoding': pre.format(_1),
        'teamid': teamid,
    }


# yapf: disable
_all = [0, 1, 2, 3, 4, 5, 6]
_h31, _n31 = 'Arizona', 'Diamondbacks'
_c31 = (('#000000', '#ffffff', '#a71930', ''),
        ('#000000', '#acacac', '#e3d4ad', ''),
        ('#000000', '#ffffff', '#30ced8', '', ('home', [1, 4], 1.0)),
        ('#000000', '#acacac', '#30ced8', '', ('away', [1, 4], 1.0)),
        ('#000000', '#a71930', '#e3d4ad', '', ('home|away', [6], 1.0)))
_h32, _n32 = 'Atlanta', 'Braves'
_c32 = (('#ce1141', '#ffffff', '#13274f', ''),
        ('#ce1141', '#acacac', '#13274f', ''),
        ('#000000', '#f0f0dc', '#13274f', '', ('home', [6], 1.0)),
        ('#ffffff', '#13274f', '#13274f', '', ('away', _all, .5)))
_h33, _n33 = 'Baltimore', 'Orioles'
_c33 = (('#df4601', '#ffffff', '#000000', ''),
        ('#df4601', '#acacac', '#000000', ''),
        ('#df4601', '#000000', '#ffffff', '', ('home|away', [4], 1.0)),
        ('#000000', '#df4601', '#ffffff', '', ('home|away', [5], 1.0)))
_h34, _n34 = 'Boston', 'Red Sox'
_c34 = (('#bd3039', '#ffffff', '#0c2340', ''),
        ('#bd3039', '#acacac', '#0c2340', ''),
        ('#0c2340', '#bd3039', '#ffffff', '', ('home', [4], 1.0)),
        ('#bd3039', '#0c2340', '#ffffff', '', ('away', [4], 1.0)))
_h37, _n37 = 'Cincinnati', 'Reds'
_c37 = (('#c6011f', '#ffffff', '#000000', ''),
        ('#c6011f', '#acacac', '#ffffff', ''),
        ('#ffffff', '#c6011f', '#000000', '', ('home', _all, .35)))
_h38, _n38 = 'Cleveland', 'Indians'
_c38 = (('#e31937', '#ffffff', '#0c2340', ''),
        ('#0c2340', '#acacac', '#e31937', ''),
        ('#e31937', '#0c2340', '#ffffff', '', ('home|away', _all, .6)))
_h39, _n39 = 'Colorado', 'Rockies'
_c39 = (('#000000', '#ffffff', '#33006f', '#400d7c'),
        ('#33006f', '#acacac', '#ffffff', ''),
        ('#000000', '#33006f', '#c4ced4', '', ('home|away', _all, .35)),
        ('#c4ced4', '#000000', '#33006f', '', ('home|away', _all, .15)))
_h40, _n40 = 'Detroit', 'Tigers'
_c40 = (('#0c2340', '#ffffff', '#ffffff', ''),
        ('#0c2340', '#acacac', '#fa4616', ''))
_h41, _n41 = 'Miami', 'Marlins'
_c41 = (('#000000', '#ffffff', '#ff6600', ''),
        ('#000000', '#acacac', '#ff6600', ''),
        ('#ff6600', '#000000', '#ffffff', '', ('home|away', [4, 5], 1.0)))
_h42, _n42 = 'Houston', 'Astros'
_c42 = (('#002d62', '#ffffff', '#eb6e1f', ''),
        ('#002d62', '#acacac', '#eb6e1f', ''),
        ('#eb6e1f', '#002d62', '#ffffff', '', ('home', [6], .7)),
        ('#002d62', '#eb6e1f', '#ffffff', '', ('home|away', _all, .2)))
_h43, _n43 = 'Kansas City', 'Royals'
_c43 = (('#004687', '#ffffff', '#bd9B60', ''),
        ('#004687', '#acacac', '#ffffff', ''),
        ('#ffffff', '#71ade5', '#004687', '', ('home', [6], 1.0)),
        ('#ffffff', '#004687', '#71ade5', '', ('away', [6], 1.0)))
_h46, _n46 = 'Milwaukee', 'Brewers'
_c46 = (('#0a2351', '#ffffff', '#b6922e', ''),
        ('#0a2351', '#acacac', '#b6922e', ''),
        ('#0046ae', '#ffffff', '#ffd451', '#0d53bb', ('home', _all, .25)),
        ('#ffffff', '#0a2351', '#b6922e', '', ('home|away', _all, .5)))
_h47, _n47 = 'Minnesota', 'Twins'
_c47 = (('#052a44', '#ffffff', '#bc0e34', ''),
        ('#052a44', '#acacac', '#bc0e34', ''),
        ('#052a44', '#f0f0dc', '#bc0e34', '#123751', ('home', _all, 1.0)))
_h50, _n50 = 'Oakland', 'Athletics'
_c50 = (('#003831', '#ffffff', '#efb21e', ''),
        ('#003831', '#acacac', '#efb21e', ''),
        ('#ffffff', '#035a2e', '#efb21e', '', ('home', [4], 1.0)),
        ('#003831', '#fcb600', '#ffffff', '', ('home', _all, .1)),
        ('#ffffff', '#003831', '#efb21e', '', ('home|away', _all, .45)))
_h51, _n51 = 'Philadelphia', 'Phillies'
_c51 = (('#e81828', '#ffffff', '#ffffff', '#f52535'),
        ('#e81828', '#acacac', '#ffffff', ''),
        ('#6f263d', '#6bace4', '#ffffff', '', ('home', [3], 1.0)),
        ('#e81828', '#f0f0dc', '#284898', '', ('home', [6], 1.0)))
_h52, _n52 = 'Pittsburgh', 'Pirates'
_c52 = (('#27251f', '#ffffff', '#fdb827', ''),
        ('#27251f', '#acacac', '#fdb827', ''),
        ('#27251f', '#fdb827', '#ffffff', '', ('home', [6], 1.0)),
        ('#fdb827', '#27251f', '#ffffff', '', ('home|away', _all, .4)))
_h53, _n53 = 'San Diego', 'Padres'
_c53 = (('#002d62', '#ffffff', '#ffffff', ''),
        ('#002d62', '#acacac', '#acacac', ''),
        ('#ffc72c', '#473729', '#473729', '', ('home', [4], 1.0)),
        ('#ffffff', '#002d62', '#002d62', '', ('away', _all, .5)))
_h54, _n54 = 'Seattle', 'Mariners'
_c54 = (('#0c2c56', '#ffffff', '#005c5c', ''),
        ('#0c2c56', '#acacac', '#005c5c', ''),
        ('#c4ced4', '#005c5c', '#0c2c56', '', ('home', [4], 1.0)),
        ('#0c2c56', '#f0f0dc', '#005c5c', '', ('home', [6], 1.0)),
        ('#c4ced4', '#0c2c56', '#005c5c', '', ('away', _all, .45)))
_h55, _n55 = 'San Francisco', 'Giants'
_c55 = (('#27251f', '#ffffff', '#fd5a1e', ''),
        ('#27251f', '#acacac', '#fd5a1e', ''),
        ('#27251f', '#fd5a1e', '#ffffff', '', ('home', [4], 1.0)))
_h56, _n56 = 'St. Louis', 'Cardinals'
_c56 = (('#c41e3a', '#ffffff', '#0c2340', ''),
        ('#c41e3a', '#acacac', '#0c2340', ''),
        ('#c41e3a', '#f0f0dc', '#0c2340', '', ('home', [5], 1.0)))
_h57, _n57 = 'Tampa Bay', 'Rays'
_c57 = (('#092c5c', '#ffffff', '#8fbce6', ''),
        ('#092c5c', '#acacac', '#8fbce6', ''),
        ('#092c5c', '#8fbce6', '#ffffff', '', ('home', [6], 1.0)),
        ('#8fbce6', '#092c5c', '#ffffff', '', ('', _all, .25)))
_h58, _n58 = 'Texas', 'Rangers'
_c58 = (('#003278', '#ffffff', '#c0111f', ''),
        ('#003278', '#acacac', '#c0111f', ''),
        ('#c0111f', '#ffffff', '#003278', '', ('home', _all, .25)),
        ('#ffffff', '#003278', '#c0111f', '', ('home|away', _all, .5)))
_h59, _n59 = 'Toronto', 'Blue Jays'
_c59 = (('#134a8e', '#ffffff', '#ffffff', ''),
        ('#134a8e', '#acacac', '#acacac', ''),
        ('#ffffff', '#134a8e', '#134a8e', '', ('home|away', _all, .5)))
_h60, _n60 = 'Washington', 'Nationals'
_c60 = (('#ab0003', '#ffffff', '#14225a', ''),
        ('#ab0003', '#acacac', '#14225a', ''),
        ('#', '#', '#', '', ('home', [1, 4], 1.0)),
        ('#', '#', '#', '', ('home|away', [5, 6], .5)))
_hch, _n35, _n36 = 'Chicago', 'White Sox', 'Cubs'
_c35 = (('#27251f', '#ffffff', '#c4ced4', '#34322c'),
        ('#27251f', '#acacac', '#ffffff', ''),
        ('#002663', '#ffffff', '#cc092f', '', ('home', [6], 1.0)),
        ('#ffffff', '#27251f', '#c4ced4', '', ('home|away', _all, .6)))
_c36 = (('#0e3386', '#ffffff', '#cc3433', '#1b4093'),
        ('#cc3433', '#acacac', '#0e3386', ''),
        ('#cc3433', '#0e3386', '#ffffff', '', ('away', _all, .4)))
_hla, _n44, _n45 = 'Los Angeles', 'Angels', 'Dodgers'
_c44 = (('#ba0021', '#ffffff', '#003263', ''),
        ('#ba0021', '#acacac', '#003263', ''),
        ('#c4ced4', '#ba0021', '#003263', '', ('', _all, .55)))
_c45 = (('#005a9c', '#ffffff', '#ef3e42', ''),
        ('#005a9c', '#acacac', '#ef3e42', ''))
_hny, _n48, _n49 = 'New York', 'Yankees', 'Mets'
_c48 = (('#0c2340', '#ffffff', '#ffffff', '#19304d'),
        ('#0c2340', '#acacac', '#acacac', ''))
_c49 = (('#002d72', '#ffffff', '#ff5910', '#0d3a7f'),
        ('#002d72', '#acacac', '#ff5910', ''),
        ('#ff5910', '#002d72', '#ffffff', '', ('home', _all, .15)),
        ('#aabec8', '#002d72', '#ff5910', '', ('away', _all, .2)))
# yapf: enable

_teams = [
    _team(_h31, _n31, 'ARI', _c31, '', '', '{} {}', 'T31', '{}', '{}', '31'),
    _team(_h32, _n32, 'ATL', _c32, '', '', '{} {}', 'T32', '{}', '{}', '32'),
    _team(_h33, _n33, 'BAL', _c33, '', '', '{} {}', 'T33', '{}', '{}', '33'),
    _team(_h34, _n34, 'BOS', _c34, '', '', '{} {}', 'T34', '{}', '{}', '34'),
    _team(_hch, _n35, 'CWS', _c35, 'TCH', 'T36', '{} {}', 'T35', '{}', '',
          '35'),
    _team(_hch, _n36, 'CHC', _c36, 'TCH', 'T35', '{} {}', 'T36', '{}', '',
          '36'),
    _team(_h37, _n37, 'CIN', _c37, '', '', '{} {}', 'T37', '{}', '{}', '37'),
    _team(_h38, _n38, 'CLE', _c38, '', '', '{} {}', 'T38', '{}', '{}', '38'),
    _team(_h39, _n39, 'COL', _c39, '', '', '{} {}', 'T39', '{}', '{}', '39'),
    _team(_h40, _n40, 'DET', _c40, '', '', '{} {}', 'T40', '{}', '{}', '40'),
    _team(_h41, _n41, 'MIA', _c41, '', '', '{} {}', 'T41', '{}', '{}', '41'),
    _team(_h42, _n42, 'HOU', _c42, '', '', '{} {}', 'T42', '{}', '{}', '42'),
    _team(_h43, _n43, 'KC', _c43, '', '', '{} {}', 'T43', '{}', '{}', '43'),
    _team(_hla, _n44, 'LAA', _c44, 'TLA', 'T45', '{} {}', 'T44', '{}', '',
          '44'),
    _team(_hla, _n45, 'LAD', _c45, 'TLA', 'T44', '{} {}', 'T45', '{}', '',
          '45'),
    _team(_h46, _n46, 'MIL', _c46, '', '', '{} {}', 'T46', '{}', '{}', '46'),
    _team(_h47, _n47, 'MIN', _c47, '', '', '{} {}', 'T47', '{}', '{}', '47'),
    _team(_hny, _n48, 'NYY', _c48, 'TNY', 'T49', '{} {}', 'T48', '{}', '',
          '48'),
    _team(_hny, _n49, 'NYM', _c49, 'TNY', 'T48', '{} {}', 'T49', '{}', '',
          '49'),
    _team(_h50, _n50, 'OAK', _c50, '', '', '{} {}', 'T50', '{}', '{}', '50'),
    _team(_h51, _n51, 'PHI', _c51, '', '', '{} {}', 'T51', '{}', '{}', '51'),
    _team(_h52, _n52, 'PIT', _c52, '', '', '{} {}', 'T52', '{}', '{}', '52'),
    _team(_h53, _n53, 'SD', _c53, '', '', '{} {}', 'T53', '{}', '{}', '53'),
    _team(_h54, _n54, 'SEA', _c54, '', '', '{} {}', 'T54', '{}', '{}', '54'),
    _team(_h55, _n55, 'SF', _c55, '', '', '{} {}', 'T55', '{}', '{}', '55'),
    _team(_h56, _n56, 'STL', _c56, '', '', '{} {}', 'T56', '{}', '{}', '56'),
    _team(_h57, _n57, 'TB', _c57, '', '', '{} {}', 'T57', '{}', '{}', '57'),
    _team(_h58, _n58, 'TEX', _c58, '', '', '{} {}', 'T58', '{}', '{}', '58'),
    _team(_h59, _n59, 'TOR', _c59, '', '', '{} {}', 'T59', '{}', '{}', '59'),
    _team(_h60, _n60, 'WAS', _c60, '', '', '{} {}', 'T60', '{}', '{}', '60'),
    _team(_hch, '', '', '', '', '', '{}', 'TCH', '', '{}', ''),
    _team(_hla, '', '', '', '', '', '{}', 'TLA', '', '{}', ''),
    _team(_hny, '', '', '', '', '', '{}', 'TNY', '', '{}', ''),
]


def _map(k, vs):
    return {t[k]: {v: t[v] for v in vs if t[v]} for t in _teams if t[k]}


def _repl(f, m):
    a = m.group(0)
    b = f(a)
    return b if b else a


def _sub(ks, f, s):
    pattern = '|'.join(ks)
    return re.sub(pattern, partial(_repl, f), s)


_decodings = _map('decoding', ['encoding', 'nickname'])
_encodings = _map('encoding', [
    'abbreviation', 'chlany', 'colors', 'crosstown', 'decoding', 'nickname',
    'precoding', 'teamid'
])
_precodings = _map('precoding', ['encoding'])
_teamids = _map(
    'teamid', ['abbreviation', 'decoding', 'encoding', 'hometown', 'nickname'])
_img = '<img src="https://orangeandblueleaguebaseball.com/StatsLab/' + \
       'reports/news/html/images/team_logos/{0}_40.png" width="20" ' + \
       'height="20" border="0" class="{1}">'
_span = '<span class="align-middle {0}">{1}</span>'
_absolute_img = _img.format('{0}', 'position-absolute {1}-8p top-14p')
_absolute_span = _span.format('d-block text-truncate p{0}-24p', '{1}')
_inline_img = _img.format('{0}', 'd-inline-block')
_inline_span = _span.format('d-inline-block px-2', '{0}')


def choose_colors(colors, day, where):
    for alt in colors[2:]:
        regex, days, pct = alt[-1]
        if re.search(regex, where) and day in days and pct >= random.random():
            return alt[:4]
    if re.search('home', where):
        return colors[0]
    return colors[1]


def chlany():
    return ['TCH', 'TLA', 'TNY']


def decoding_to_encoding(decoding):
    return _decodings.get(decoding, {}).get('encoding', '')


def decoding_to_nickname(decoding):
    return _decodings.get(decoding, {}).get('nickname', '')


def decoding_to_encoding_sub(text):
    return _sub(_decodings_keys, decoding_to_encoding, text)


def decodings():
    return _decodings_keys


def divisions():
    return [
        ('AL East', ('33', '34', '48', '57', '59')),
        ('AL Central', ('35', '38', '40', '43', '47')),
        ('AL West', ('42', '44', '50', '54', '58')),
        ('NL East', ('32', '41', '49', '51', '60')),
        ('NL Central', ('36', '37', '46', '52', '56')),
        ('NL West', ('31', '39', '45', '53', '55')),
    ]


def encoding_to_abbreviation(encoding):
    return _encodings.get(encoding, {}).get('abbreviation', '')


def encoding_to_chlany(encoding):
    return _encodings.get(encoding, {}).get('chlany', '')


def encoding_to_colors(encoding):
    return _encodings.get(encoding, {}).get('colors', '')


def encoding_to_crosstown(encoding):
    return _encodings.get(encoding, {}).get('crosstown', '')


def encoding_to_decoding(encoding):
    return _encodings.get(encoding, {}).get('decoding', '')


def encoding_to_decoding_sub(text):
    return _sub(_encodings_keys, encoding_to_decoding, text)


def encoding_to_nickname(encoding):
    return _encodings.get(encoding, {}).get('nickname', '')


def encoding_to_precoding(encoding):
    return _encodings.get(encoding, {}).get('precoding', '')


def encoding_to_teamid(encoding):
    return _encodings.get(encoding, {}).get('teamid', '')


def encodings():
    return _encodings_keys


def precoding_to_encoding(precoding):
    return _precodings.get(precoding, {}).get('encoding', '')


def precoding_to_encoding_sub(text):
    return _sub(_precodings_keys, precoding_to_encoding, text)


def precodings():
    return _precodings_keys


def logo_absolute(teamid, text, side):
    decoding = teamid_to_decoding(teamid)
    fname = decoding.replace('.', '').replace(' ', '_').lower()
    img = _absolute_img.format(fname, side)
    span = _absolute_span.format(side[0], text)
    return img + span


def logo_inline(teamid, text):
    decoding = teamid_to_decoding(teamid)
    fname = decoding.replace('.', '').replace(' ', '_').lower()
    img = _inline_img.format(fname)
    span = _inline_span.format(text)
    return img + span


def teamid_to_abbreviation(teamid):
    return _teamids.get(teamid, {}).get('abbreviation', '')


def teamid_to_decoding(teamid):
    return _teamids.get(teamid, {}).get('decoding', '')


def teamid_to_encoding(teamid):
    return _teamids.get(teamid, {}).get('encoding', '')


def teamid_to_hometown(teamid):
    return _teamids.get(teamid, {}).get('hometown', '')


def teamid_to_nickname(teamid):
    return _teamids.get(teamid, {}).get('nickname', '')


def teamids():
    return _teamids_keys


_decodings_keys = list(sorted(_decodings.keys(), key=decoding_to_encoding))
_encodings_keys = list(sorted(_encodings.keys()))
_precodings_keys = list(sorted(_precodings.keys(), key=precoding_to_encoding))
_teamids_keys = list(sorted(_teamids.keys()))
