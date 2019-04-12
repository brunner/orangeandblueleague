#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for storing gameday player information."""

import os
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/tables', '', _path))

from common.elements.elements import cell  # noqa
from common.elements.elements import col  # noqa
from common.elements.elements import table  # noqa
from common.elements.elements import tbody  # noqa


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

    def create_table(self, roster, state):
        bcols = [col(), col(clazz='w-50p text-right')]
        body, self.body = list(self.body), []
        self.body.append(roster.create_player_row(False))
        self.body.append(roster.create_player_row(True))
        self.table = table(clazz='border mb-3', bcols=bcols, body=body)

        self.tables.append(state.create_head_table())
        self.tables.append(self.table)

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


def create_tables():
    return Tables()