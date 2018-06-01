#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import importlib
import logging
import os
import re
import sys
import threading
import time
import traceback
import websocket

_path = os.path.dirname(os.path.abspath(__file__))
_root = re.sub(r'/core/fairylab', '', _path)
sys.path.append(_root)

from api.messageable.messageable import Messageable  # noqa
from api.nameable.nameable import Nameable  # noqa
from api.plugin.plugin import Plugin  # noqa
from api.registrable.registrable import Registrable  # noqa
from api.renderable.renderable import Renderable  # noqa
from core.dashboard.dashboard import Dashboard  # noqa
from core.dashboard.dashboard import LoggingHandler  # noqa
from core.notify.notify import Notify  # noqa
from util.ago.ago import delta  # noqa
from util.component.component import card  # noqa
from util.jinja2_.jinja2_ import env  # noqa
from util.logger.logger import log  # noqa
from util.slack.slack import rtm_connect  # noqa


class Fairylab(Messageable, Renderable):
    def __init__(self, **kwargs):
        d = kwargs.pop('d')
        super(Fairylab, self).__init__(**kwargs)

        self.bg = None
        self.day = None
        self.keep_running = True
        self.lock = threading.Lock()
        self.registered = {'dashboard': d}
        self.sleep = 120
        self.tasks = []
        self.ws = None

    @staticmethod
    def _data():
        return os.path.join(_path, 'data.json')

    @staticmethod
    def _href():
        return '/fairylab/'

    @staticmethod
    def _title():
        return 'home'

    @staticmethod
    def _info():
        return 'Fairylab core framework.'

    def _setup(self, date):
        kwargs = {'date': date, 'v': True}
        self.day = date.day

        d = os.path.join(_root, 'plugin')
        ps = filter(lambda x: self._is_plugin_dir(d, x), os.listdir(d))
        for p in sorted(ps):
            self._reload_internal('plugin', p, **kwargs)

        self._try_all('_setup', **kwargs)
        log(self._name(), **dict(kwargs, s='Completed setup.'))

    def _on_message_internal(self, **kwargs):
        pass

    def _render_internal(self, **kwargs):
        _home = self._home(**kwargs)
        return [('html/fairylab/index.html', '', 'home.html', _home)]

    @staticmethod
    def _is_plugin_dir(d, x):
        return os.path.isdir(os.path.join(d, x)) and x != '__pycache__'

    @staticmethod
    def _package(path, name):
        return '{0}.{1}.{1}'.format(path, name)

    def _try_all(self, method, *args, **kwargs):
        ps = sorted(self.registered.keys())
        for p in ps:
            self._try(p, method, *args, **kwargs)

    def _try(self, p, method, *args, **kwargs):
        if p not in self.registered:
            return

        instance = self.registered.get(p)
        if not isinstance(instance, Plugin) or not instance.ok:
            return

        item = getattr(instance, method, None)
        if not item or not callable(item):
            return

        date = kwargs.get('date') or datetime.datetime.now()

        try:
            response = item(*args, **dict(kwargs, date=date))
            if response.notify:
                self.registered[p].date = date
            for n in response.notify:
                if n != Notify.BASE:
                    self._try_all('_notify', **dict(kwargs, notify=n))
            for shadow in response.shadow:
                s = shadow.destination
                self._try(s, '_shadow', **dict(kwargs, shadow=shadow))
            for t in response.task:
                self.tasks.append((p, t))
        except Exception:
            exc = traceback.format_exc()
            log(instance._name(), s='Exception.', c=exc, v=True)
            self.registered[p].date = date
            self.registered[p].ok = False

    def _background(self):
        while self.keep_running:
            original = list(self.tasks)
            self.tasks = []

            for p, task in original:
                self._try(p, task.target, *task.args, **task.kwargs)

            if not self.tasks:
                time.sleep(self.sleep)

    def _recv(self, message):
        with self.lock:
            date = datetime.datetime.now()
            obj = json.loads(message)
            self._on_message(obj=obj, date=date)
            self._try_all('_on_message', obj=obj, date=date)

    def _connect(self):
        def _recv(ws, message):
            self._recv(message)

        obj = rtm_connect()
        if obj['ok'] and 'url' in obj:
            self.ws = websocket.WebSocketApp(obj['url'], on_message=_recv)
            t = threading.Thread(target=self.ws.run_forever)
            t.daemon = True
            t.start()

    def _start(self):
        while self.keep_running:
            if not self.bg:
                self.bg = threading.Thread(target=self._background)
                self.bg.daemon = True
                self.bg.start()

            if not self.ws or not self.ws.sock:
                if self.ws:
                    self.ws.close()
                self._connect()

            with self.lock:
                date = datetime.datetime.now()
                self._try_all('_run', date=date)

                if self.day != date.day:
                    self.day = date.day
                    self._try_all('_notify', notify=Notify.FAIRYLAB_DAY)

                self._render(date=date)

            time.sleep(self.sleep)

        if self.ws:
            self.ws.close()

    def _home(self, **kwargs):
        ret = {
            'breadcrumbs': [{
                'href': '',
                'name': 'Home'
            }],
            'browsable': [],
            'internal': []
        }

        date = kwargs['date']
        ps = sorted(self.registered.keys())
        for p in ps:
            instance = self.registered.get(p, None)
            info = ''
            if isinstance(instance, Nameable):
                info = instance._info()

            href = ''
            renderable = isinstance(instance, Renderable)
            if renderable:
                href = instance._href()

            ts, success, danger = '', '', ''
            if isinstance(instance, Registrable):
                ts = delta(instance.date, date)
                success = 'just now' if 's' in ts else ''
                danger = 'error' if not instance.ok else ''

            c = card(
                href=href,
                title=p,
                info=info,
                ts=ts,
                success=success,
                danger=danger)

            if renderable:
                ret['browsable'].append(c)
            else:
                ret['internal'].append(c)

        return ret

    def reload(self, *args, **kwargs):
        value = self._reload_internal(*args, **kwargs)
        if value:
            self._try_all('_setup', **kwargs)
            log(self._name(), **dict(kwargs, s='Completed setup.'))

    def _reload_internal(self, *args, **kwargs):
        if len(args) != 2:
            return False

        path, name = args
        clazz = name.capitalize()
        package = self._package(path, name)

        if package in sys.modules:
            del sys.modules[package]

        try:
            module = importlib.import_module(package)

            if path == 'plugin':
                return self._install(name, module, clazz, **kwargs)
            else:
                s = 'Reloaded {}.'.format(name)
                log(self._name(), **dict(kwargs, s=s))
        except Exception:
            exc = traceback.format_exc()
            log(clazz, **dict(kwargs, s='Exception.', c=exc))

        return False

    def _install(self, name, module, clazz, **kwargs):
        try:
            date = kwargs['date']
            plugin = getattr(module, clazz)
            if issubclass(plugin, Renderable):
                instance = plugin(date=date, e=self.environment)
            else:
                instance = plugin(date=date)
            enabled = instance.enabled
            exc = None
        except Exception:
            date = None
            instance = None
            enabled = False
            exc = traceback.format_exc()

        s = 'Exception.' if exc else 'Installed.' if enabled else 'Disabled.'
        log(clazz, **dict(kwargs, s=s, c=exc))

        if isinstance(instance, Registrable):
            instance.date = date
            instance.ok = enabled
            self.registered[name] = instance

        return enabled

    def reboot(self, *args, **kwargs):
        log(self._name(), **dict(kwargs, s='Rebooting.'))
        os.execv(sys.executable, ['python'] + sys.argv)

    def shutdown(self, *args, **kwargs):
        log(self._name(), **dict(kwargs, s='Shutting down.'))
        self.keep_running = False


if __name__ == '__main__':
    date = datetime.datetime.now()
    env_ = env()
    dashboard = Dashboard(date=date, e=env_)

    handler = LoggingHandler(dashboard)
    logger_ = logging.getLogger('fairylab')
    logger_.addHandler(handler)
    logger_.setLevel(logging.DEBUG)

    fairylab = Fairylab(d=dashboard, e=env_)
    fairylab._setup(date)
    fairylab._start()