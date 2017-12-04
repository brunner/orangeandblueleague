#!/usr/bin/env python

import copy
import json
import os
import re
import threading
import time
import urllib2
import websocket

from slack_api import chat_post_message, files_upload, rtm_connect
from teams import get_city, get_emoji, get_nickname


class App(object):

  def __init__(self):
    self.file_url = 'https://orangeandblueleaguebaseball.com/StatsLab/exports.php'
    self.standings_in = 'data/standings.txt'

  def setup(self):
    self.file_date = self.get_file_date(self.get_page(self.file_url))
    self.finalScores = []
    self.injuries = []
    self.liveTables = []
    self.lock = threading.Lock()
    self.tick = 0
    self.records = {t: {'w': 0, 'l': 0} for t in range(31, 61)}
    self.standings = self.read_standings(self.get_standings_in())
    self.ws = None

  def get_path(self):
    return os.path.expanduser('~') + '/orangeandblueleague/filefairy/'

  def get_standings_in(self):
    s_i = self.standings_in
    if os.path.isfile(self.get_path() + 'data/standings_over.txt'):
      s_i = 'data/standings_over.txt'
    return self.get_path() + s_i if s_i else ''

  def get_standings_out(self):
    return self.get_path() + 'data/standings.txt'

  def get_general_name(self):
    return 'general'

  def get_live_sim_discussion_name(self):
    return 'live-sim-discussion'

  def get_testing_name(self):
    return 'testing'

  def get_statsplus_id(self):
    return 'C7JSGHW8G'

  def get_timer_values(self):
    return [120, 82800]

  def get_page(self, url):
    try:
      return urllib2.urlopen(url).read()
    except:
      return ''

  def read_standings(self, standings_in):
    """Read standings data from file.

    Args:
        standings_in: the file to read the standings data from.
    Returns:
        a mapping of team ids to season win/loss pairs.

    """
    s = {t: {'w': 0, 'l': 0} for t in range(31, 61)}
    if os.path.isfile(standings_in):
      with open(standings_in, 'r') as f:
        for line in f.readlines():
          t, w, l = [int(n) for n in line.split()]
          s[t]['w'], s[t]['l'] = w, l
    return s

  def write_standings(self, standings_out, s):
    """Write standings data to file.

    Args:
        standings_out: the file to write the standings data to.
        s: the copy of the standings data.
    Returns:
        None

    """
    lines = ['{} {} {}\n'.format(t, s[t]['w'], s[t]['l']) for t in s]
    if os.path.isfile(standings_out):
      with open(standings_out, 'w') as f:
        f.writelines(lines)

  def listen(self):
    def on_message_(ws, message):
      self.lock.acquire()
      obj = json.loads(message)
      if all(k in obj for k in ['type', 'channel', 'text']):
        if obj['type'] == 'message' and obj['channel'] == self.get_statsplus_id():
          self.handle_statsplus(obj['text'])
      self.lock.release()

    obj = rtm_connect()
    if obj['ok'] and 'url' in obj:
      chat_post_message('testing', 'Started listening.')
      self.ws = websocket.WebSocketApp(obj['url'], on_message=on_message_)

      t = threading.Thread(target=self.ws.run_forever)
      t.daemon = True
      t.start()

  def handle_statsplus(self, text):
    if 'MAJOR LEAGUE BASEBALL Final Scores' in text:
      self.handle_final_scores(text)
    elif 'MAJOR LEAGUE BASEBALL Live Table' in text:
      self.handle_live_table(text)
    elif re.findall(r'\d{2}\/\d{2}\/\d{4}', text) and 'was injured' in text:
      self.handle_injuries(text)

  def handle_final_scores(self, text):
    text = re.sub(r'( MAJOR LEAGUE BASEBALL Final Scores|\*)', '', text)
    if text not in self.finalScores:
      self.finalScores.append(text)
      self.liveTables.append('')
      self.tick = int(time.time())

  def process_final_scores(self):
    for i, finalScore in enumerate(self.finalScores):
      chat_post_message(self.get_live_sim_discussion_name(), finalScore)
      if len(self.finalScores) == len(self.liveTables):
        liveTable = self.liveTables[i]
        for t in range(31, 61):
          if t in [35, 36, 44, 45, 48, 49]:
            continue
          city = get_city(t)
          cw = len(re.findall(r'\|' + re.escape(city), finalScore))
          cl = len(re.findall(r', ' + re.escape(city), finalScore))
          self.add_score(t, cw, cl)

        for t, u in zip([35, 44, 48], [36, 45, 49]):
          city = get_city(t)
          cw = len(re.findall(r'\|' + re.escape(city), finalScore))
          cl = len(re.findall(r', ' + re.escape(city), finalScore))

          ws = re.findall(r'\|' + re.escape(city) + '\s\d+,\s([^\d]+)\d', finalScore)
          ls = re.findall(r'\|([^\d]+)\d+,\s' + re.escape(city), finalScore)

          tn = get_nickname(t)
          tt = re.findall(re.escape(tn) + r'\s+(\d+)', liveTable)
          ts = self.get_score(t, 'w')

          un = get_nickname(u)
          ut = re.findall(re.escape(un) + r'\s+(\d+)', liveTable)
          us = self.get_score(u, 'w')

          if tt and ut:
            ct = cw + cl
            tw, uw = int(tt[0]) - ts, int(ut[0]) - us
            if ct != 3:
              tl, ul = ct / 2 - tw, ct / 2 - uw
              self.add_score(t, tw, tl)
              self.add_score(u, uw, ul)
            else:
              tl, ul = 0 if tw else 1, 0 if uw else 1
              self.add_score(t, tw, tl)
              self.add_score(u, uw, ul)
            if tw == uw or cw == 1 and cl == 2:
              _ = list(set().union(ws, ls))
              tk, uk = _ if len(_) == 2 else ('', '')
              if ct != 3:
                self.add_schedule(t, {tk: False, uk: False})
                self.add_schedule(u, {tk: False, uk: False})
              else:
                td = ws.count(tk) + ls.count(tk) == 2
                ud = ws.count(uk) + ls.count(uk) == 2
                self.add_schedule(t, {tk: td, uk: ud})
                self.add_schedule(u, {tk: td, uk: ud})
            else:
              tk, uk = '', ''
              for k in ws:
                tk = k if ws.count(k) == tw and not tk else tk
                uk = k if ws.count(k) == uw and not uk else uk
              for k in ls:
                tk = k if ls.count(k) == tl and not tk else tk
                uk = k if ls.count(k) == ul and not uk else uk
              self.add_schedule(t, {tk: False})
              self.add_schedule(u, {uk: False})
          else:
            _ = list(set().union(ws, ls))
            sk = _[0] if len(_) == 1 else ''
            if tt:
              self.add_score(t, cw, cl)
              self.add_schedule(t, {sk: False})
              self.add_schedule(u, {'': False})
            if ut:
              self.add_score(u, cw, cl)
              self.add_schedule(t, {'': False})
              self.add_schedule(u, {sk: False})

    for t, u in zip([35, 44, 48], [36, 45, 49]):
      if 'scs' not in self.records[t]:
        continue
      tscs, uscs = self.records[t]['scs'], self.records[u]['scs']
      if len(tscs) < 2:
        continue
      for i in range(len(tscs)):
        if len(tscs[i].keys()) == 2:
          vk, wk = tscs[i].keys()
          tvn, uvn, twn, uwn = 0, 0, 0, 0
          for j in tscs[i-1::-1]:
            if vk not in j and wk not in j:
              break
            if vk in j:
              tvn += 1
            if wk in j:
              twn += 1
          for j in uscs[i-1::-1]:
            if vk not in j and wk not in j:
              break
            if vk in j:
              uvn += 1
            if wk in j:
              uwn += 1
          for j in tscs[i+1:]:
            if vk not in j and wk not in j:
              break
            if vk in j:
              tvn += 1
            if wk in j:
              twn += 1
          for j in uscs[i+1:]:
            if vk not in j and wk not in j:
              break
            if vk in j:
              uvn += 1
            if wk in j:
              uwn += 1
          if tvn > twn:
            if tscs[i][vk]:
              self.add_score(t, 0, 1)
              tscs[i][vk] = False
              uscs[i][vk] = False
            elif uscs[i][wk]:
              self.add_score(u, 0, 1)
              tscs[i][wk] = False
              uscs[i][wk] = False
          elif twn > tvn:
            if tscs[i][wk]:
              self.add_score(t, 0, 1)
              tscs[i][wk] = False
              uscs[i][wk] = False
            elif uscs[i][vk]:
              self.add_score(u, 0, 1)
              tscs[i][vk] = False
              uscs[i][vk] = False
          elif uvn > uwn:
            if uscs[i][vk]:
              self.add_score(u, 0, 1)
              tscs[i][vk] = False
              uscs[i][vk] = False
            elif tscs[i][wk]:
              self.add_score(t, 0, 1)
              tscs[i][wk] = False
              uscs[i][wk] = False
          elif uwn > uvn:
            if uscs[i][wk]:
              self.add_score(u, 0, 1)
              tscs[i][wk] = False
              uscs[i][wk] = False
            elif tscs[i][vk]:
              self.add_score(t, 0, 1)
              tscs[i][vk] = False
              uscs[i][vk] = False

    ret = '\n'.join(self.finalScores)
    self.finalScores, self.liveTables = [], []
    return ret

  def add_score(self, t, w, l):
    self.records[t]['w'] += w
    self.records[t]['l'] += l

    self.standings[t]['w'] += w
    self.standings[t]['l'] += l

  def get_score(self, t, key):
    return self.standings[t][key]

  def add_schedule(self, t, sc):
    self.records[t].setdefault('scs', []).append(sc)

  def handle_live_table(self, text):
    i = len(self.liveTables) - 1
    self.liveTables[i] = text
    self.tick = int(time.time())

  def handle_injuries(self, text):
    if text not in self.injuries:
      self.injuries.append(text)
      self.tick = int(time.time())

  def process_injuries(self):
    lines = []
    if self.injuries:
      lines.append('Injuries:')
      for injury in self.injuries:
        for chunk in injury.split('. '):
          match = re.findall(r'(\<[^\(]+)\(', chunk)
          if match:
            line = re.sub(r'was injured (?:(?:in a|on a|while) )?',
                          '(', match[0].strip())
            if not line == match[0]:
              line += ')'
            lines.append(line)

      self.injuries = []

    ret = '\n'.join(lines)
    if ret:
      chat_post_message(self.get_live_sim_discussion_name(), ret)

    return ret

  def process_records(self):
    ret = self.format_records()
    chat_post_message(self.get_live_sim_discussion_name(), ret)
    return ret

  def process_standings(self):
    retA = self.format_standings_al()
    retB = self.format_standings_nl()
    files_upload(retA, 'AL.txt', self.get_live_sim_discussion_name())
    files_upload(retB, 'NL.txt', self.get_live_sim_discussion_name())
    self.write_standings(self.get_standings_out(), self.standings)
    return '\n'.join([retA, retB])

  def handle_close(self):
    self.lock.acquire()
    if self.ws:
      self.ws.close()
      chat_post_message('testing', 'Done listening.')
    self.lock.release()

  def watch(self):
    sleep, timeout = self.get_timer_values()
    elapsed = 0
    chat_post_message('testing', 'Started watching.')

    while elapsed < timeout:
      time.sleep(sleep)
      elapsed = elapsed + sleep

      if self.update_league_file():
        elapsed = timeout

      self.lock.acquire()
      if self.finalScores and int(time.time()) - self.tick > sleep:
        self.process_final_scores()
        self.process_injuries()
        self.process_records()
        self.process_standings()
      self.lock.release()

    chat_post_message('testing', 'Done watching.')
    self.handle_close()

  def update_league_file(self):
    date = self.get_file_date(self.get_page(self.file_url))
    if date and date != self.file_date:
      chat_post_message(self.get_general_name(), 'File is up.')
      self.file_date = date
      return True
    return False

  def get_file_date(self, page):
    match = re.findall(r'League File Updated: ([^<]+)<', page)
    return match[0] if len(match) else ''

  def format_records(self):
    groups = [
        ('AL East', [33, 34, 48, 57, 59]),
        ('AL Central', [35, 38, 40, 43, 47]),
        ('AL West', [42, 44, 50, 54, 58]),
        ('NL East', [32, 41, 49, 51, 60]),
        ('NL Central', [36, 37, 46, 52, 56]),
        ('NL West', [31, 39, 45, 53, 55]),
    ]
    lines = []
    for group in groups:
      r = self.records
      ordered = self.get_ordered(r, group[1])
      formatted = []
      for t in ordered:
        if r[t]['w'] + r[t]['l'] > 0:
          emoji = get_emoji(t)
          formatted.append('{0} {1}-{2}'.format(emoji, r[t]['w'], r[t]['l']))
      if formatted:
        lines.append('{0}\n{1}'.format(group[0], ' :separator: '.join(formatted)))

    unhandled = []
    for t in [35, 44, 48]:
      if 'scs' not in self.records[t]:
        continue
      city = get_city(t)
      tscs = self.records[t]['scs']
      for sc in tscs:
        for tk in sc:
          if sc[tk]:
            unhandled.append('Unhandled loss for {}.'.format(city))
    if unhandled:
      lines.append('_{}_'.format(' '.join(unhandled)))

    return '\n\n'.join(lines)

  def get_standings_keys(self, k):
    return [k + ey for ey in ['gb', 'en', 'mn']]

  def get_games_behind(self, s, u, t0):
    """Return the number of games that u is behind t.

    Args:
        s: the copy of the standings data.
        u: the trailing team.
        t0: the leading team.
    Returns:
        the number of games that u is behind t.

    """
    return (s[t0]['w'] - s[u]['w'] + s[u]['l'] - s[t0]['l']) / 2.0

  def get_elimination_number(self, s, u, t):
    """Return the elimination number for a team.

    Args:
        s: the copy of the standings data.
        u: the trailing team.
        t0: the leading team.
    Returns:
        the elimination number for u.

    """
    return max(163 - s[t]['w'] - s[u]['l'], 0)

  def get_ordered(self, s, group):
    """Return a set of teams, sorted by winning percentage.

    Args:
        s: the copy of the standings data.
        group: the set of team ids to sort.
    Returns:
        the sorted group.

    """
    pct = lambda t: (float(s[t]['w']) / ((s[t]['w'] + s[t]['l']) or 1),
                     s[t]['w'],
                     float(1) / s[t]['l'] if s[t]['l'] else 2,
                     float(1) / t)
    return sorted(group, key=pct, reverse=True)

  def process_elimination_numbers(self, s, ordered, i, k):
    """Annotates the standings with elimination number data.

    Args:
        s: the copy of the standings data.
        ordered: the ordered set of team ids to annotate (e.g. a division).
        i: the index of the team occupying the final playoff spot in ordered.
        k: the key prefix to use when setting annotations ('d' for division, 'w' for wild card).

    """
    kgb, ken, kmn = self.get_standings_keys(k)
    ts = filter(lambda v: s[v][kgb] <= 0, ordered)
    if len(ts) == len(ordered):
      for t in ordered:
        u0 = sorted(filter(lambda v: v != t, ts), key=lambda v: s[v]['l'], reverse=True)[0]
        en = self.get_elimination_number(s, u0, t)
        if kmn not in s[t] or en > s[t][kmn]:
          s[t][kmn] = en
    else:
      for t in ts:
        for u in ordered:
          if u == t or (u not in ts and 'dgb0' in s[u]):
            continue
          en = self.get_elimination_number(s, u, t)
          s[u].setdefault(ken, []).append(en)
          s[t].setdefault(kmn, []).append(en)
      for v in ordered:
        if kmn in s[v]:
          s[v][kmn] = sorted(s[v][kmn], reverse=True)[i]
        elif ken in s[v]:
          s[v][ken] = sorted(s[v][ken])[i]
        if kmn in s[v] and ken in s[v]:
          del s[v][ken]

  def get_standings_output(self, s, kgroup, group, k):
    """Populates a standings template with data for a set of teams.

    Args:
        s: the copy of the standings data.
        kgroup: the title of the group (e.g. 'AL East')
        group: the set of team ids in the group.
        k: the key prefix to use when getting annotations ('d' for division, 'w' for wild card).
    Returns:
        the populated standings template.

    """
    kgb, ken, kmn = self.get_standings_keys(k)
    div = ' | '
    top = '{title:<15}{div}  W{div}  L{div}   GB{div} M#\n' + \
          '----------------|-----|-----|-------|-----'
    row = '{city:<15}{div}{w:>3}{div}{l:>3}{div}{gb:>5}{div}{mn:>3}'

    lines = [top.format(title=kgroup, div=div)]
    for v in self.get_ordered(s, group):
      city = get_city(v)
      if 'p' in s[v]:
        city = s[v]['p'] + city
      w, l, dgb = s[v]['w'], s[v]['l'], s[v][kgb]
      gb = '{:0.1f}'.format(dgb) if dgb > 0 else '+{:0.1f}'.format(abs(dgb)) if dgb < 0 else '-'
      mn = '' if kmn not in s[v] else s[v][kmn] if s[v][kmn] > 0 else 'X'
      en = '' if ken not in s[v] else s[v][ken]
      lines.append(row.format(city=city, div=div, w=w, l=l, gb=gb, mn=mn))

    return '\n'.join(lines)

  def format_standings_internal(self, east, cent, west, k):
    """Return a string representation of the standings for a league.

    Args:
        east: the set of team ids in the east division.
        cent: the set of team ids in the central division.
        west: the set of team ids in the west division.
        kgroup: the title of the group (e.g. 'AL East').
        k: the league title prefix (e.g. 'AL').
    Returns:
        the string representation of the standings.

    """
    s = copy.deepcopy(self.standings)
    keast, kcent, kwest, kwc = [k + ' ' + ey for ey in ['East', 'Central', 'West', 'Wild Card']]

    # Set the games behind and elimination numbers for each division.
    # If a team is the only leader in its division, annotate it with 'dbg0'.
    for group in [east, cent, west]:
      ordered = self.get_ordered(s, group)
      t0, s[t0]['dgb'], s[t0]['dgb0'] = ordered[0], 0.0, 1
      for u in ordered[1:]:
        gb = self.get_games_behind(s, u, t0)
        s[u]['dgb'] = gb
        if gb == 0.0 and 'dgb0' in s[t0]:
          del s[t0]['dgb0']
      self.process_elimination_numbers(s, ordered, 0, 'd')

    # Filter division leaders out of the set of wild card teams.
    lg = east + cent + west
    wc = filter(lambda v: 'dgb0' not in s[v], lg)

    # Find the index of the team occupying the final playoff spot in the league.
    ordered = self.get_ordered(s, lg)
    k, j = 0, 2
    for i, t0 in enumerate(ordered):
      if 'dgb0' not in s[t0]:
        k += 1
        if s[t0]['dgb'] == 0:
          j = 3
      if k == j:
        break

    # Set the games behind and elimination numbers for the wild card.
    s[t0]['wgb'] = 0.0
    for v in ordered:
      s[v]['wgb'] = self.get_games_behind(s, v, t0)
    self.process_elimination_numbers(s, ordered, i, 'w')

    # Annotate the standings with team prefixes, if applicable.
    for v in ordered:
      if s[v].get('den', 1) == 0 and s[v].get('wen', 1) == 0:
        # v has been eliminated.
        s[v]['p'] = 'e-'
      if s[v].get('dmn', 1) == 0:
        # v has clinched the division.
        s[v]['p'] = 'x-'
      elif s[v].get('wmn', 1) == 0:
        if 'dgb0' in s[v]:
          # v has clinched a playoff berth.
          s[v]['p'] = 'y-'
        else:
          # v has clinched the wild card.
          s[v]['p'] = 'z-'

    # Feed the annotated standings data into a helper method to populate the standings template.
    groups = zip([keast, kcent, kwest, kwc], [east, cent, west, wc], ['d', 'd', 'd', 'w'])
    ret = [self.get_standings_output(s, kgroup, group, k) for (kgroup, group, k) in groups]
    return '\n\n'.join(ret)

  def format_standings_al(self):
    aleast, alcent, alwest = [33, 34, 48, 57, 59], [35, 38, 40, 43, 47], [42, 44, 50, 54, 58]
    return self.format_standings_internal(aleast, alcent, alwest, 'AL')

  def format_standings_nl(self):
    nleast, nlcent, nlwest = [32, 41, 49, 51, 60], [36, 37, 46, 52, 56], [31, 39, 45, 53, 55]
    return self.format_standings_internal(nleast, nlcent, nlwest, 'NL')


if __name__ == '__main__':
  app = App()
  app.setup()
  app.listen()
  app.watch()
