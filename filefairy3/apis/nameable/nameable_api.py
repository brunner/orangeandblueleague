#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc


class NameableApi(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(NameableApi, self).__init__()

    @abc.abstractmethod
    def _name(self):
        pass
